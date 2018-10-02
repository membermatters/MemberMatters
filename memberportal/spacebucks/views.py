from django.http import JsonResponse, HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from memberportal.decorators import no_noobs, api_auth
from memberportal.helpers import log_user_event
from .models import SpaceBucks
from profile.models import Profile
import stripe
import json
import pytz
import os

utc = pytz.UTC


@login_required
@no_noobs
def manage_spacebucks(request):
    spacebucks_transactions = SpaceBucks.objects.filter(user=request.user)

    return render(
        request, 'manage_spacebucks.html',
        {"spacebucks_transactions": spacebucks_transactions})


@login_required
@no_noobs
def add_spacebucks(request, amount=None):
    if request.method == "POST":
        if "STRIPE_SECRET_KEY" in os.environ:
            stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
            stripe.default_http_client = stripe.http_client.RequestsClient()
        else:
            return HttpResponseServerError("No stripe API details found.")

        if amount is not None:
            # lets restrict this to something reasonable
            if amount <= 30:
                log_user_event(
                    request.user,
                    "Attempting to charge {} for ${}.".format(
                        request.user.profile.get_full_name(), amount),
                    "stripe")
                charge = stripe.Charge.create(
                    amount=amount * 100,  # convert to cents,
                    currency='aud',
                    description='HSBNE Spacebucks ({})'.format(
                        request.user.profile.get_full_name()),
                    customer=request.user.profile.stripe_customer_id,
                    metadata={'Payment By': request.user.profile.get_full_name(),
                              "For": "Spacebucks Top Up"},
                )

                if charge.paid:
                    transaction = SpaceBucks()
                    transaction.amount = amount
                    transaction.user = request.user
                    transaction.description = "Added spacebucks via Stripe"
                    transaction.transaction_type = "stripe"
                    transaction.logging_info = charge
                    transaction.save()
                    log_user_event(request.user,
                                   "Successfully charged {} for ${}.".format(
                                       request.user.profile.get_full_name(), amount),
                                   "stripe")

                    return render(
                        request, 'add_spacebucks.html',
                        {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"],
                         "success": True,
                         "message": "Successfully charged ${} to your card ending in {}. Please check your spacebucks balance.".format(
                             amount, request.user.profile.stripe_card_last_digits)})
                else:
                    log_user_event(
                        request.user,
                        "Problem charging {}.".format(request.user.profile.get_full_name()),
                        "stripe")
                    return render(
                        request, 'add_spacebucks.html',
                        {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"],
                         "success": False,
                         "message": "There was a problem collecting the funds off your card."})
            else:
                log_user_event(
                  request.user,
                  "Tried to add invalid amount {} to spacebucks via stripe.".format(amount),
                  "stripe")

        return render(request, 'add_spacebucks.html',
                      {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"],
                       "success": False,
                       "message": "Invalid amount."})

    else:
        if "STRIPE_PUBLIC_KEY" in os.environ:
            return render(
                request, 'add_spacebucks.html',
                {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"]})

        else:
            return HttpResponseServerError(
                "Error unable to find stripe details in environment variables.")


@csrf_exempt
def add_spacebucks_payment_info(request):
    if request.method == 'POST':
        if "STRIPE_SECRET_KEY" in os.environ:
            stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
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

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            log_user_event(request.user,
                           "Card declined while saving payment details.",
                           "stripe")

            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": err})

        except stripe.error.RateLimitError as e:
            log_user_event(request.user, "Rate limtied while saving payment details.", "stripe")
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server is talking to stripe too quickly, try again later."})

        except stripe.error.InvalidRequestError as e:
            log_user_event(request.user, "Invalid request while saving payment details.", "stripe", request)
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "There was an error with the request details."})

        except stripe.error.AuthenticationError as e:
            log_user_event(request.user, "Can't authenticate with stripe while saving payment details.", "stripe")
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to authenticate with the Stripe server."})

        except stripe.error.APIConnectionError as e:
            log_user_event(request.user, "Stripe API connection error while saving payment details.", "stripe")
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to communicate with the Stripe server."})

        except stripe.error.StripeError as e:
            log_user_event(request.user, "Unkown stripe while saving payment details.", "stripe", request)
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": e})

        except Exception as e:
            log_user_event(request.user, "Unkown other error while saving payment details.", "stripe", request)
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Unkown error (unrelated to stripe)."})

        log_user_event(request.user, "Successfully save payment details.", "stripe")
        return render(request, 'add_spacebucks.html',
                      {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": True,
                       "message": "Your payment details were successfully saved."})

    else:
        return redirect(reverse('add_spacebucks'))


@login_required
@csrf_exempt
def delete_spacebucks_payment_info(request):
    if "STRIPE_SECRET_KEY" in os.environ:
        stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
        stripe.default_http_client = stripe.http_client.RequestsClient()

    else:
        return HttpResponseServerError("Can't find stripe API details.")

    profile = request.user.profile
    customer = stripe.Customer.retrieve(profile.stripe_customer_id)
    customer.sources.retrieve(customer['default_source']).delete()

    profile.stripe_card_last_digits = ""
    profile.stripe_card_expiry = ""
    profile.save()

    return render(
        request, 'add_spacebucks.html',
        {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": True,
         "message": "Successfully removed saved card details."})


@csrf_exempt
@api_auth
def spacebucks_debit(request, amount=None, description=None, rfid=None):
    if request.method == "GET":
        amount = abs(amount/100)
        profile = Profile.objects.get(rfid=rfid)

    elif request.method == "POST":
        details = json.loads(request.body)
        amount = abs(details['amount']/100)
        description = details['description']
        profile = Profile.objects.get(rfid=details['rfid_code'])

    else:
        return HttpResponseBadRequest("Invalid request method.")

    if profile.spacebucks_balance >= amount:
        transaction = SpaceBucks()
        transaction.amount = amount * -1.0  # abs() handles if we're given a negative number
        transaction.user = profile.user
        transaction.description = description
        transaction.transaction_type = "card"
        transaction.save()

        log_user_event(
          profile.user,
          "Successfully debited ${} from spacebucks account.".format(amount),
          "spacebucks")

        return JsonResponse(
          {"success": True, "balance": round(profile.spacebucks_balance, 2)})

    # not enough $$
    log_user_event(
        profile.user,
        "Not enough funds to debit ${} from spacebucks account.".format(amount),
        "spacebucks")
    return JsonResponse(
        {"success": False,
         "balance": round(profile.spacebucks_balance, 2)})
