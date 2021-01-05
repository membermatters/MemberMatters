from memberbucks.models import MemberBucks

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

import stripe
import json
from constance import config
from membermatters.helpers import log_user_event, log_event

stripe.api_key = config.STRIPE_SECRET_KEY


class MemberBucksTransactions(APIView):
    """
    get: This method returns a member's memberbucks transactions.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        recent_transactions = MemberBucks.objects.filter(user=request.user).order_by(
            "date"
        )[::-1][:100]

        def get_transaction(transaction):
            return transaction.get_transaction_display()

        return Response(
            map(get_transaction, recent_transactions), status=status.HTTP_200_OK
        )


class MemberBucksBalance(APIView):
    """
    get: This method returns a member's memberbucks balance.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(
            {"balance": request.user.profile.memberbucks_balance},
            status=status.HTTP_200_OK,
        )


class MemberBucksAddFunds(APIView):
    """
    post: attempts to charge the saved card and add funds.
    """

    def post(self, request, amount=None):
        profile = request.user.profile

        # check if we got an amount, and if it's less than or equal to 50 dollars
        if amount and amount <= int(config.MEMBERBUCKS_MAX_TOPUP):
            payment_amount = amount * 100  # convert to cents

        else:
            return Response(
                "Invalid amount specified", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=payment_amount,
                currency=config.MEMBERBUCKS_CURRENCY,
                customer=profile.stripe_customer_id,
                payment_method=profile.stripe_payment_method_id,
                off_session=True,
                confirm=True,
            )
        except stripe.error.CardError as e:
            err = e.error
            # Error code will be authentication_required if authentication is needed
            if err.code is "authentication_required":
                return Response(
                    "Card requires 3D Secure which is not yet supported.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment_intent_id = err.payment_intent["id"]
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            print(payment_intent)

            return Response("Error charging card", status=status.HTTP_400_BAD_REQUEST)

        if payment_intent.status == "succeeded":
            MemberBucks.objects.create(
                transaction_type="stripe",
                user=profile.user,
                amount=payment_amount / 100,
            )
            return Response()

        else:
            print(payment_intent.status)
            return Response("Error charging card", status=status.HTTP_400_BAD_REQUEST)


class MemberBucksDonateFunds(APIView):
    """
    post: charges the member the specified amount and removes it from their balance.
    """

    def post(self, request, amount=None):
        profile = request.user.profile

        # check if we got an amount, and if it's less than or equal to the max
        if not (amount and amount <= int(config.MEMBERBUCKS_MAX_TOPUP) * 100):
            return Response(
                "Invalid amount specified", status=status.HTTP_400_BAD_REQUEST
            )

        if profile.memberbucks_balance < amount / 100:
            return Response("Not enough funds", status=status.HTTP_400_BAD_REQUEST)

        MemberBucks.objects.create(
            transaction_type="web",
            user=profile.user,
            amount=abs(amount / 100) * -1,  # make sure it's always negative!
            description=request.data.get(
                "description", "No description. Manual payment via portal."
            ),
        )
        return Response()
