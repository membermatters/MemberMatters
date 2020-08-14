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


@csrf_exempt
@api_auth
def memberbucks_debit(request, amount=None, description="No Description", rfid=None):
    if amount is not None:
        if abs(amount / 100) > 10:
            return HttpResponseBadRequest(
                "400 Invalid request. A maximum of $10 may be debited with this API."
            )

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
        amount = abs(
            details["amount"] / 100
        )  # the abs() stops us accidentally crediting an account if it's negative
        description = details["description"]
        profile = Profile.objects.get(rfid=details["rfid_code"])

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
            message = (
                "Description: {}. Balance Remaining: ${}. If this wasn't you, or you believe there has been an "
                "error, please let us know.".format(
                    transaction.description, profile.memberbucks_balance
                )
            )
            User.objects.get(profile=profile).email_notification(
                subject, subject, subject, message
            )

            log_user_event(
                profile.user,
                f"Successfully debited ${amount} from {config.MEMBERBUCKS_NAME} account.",
                "memberbucks",
            )

            return JsonResponse(
                {"success": True, "balance": round(profile.memberbucks_balance, 2)}
            )

        else:
            return JsonResponse(
                {
                    "success": False,
                    "balance": round(profile.memberbucks_balance, 2),
                    "message": "Whoa! Not so fast!!",
                }
            )

    # not enough $$
    log_user_event(
        profile.user,
        f"Not enough funds to debit ${amount} from {config.MEMBERBUCKS_NAME} account.",
        "memberbucks",
    )
    subject = f"Failed to make a ${amount} {config.MEMBERBUCKS_NAME} purchase."
    User.objects.get(profile=profile).email_notification(
        subject,
        subject,
        subject,
        f"We just tried to debit ${amount} from your {config.MEMBERBUCKS_NAME} balance but were not successful. "
        f"You currently have ${profile.memberbucks_balance}. If this wasn't you, please let us know "
        "immediately.",
    )

    return JsonResponse(
        {"success": False, "balance": round(profile.memberbucks_balance, 2)}
    )


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
        return HttpResponseBadRequest(
            f"400 Invalid request. {config.GROUP_NAME} does not exist."
        )

    try:
        amount = amount / 100  # convert to dollars
        profile = Profile.objects.get(rfid=rfid)
        result = create_group_donation_invoice(profile.user, group, amount)
        if "Error" not in result:
            time_dif = (
                timezone.now() - profile.last_memberbucks_purchase
            ).total_seconds()

            if time_dif > 10:
                transaction = MemberBucks()
                transaction.amount = amount * -1.0
                transaction.user = profile.user
                transaction.description = "Donation to {}.".format(group.name)
                transaction.transaction_type = "card"
                transaction.save()

                profile.last_memberbucks_purchase = timezone.now()
                profile.save()

            return JsonResponse(
                {
                    "success": True,
                    "balance": profile.memberbucks_balance,
                    "donated": amount,
                }
            )

        return HttpResponseServerError("Error while creating invoice: " + result)

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("400 Invalid request. User does not exist.")
