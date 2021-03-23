from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from membermatters.decorators import api_auth
from membermatters.helpers import log_user_event
from .models import MemberBucks
from profile.models import Profile, User
from constance import config
import json
import pytz

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
