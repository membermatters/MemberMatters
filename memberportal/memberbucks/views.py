from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone
from membermatters.decorators import no_noobs, api_auth
from membermatters.helpers import log_user_event
from .models import MemberBucks
from profile.models import Profile, User
from group.models import Group
from profile.xerohelpers import create_group_donation_invoice
from constance import config
import stripe
import json
import pytz
import os

utc = pytz.UTC


@login_required
@no_noobs
def manage_memberbucks(request):
    memberbucks_transactions = MemberBucks.objects.filter(user=request.user)

    return render(
        request, 'manage_memberbucks.html',
        {"memberbucks_transactions": memberbucks_transactions})


@login_required
@no_noobs
def add_memberbucks_page(request):
    if "PORTAL_STRIPE_PUBLIC_KEY" in os.environ:
        return render(
            request, 'add_memberbucks.html',
            {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"]})

    else:
        return HttpResponseServerError(
            "Error unable to find stripe details in environment variables.")


@login_required
@no_noobs
def add_memberbucks(request, amount=None):
    if request.method == "GET":
        if "PORTAL_STRIPE_SECRET_KEY" in os.environ:
            stripe.api_key = os.environ["PORTAL_STRIPE_SECRET_KEY"]
            stripe.default_http_client = stripe.http_client.RequestsClient()
        else:
            return HttpResponseServerError("No stripe API details found.")

        if amount is not None:
            # lets restrict this to something reasonable
            if amount <= 30:
                log_user_event(request.user, "Attempting to charge {} for ${}.".format(
                    request.user.profile.get_full_name(), amount),
                               "stripe")
                charge = stripe.Charge.create(
                    amount=amount * 100,  # convert to cents,
                    currency='aud',
                    description=f'{config.MEMBERBUCKS_NAME} ({request.user.profile.get_full_name()})',
                    customer=request.user.profile.stripe_customer_id,
                    metadata={'Payment By': request.user.profile.get_full_name(),
                              "For": f"{config.MEMBERBUCKS_NAME} Top Up"},
                )

                if charge.paid:
                    transaction = MemberBucks()
                    transaction.amount = amount
                    transaction.user = request.user
                    transaction.description = f"Added {config.MEMBERBUCKS_NAME} via Stripe"
                    transaction.transaction_type = "stripe"
                    transaction.logging_info = charge
                    transaction.save()
                    log_user_event(request.user, "Successfully charged {} for ${}.".format(
                        request.user.profile.get_full_name(), amount),
                                   "stripe")
                    subject = f"You just added {config.MEMBERBUCKS_NAME} to your {config.SITE_OWNER} account."
                    request.user.email_notification(subject, subject, subject, f"We just charged you card for ${amount} and "
                                                                               f"added this to your {config.MEMBERBUCKS_NAME} balance."
                                                                               "If this wasn't you, please let us know "
                                                                               "immediately.")

                    return JsonResponse({"success": True})
                else:
                    log_user_event(request.user, "Problem charging {}.".format(request.user.profile.get_full_name()),
                                   "stripe")
                    subject = f"Failed to add {config.MEMBERBUCKS_NAME} to your {config.SITE_OWNER} account."
                    request.user.email_notification(subject, subject, subject, "We just tried to charge your card for"
                                                                               f"${amount} for {config.MEMBERBUCKS_NAME} but were not "
                                                                               "successful. If this wasn't you, please "
                                                                               "let us know immediately.")
                    return JsonResponse({"success": False})
            else:
                log_user_event(request.user, f"Tried to add invalid amount {amount} to {config.MEMBERBUCKS_NAME} via stripe.",
                               "stripe")

        return render(request, 'add_memberbucks.html',
                      {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"],
                       "success": False,
                       "message": "Invalid amount."})
    else:
        return HttpResponseBadRequest("Invalid method")


@csrf_exempt
def add_memberbucks_payment_info(request):
    if request.method == 'POST':
        if "PORTAL_STRIPE_SECRET_KEY" in os.environ:
            stripe.api_key = os.environ["PORTAL_STRIPE_SECRET_KEY"]
            stripe.default_http_client = stripe.http_client.RequestsClient()

        else:
            return HttpResponseServerError("Can't find stripe API details.")

        try:
            log_user_event(request.user,
                           "Attempting to create stripe customer.", "stripe")
            customer = stripe.Customer.create(
                source=request.POST.get("stripeToken"),
                email=request.POST.get("stripeEmail"),
            )

            profile = request.user.profile
            profile.stripe_customer_id = customer.id
            profile.stripe_card_expiry = str(
                customer.sources.data[0]['exp_month']) + '/' + str(
                customer.sources.data[0]['exp_year'])
            profile.stripe_card_last_digits = customer.sources.data[0]['last4']
            profile.save()
            log_user_event(
                request.user, "Created stripe customer.".format(
                    request.user.profile.get_full_name()), "stripe")

            subject = f"You just added a payment card to your {config.SITE_OWNER} account."
            request.user.email_notification(subject, subject, subject, "Don't worry, your card details are stored safe "
                                                                       "with Stripe and are not on our servers. You "
                                                                       "can remove this card at any time via the "
                                                                       f"{config.SITE_NAME}.")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            log_user_event(request.user,
                           "Card declined while saving payment details.",
                           "stripe")

            return render(request, 'add_memberbucks.html',
                          {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": False,
                           "message": err})

        except stripe.error.RateLimitError as e:
            log_user_event(request.user, "Rate limtied while saving payment details.", "stripe")
            return render(request, 'add_memberbucks.html',
                          {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server is talking to stripe too quickly, try again later."})

        except stripe.error.InvalidRequestError as e:
            log_user_event(request.user, "Invalid request while saving payment details.", "stripe", request)
            return render(request, 'add_memberbucks.html',
                          {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "There was an error with the request details."})

        except stripe.error.AuthenticationError as e:
            log_user_event(request.user, "Can't authenticate with stripe while saving payment details.", "stripe")
            return render(request, 'add_memberbucks.html',
                          {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to authenticate with the Stripe server."})

        except stripe.error.APIConnectionError as e:
            log_user_event(request.user, "Stripe API connection error while saving payment details.", "stripe")
            return render(request, 'add_memberbucks.html',
                          {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to communicate with the Stripe server."})

        except stripe.error.StripeError as e:
            log_user_event(request.user, "Unkown stripe while saving payment details.", "stripe", request)
            return render(request, 'add_memberbucks.html',
                          {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": False,
                           "message": e})

        except Exception as e:
            log_user_event(request.user, "Unkown other error while saving payment details.", "stripe", request)
            return render(request, 'add_memberbucks.html',
                          {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Unkown error (unrelated to stripe)."})

        log_user_event(request.user, "Successfully saved payment details.", "stripe")
        return render(request, 'add_memberbucks.html',
                      {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": True,
                       "message": "Your payment details were successfully saved."})

    else:
        return redirect(reverse('add_memberbucks'))


@login_required
@csrf_exempt
def delete_memberbucks_payment_info(request):
    if "PORTAL_STRIPE_SECRET_KEY" in os.environ:
        stripe.api_key = os.environ["PORTAL_STRIPE_SECRET_KEY"]
        stripe.default_http_client = stripe.http_client.RequestsClient()

    else:
        return HttpResponseServerError("Can't find stripe API details.")

    profile = request.user.profile

    try:
        customer = stripe.Customer.retrieve(profile.stripe_customer_id)
        customer.sources.retrieve(customer['default_source']).delete()

    except stripe.error.InvalidRequestError as e:
        # this ignores the error that happens when a user doesn't have saved details, sometimes needed.
        pass

    profile.stripe_card_last_digits = ""
    profile.stripe_card_expiry = ""
    profile.save()

    subject = f"You just removed a saved card from your {config.SITE_OWNER} account."
    request.user.email_notification(subject, subject, subject, "If this wasn't you, please let us know immediately.")

    return render(
        request, 'add_memberbucks.html',
        {"PORTAL_STRIPE_PUBLIC_KEY": os.environ["PORTAL_STRIPE_PUBLIC_KEY"], "success": True,
         "message": "Successfully removed saved card details."})


@csrf_exempt
@api_auth
def memberbucks_debit(request, amount=None, description="No Description", rfid=None):
    if amount is not None:
        if abs(amount / 100) > 10:
            return HttpResponseBadRequest("400 Invalid request. A maximum of $10 may be debited with this API.")

    if request.method == "GET":
        if amount is None or rfid is None:
            return HttpResponseBadRequest("400 Invalid request.")

        amount = abs(amount / 100)
        try:
            profile = Profile.objects.get(rfid=rfid)

        except ObjectDoesNotExist:
            return HttpResponseBadRequest("400 Invalid request. User does not exist.")

    elif request.method == "POST":
        details = json.loads(request.body)
        amount = abs(details['amount'] / 100)  # the abs() stops us accidentally crediting an account if it's negative
        description = details['description']
        profile = Profile.objects.get(rfid=details['rfid_code'])

    else:
        return HttpResponseBadRequest("400 Invalid request method.")

    if profile.memberbucks_balance >= amount:
        time_dif = (timezone.now() - profile.last_memberbucks_purchase).total_seconds()
        print(time_dif)

        if time_dif > 5:
            transaction = MemberBucks()
            transaction.amount = amount * -1.0
            transaction.user = profile.user
            transaction.description = description.replace("+", " ")
            transaction.transaction_type = "card"
            transaction.save()

            profile.last_memberbucks_purchase = timezone.now()
            profile.save()

            subject = f"You just made a ${amount} {config.MEMBERBUCKS_NAME} purchase."
            message = "Description: {}. Balance Remaining: ${}. If this wasn't you, or you believe there has been an " \
                      "error, please let us know.".format(transaction.description, profile.memberbucks_balance)
            User.objects.get(profile=profile).email_notification(subject, subject, subject, message)

            log_user_event(profile.user, f"Successfully debited ${amount} from {config.MEMBERBUCKS_NAME} account.",
                           "memberbucks")

            return JsonResponse({"success": True, "balance": round(profile.memberbucks_balance, 2)})

        else:
            return JsonResponse({"success": False, "balance": round(profile.memberbucks_balance, 2),
                                 "message": "Whoa! Not so fast!!"})

    # not enough $$
    log_user_event(profile.user, f"Not enough funds to debit ${amount} from {config.MEMBERBUCKS_NAME} account.",
                   "memberbucks")
    subject = f"Failed to make a ${amount} {config.MEMBERBUCKS_NAME} purchase."
    User.objects.get(profile=profile).email_notification(subject, subject, subject,
                                                         f"We just tried to debit ${amount} from your {config.MEMBERBUCKS_NAME} balance but were not successful. "
                                                         f"You currently have ${profile.memberbucks_balance}. If this wasn't you, please let us know "
                                                         "immediately."
                                                         )

    return JsonResponse({"success": False, "balance": round(profile.memberbucks_balance, 2)})


@api_auth
def memberbucks_balance(request, rfid=None):
    if rfid is None:
        return HttpResponseBadRequest("400 Invalid request.")

    try:
        profile = Profile.objects.get(rfid=rfid)
        return JsonResponse({"balance": profile.memberbucks_balance})

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("400 Invalid request. User does not exist.")


@api_auth
def memberbucks_group_donation(request, rfid=None, group_id=None, amount=None):
    if group_id is None or rfid is None or amount is None:
        return HttpResponseBadRequest("400 Invalid request.")

    try:
        group = Group.objects.get(pk=group_id)

    except ObjectDoesNotExist:
        return HttpResponseBadRequest(f"400 Invalid request. {config.GROUP_NAME} does not exist.")

    try:
        amount = amount / 100  # convert to dollars
        profile = Profile.objects.get(rfid=rfid)
        result = create_group_donation_invoice(profile.user, group, amount)
        if "Error" not in result:
            time_dif = (timezone.now() - profile.last_memberbucks_purchase).total_seconds()
            print(time_dif)

            if time_dif > 10:
                transaction = MemberBucks()
                transaction.amount = amount * -1.0
                transaction.user = profile.user
                transaction.description = "Donation to {}.".format(group.name)
                transaction.transaction_type = "card"
                transaction.save()

                profile.last_memberbucks_purchase = timezone.now()
                profile.save()

            return JsonResponse({"success": True, "balance": profile.memberbucks_balance, "donated": amount})

        return HttpResponseServerError("Error while creating invoice: " + result)

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("400 Invalid request. User does not exist.")
