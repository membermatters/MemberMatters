from memberbucks.models import MemberBucks

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api_admin_tools.models import *
import stripe
import json
from constance import config
from membermatters.helpers import log_user_event, log_event

stripe.api_key = config.STRIPE_SECRET_KEY


class MemberBucksAddCard(APIView):
    """
    get: gets the client secret used to add new card details.
    post: saves the customers card details.
    """

    def get(self, request):
        profile = request.user.profile

        if not profile.stripe_customer_id:
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

                intent = stripe.SetupIntent.create(customer=profile.stripe_customer_id)

                return Response({"clientSecret": intent.client_secret})

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
                    {
                        "success": False,
                        "message": err,
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.RateLimitError as e:
                log_user_event(
                    request.user, "Rate limited while saving payment details.", "stripe"
                )

                return Response(
                    {
                        "success": False,
                        "message": e,
                    },
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
                    {
                        "success": False,
                        "message": e,
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.AuthenticationError as e:
                log_user_event(
                    request.user,
                    "Can't authenticate with stripe while saving payment details.",
                    "stripe",
                )

                return Response(
                    {
                        "success": False,
                        "message": e,
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except stripe.error.APIConnectionError as e:
                log_user_event(
                    request.user,
                    "Stripe API connection error while saving payment details.",
                    "stripe",
                )

                return Response(
                    {
                        "success": False,
                        "message": e,
                    },
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
                    {
                        "success": False,
                        "message": e,
                    },
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

        else:
            intent = stripe.SetupIntent.create(customer=profile.stripe_customer_id)

            return Response({"clientSecret": intent.client_secret})

    def post(self, request):
        profile = request.user.profile
        payment_method_id = request.data.get("paymentMethodId")

        payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

        profile.stripe_card_last_digits = payment_method["card"]["last4"]
        profile.stripe_card_expiry = f"{str(payment_method['card']['exp_month']).zfill(2)}/{str(payment_method['card']['exp_year'])}"
        profile.stripe_payment_method_id = payment_method_id
        profile.save()

        # attached the payment method to the customer
        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=profile.stripe_customer_id,
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            profile.stripe_customer_id,
            invoice_settings={
                "default_payment_method": payment_method_id,
            },
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

        return Response()

    def delete(self, request):
        profile = request.user.profile

        if profile.stripe_payment_method_id:
            stripe.PaymentMethod.detach(profile.stripe_payment_method_id)

        profile.stripe_payment_method_id = ""
        profile.stripe_card_last_digits = ""
        profile.stripe_card_expiry = ""
        profile.save()
        return Response()


class MemberTiers(APIView):
    """
    get: gets a list of all member tiers.
    """

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        tiers = MemberTier.objects.filter(visible=True)
        formatted_tiers = []

        for tier in tiers:
            plans = []

            for plan in tier.plans.filter(visible=True):
                plans.append(
                    {
                        "id": plan.id,
                        "name": plan.name,
                        "currency": plan.currency,
                        "cost": plan.cost,
                        "intervalAmount": plan.interval_count,
                        "interval": plan.interval,
                    }
                )

            formatted_tiers.append(
                {
                    "id": tier.id,
                    "name": tier.name,
                    "description": tier.description,
                    "featured": tier.featured,
                    "plans": plans,
                }
            )

        return Response(formatted_tiers)


class StripeWebhook(APIView):
    """
    post: processes a Stripe webhook event.
    """

    def post(self, request):
        webhook_secret = config.STRIPE_WEBHOOK_SECRET
        request_data = request.data

        if webhook_secret:
            # Retrieve the event by verifying the signature if webhook signing is configured.
            signature = request.headers.get("stripe-signature")
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body, sig_header=signature, secret=webhook_secret
                )
                data = event["data"]
            except Exception as e:
                return e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event["type"]
        else:
            data = request_data["data"]
            event_type = request_data["type"]

        data_object = data["object"]
        print(data_object)

        if event_type == "invoice.paid":
            print("INVOICE PAID")
            print(data)

        if event_type == "invoice.payment_failed":
            print("INVOICE PAYMENT FAILED")
            print(data)

        if event_type == "customer.subscription.deleted":
            print("SUBSCRIPTION DELETED")
            print(data)

        return Response()
