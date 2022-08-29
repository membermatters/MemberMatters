from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from membermatters.helpers import log_user_event
from .models import MemberBucks
from profile.models import Profile, User
from constance import config
import pytz

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

utc = pytz.UTC


class MemberbucksDebit(APIView):
    """
    get:
    post:
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, rfid=None, amount=None, description="No Description"):
        if amount is None or rfid is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        amount = abs(
            amount / 100
        )  # the abs() stops us accidentally crediting an account if it's negative
        try:
            profile = Profile.objects.get(rfid=rfid)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if amount is not None:
            if abs(amount / 100) > 10:
                return Response(
                    f"A maximum of {config.LOCAL_FIAT_CURRENCY}10 may be debited with this API.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if profile.memberbucks_balance >= amount:
            time_dif = (
                timezone.now() - profile.last_memberbucks_purchase
            ).total_seconds()

            if time_dif > 5:
                transaction = MemberBucks()
                transaction.amount = amount * -1.0
                transaction.user = profile.user
                transaction.description = description.replace("+", " ")
                transaction.transaction_type = "card"
                transaction.save()

                profile.last_memberbucks_purchase = timezone.now()
                profile.save()

                subject = (
                    f"You just made a {config.LOCAL_FIAT_CURRENCY}{amount} {config.MEMBERBUCKS_NAME} purchase."
                )
                message = (
                    "Description: {}. Balance Remaining: {config.LOCAL_FIAT_CURRENCY}{}. If this wasn't you, or you believe there has been an "
                    "error, please let us know.".format(
                        transaction.description, profile.memberbucks_balance
                    )
                )
                User.objects.get(profile=profile).email_notification(
                    subject, subject, subject, message
                )

                log_user_event(
                    profile.user,
                    f"Successfully debited {config.LOCAL_FIAT_CURRENCY}{amount} from {config.MEMBERBUCKS_NAME} account.",
                    "memberbucks",
                )

                return Response(
                    {"success": True, "balance": round(profile.memberbucks_balance, 2)}
                )

            else:
                log_user_event(
                    profile.user,
                    f"Not enough funds to debit {config.LOCAL_FIAT_CURRENCY}{amount} from {config.MEMBERBUCKS_NAME} account.",
                    "memberbucks",
                )
                subject = (
                    f"Failed to make a {config.LOCAL_FIAT_CURRENCY}{amount} {config.MEMBERBUCKS_NAME} purchase."
                )
                User.objects.get(profile=profile).email_notification(
                    subject,
                    subject,
                    subject,
                    f"We just tried to debit {config.LOCAL_FIAT_CURRENCY}{amount} from your {config.MEMBERBUCKS_NAME} balance but were not successful. "
                    f"You currently have {config.LOCAL_FIAT_CURRENCY}{profile.memberbucks_balance}. If this wasn't you, please let us know "
                    "immediately.",
                )

                return Response(
                    {"success": False, "balance": round(profile.memberbucks_balance, 2)}
                )

        else:
            return Response(
                {
                    "success": False,
                    "balance": round(profile.memberbucks_balance, 2),
                    "message": "Whoa! Not so fast!!",
                }
            )


class MemberbucksBalance(APIView):
    """
    get: returns the member's current memberbucks balance.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, rfid=None):
        if rfid is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(rfid=rfid)
            return Response({"balance": profile.memberbucks_balance})

        except ObjectDoesNotExist:
            return Response()
