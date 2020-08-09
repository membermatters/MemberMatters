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


class MemberBucksAddCard(APIView):
    """
    get: gets the client secret used to add new card details.
    post: saves the customers card details.
    """

    def get(self, request):
        profile = request.user.profile

        if profile.stripe_customer_id is None:
            try:
                log_user_event(
                    request.user, "Attempting to create stripe customer.", "stripe"
                )
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=profile.get_full_name(),
                    phone=profile.phone,
                    invoice_prefix=profile.xero_account_number,
                )

                profile.stripe_customer_id = customer.id
                profile.save()

                log_user_event(
                    request.user,
                    f"Created stripe customer {request.user.profile.get_full_name()} (Stripe ID: {customer.id}).",
                    "stripe",
                )

                subject = f"You just added a payment card to your {config.SITE_OWNER} account."
                request.user.email_notification(
                    subject,
                    subject,
                    subject,
                    "Don't worry, your card details are stored safe "
                    "with Stripe and are not on our servers. You "
                    "can remove this card at any time via the "
                    f"{config.SITE_NAME}.",
                )

            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body.get("error", {})

                log_user_event(
                    request.user,
                    "Card declined while saving payment details.",
                    "stripe",
                )

                return Response(
                    {"success": False, "message": err,},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.RateLimitError as e:
                log_user_event(
                    request.user, "Rate limited while saving payment details.", "stripe"
                )

                return Response(
                    {"success": False, "message": e,},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.InvalidRequestError as e:
                log_user_event(
                    request.user,
                    "Invalid request while saving payment details.",
                    "stripe",
                    request,
                )

                return Response(
                    {"success": False, "message": e,},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.AuthenticationError as e:
                log_user_event(
                    request.user,
                    "Can't authenticate with stripe while saving payment details.",
                    "stripe",
                )

                return Response(
                    {"success": False, "message": e,},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.APIConnectionError as e:
                log_user_event(
                    request.user,
                    "Stripe API connection error while saving payment details.",
                    "stripe",
                )

                return Response(
                    {"success": False, "message": e,},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.StripeError as e:
                log_user_event(
                    request.user,
                    "Unknown stripe while saving payment details.",
                    "stripe",
                    request,
                )

                return Response(
                    {"success": False, "message": e,},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except Exception as e:
                log_user_event(
                    request.user,
                    "Unknown other error while saving payment details.",
                    "stripe",
                    request,
                )
                return Response(
                    {
                        "success": False,
                        "message": "Unknown error (unrelated to stripe).",
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            log_user_event(
                request.user, "Successfully saved payment details.", "stripe"
            )
            return None

        else:
            intent = stripe.SetupIntent.create(customer=profile.stripe_customer_id)

            return Response({"clientSecret": intent.client_secret})

    def post(self, request):
        body = request.data

        profile = request.user.profile
        profile.stripe_card_last_digits = body["card"]["last4"]
        profile.stripe_card_expiry = (
            f"{str(body['card']['exp_month']).zfill(2)}/{str(body['card']['exp_year'])}"
        )
        profile.save()
        return Response()
