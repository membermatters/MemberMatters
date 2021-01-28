from profile.models import Profile
from api_admin_tools.models import *

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

import stripe
from constance import config
from datetime import datetime, timedelta
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
                        "message": str(e),
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
                plans.append(plan.get_object())

            formatted_tiers.append(tier.get_object())

        return Response(formatted_tiers)


class PaymentPlanSignup(APIView):
    """
    post: attempts to sign the member up to a new membership payment plan.
    """

    def post(self, request, plan_id):
        current_plan = request.user.profile.membership_plan

        if current_plan:
            return Response({"success": False}, status=status.HTTP_409_CONFLICT)

        else:
            new_plan = PaymentPlan.objects.get(pk=plan_id)
            new_subscription = stripe.Subscription.create(
                customer=request.user.profile.stripe_customer_id,
                items=[
                    {"price": new_plan.stripe_id},
                ],
            )
            request.user.profile.stripe_subscription_id = new_subscription.id
            request.user.profile.membership_plan = new_plan
            request.user.profile.save()

            if new_subscription.status == "active":
                return Response({"success": True})

            return Response({"success": False})


class CanSignup(APIView):
    """
    get: checks if the member is elligible to signup, and what actions they need to complete.
    """

    def get(self, request):
        return Response(request.user.profile.can_signup())


class SubscriptionInfo(APIView):
    """
    get: retrieves information about the members subscription.
    """

    def get(self, request):
        current_plan = request.user.profile.membership_plan

        if not current_plan:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        else:
            s = stripe.Subscription.retrieve(
                request.user.profile.stripe_subscription_id,
            )

            if s:
                subscription = {
                    "billingCycleAnchor": s.billing_cycle_anchor,
                    "currentPeriodEnd": s.current_period_end,
                    "cancelAt": s.cancel_at,
                    "cancelAtPeriodEnd": s.cancel_at_period_end,
                    "startDate": s.start_date,
                }
                return Response({"success": True, "subscription": subscription})

            return Response({"success": False})


class PaymentPlanResumeCancel(APIView):
    """
    post: attempts to cancel a member's payment plan.
    """

    def post(self, request, resume):
        current_plan = request.user.profile.membership_plan
        resume = True if resume == "resume" else False

        if not current_plan:
            return Response(
                {"success": False, "message": "paymentPlan.notExists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        else:
            # this will modify the subscription to automatically cancel at the end of the current payment plan
            if resume:
                modified_subscription = stripe.Subscription.modify(
                    request.user.profile.stripe_subscription_id,
                    cancel_at_period_end=False,
                )

                if modified_subscription.cancel_at_period_end == False:
                    request.user.profile.subscription_status = "active"
                    request.user.profile.save()
                    return Response({"success": True})

            else:
                modified_subscription = stripe.Subscription.modify(
                    request.user.profile.stripe_subscription_id,
                    cancel_at_period_end=True,
                )

                if modified_subscription.cancel_at_period_end == True:
                    request.user.profile.subscription_status = "cancelling"
                    request.user.profile.save()
                    return Response({"success": True})

            return Response({"success": False})


class StripeWebhook(APIView):
    """
    post: processes a Stripe webhook event.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        webhook_secret = config.STRIPE_WEBHOOK_SECRET
        body = request.body
        request_data = request.data

        if webhook_secret:
            # Retrieve the event by verifying the signature if webhook signing is configured.
            signature = request.headers.get("stripe-signature")
            try:
                event = stripe.Webhook.construct_event(
                    payload=body, sig_header=signature, secret=webhook_secret
                )
                data = event["data"]
            except Exception as e:
                print(e)
                return Response({"error": "Error validaitng Stripe signature."})

            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event["type"]
        else:
            data = request_data["data"]
            event_type = request_data["type"]

        data = data["object"]
        try:
            member = Profile.objects.get(stripe_customer_id=data["customer"])

        except Profile.DoesNotExist:
            return Response()

        # Just in case the linked Stripe account also processes other payments we should just ignore a non existant customer.
        if not member:
            return Response()

        if event_type == "invoice.paid":
            print("INVOICE PAID EVENT")

            invoice_status = data["status"]

            if invoice_status == "paid" and member.state != "active":
                # if the invoice was paid and the member isn't active, then activate them
                subject = "Your payment was successful."
                title = subject
                preheader = ""
                message = "Thanks for making a payment via our automated billing system. You will receive another email shortly confirming that your access has been enabled, or if any additional steps are required to be completed."

                member.user.email_notification(subject, title, preheader, message)
                member.activate()
                member.subscription_status = "active"
                member.save()

                # in all other instances, we don't care about the event and can ignore it

        if event_type == "invoice.payment_failed":
            print("INVOICE PAYMENT FAILED")

            subject = "Your membership payment failed"
            title = subject
            preheader = ""
            message = "Hi there, your membership payment failed. Please update your billing information or contact us to resolve this issue. We'll try again, but if we're unable to collect your payment, your membership may be cancelled."

            member.user.email_notification(self, subject, title, preheader, message)

        if event_type == "customer.subscription.deleted":
            print("SUBSCRIPTION DELETED")

            # the subscription was deleted, so deactivate the member
            subject = "Your membership has been cancelled"
            title = subject
            preheader = ""
            message = "You will receive another email shortly confirming that your access has been deactivated. Your membership was either cancelled at your request or because we couldn't collect your payment."

            member.user.email_notification(subject, title, preheader, message)
            member.deactivate()
            member.membership_plan = None
            member.stripe_subscription_id = None
            member.subscription_status = "inactive"
            member.save()

        return Response()
