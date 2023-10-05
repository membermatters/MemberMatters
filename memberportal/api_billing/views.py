from asgiref.sync import sync_to_async

from profile.models import Profile
from access.models import Doors, Interlock
from api_admin_tools.models import *

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

import stripe
import logging
from services.canvas import Canvas
from services.moodle_integration import (
    moodle_get_course_activity_completion_status,
    moodle_get_user_from_email,
)
from services.emails import send_email_to_admin
from constance import config
from django.db.utils import OperationalError
from sentry_sdk import capture_exception

logger = logging.getLogger("app")


class StripeAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not config.ENABLE_STRIPE:
            return

        try:
            stripe.api_key = config.STRIPE_SECRET_KEY
        except OperationalError as error:
            capture_exception(error)


class MemberBucksAddCard(StripeAPIView):
    """
    get: gets the client secret used to add new card details.
    post: saves the customers card details.
    """

    def get(self, request):
        profile = request.user.profile
        customer_exists = True

        # check that the customer exists and isn't deleted
        if profile.stripe_customer_id:
            try:
                customer = stripe.Customer.retrieve(profile.stripe_customer_id)
                if customer.get("deleted") or not customer:
                    customer_exists = False

            except stripe.error.InvalidRequestError as error:
                # Invalid parameters were supplied to Stripe's API
                capture_exception(error)

                # if the customer doesn't exist then remove the Stripe customer id
                if error.http_status == 404:
                    profile.stripe_customer_id = None
                    profile.save()

                    customer_exists = False

        else:
            customer_exists = False

        if not customer_exists:
            try:
                request.user.log_event(
                    "Attempting to create stripe customer.", "stripe"
                )
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=profile.get_full_name(),
                    phone=profile.phone,
                )

                profile.stripe_customer_id = customer.id
                profile.save()

                request.user.log_event(
                    f"Created stripe customer {request.user.profile.get_full_name()} (Stripe ID: {customer.id}).",
                    "stripe",
                )

                intent = stripe.SetupIntent.create(customer=profile.stripe_customer_id)

                return Response({"clientSecret": intent.client_secret})

            except stripe.error.StripeError as e:
                request.user.log_event(
                    "Unknown stripe while saving payment details.",
                    "stripe",
                    request,
                )
                capture_exception(e)

                return Response(
                    {
                        "success": False,
                        "message": str(e),
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            except Exception as e:
                request.user.log_event(
                    "Unknown other error while saving payment details.",
                    "stripe",
                    request,
                )
                capture_exception(e)
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

        try:
            request.user.email_notification(
                subject,
                "Don't worry, your card details are stored safe "
                "with Stripe and are not on our servers. You "
                "can remove this card at any time via the "
                f"{config.SITE_NAME}.",
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                {"message": "error.postmarkNotConfigured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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


class MemberTiers(StripeAPIView):
    """
    get: gets a list of all membership plans.
    """

    def get(self, request):
        tiers = MemberTier.objects.filter(visible=True)
        formatted_tiers = []

        for tier in tiers:
            plans = []

            for plan in tier.plans.filter(visible=True):
                plans.append(plan.get_object())

            formatted_tiers.append(tier.get_object())

        return Response(formatted_tiers)


class PaymentPlanSignup(StripeAPIView):
    """
    post: attempts to sign the member up to a new membership plan.
    """

    def post(self, request, plan_id):
        current_plan = request.user.profile.membership_plan
        new_plan = PaymentPlan.objects.get(pk=plan_id)

        if current_plan:
            return Response({"success": False}, status=status.HTTP_409_CONFLICT)

        def create_subscription(attempts=0):
            attempts += 1

            if attempts > 3:
                request.user.log_event(
                    "Too many attempts while creating subscription.",
                    "stripe",
                    "",
                )
                return Response(
                    {
                        "success": False,
                        "message": None,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            try:
                return stripe.Subscription.create(
                    customer=request.user.profile.stripe_customer_id,
                    items=[
                        {"price": new_plan.stripe_id},
                    ],
                )

            except stripe.error.InvalidRequestError as e:
                capture_exception(e)
                error = e.json_body.get("error")

                if (
                    error["code"] == "resource_missing"
                    and "default payment method" in error["message"]
                ):
                    request.user.log_event(
                        "InvalidRequestError (missing default payment method) from Stripe while creating subscription.",
                        "stripe",
                        error,
                    )

                    # try to set the default and try again
                    stripe.Customer.modify(
                        request.user.profile.stripe_customer_id,
                        invoice_settings={
                            "default_payment_method": request.user.profile.stripe_payment_method_id,
                        },
                    )

                    return create_subscription(attempts)

                if (
                    error["code"] == "resource_missing"
                    and "a similar object exists in live mode" in error["message"]
                ):
                    request.user.log_event(
                        "InvalidRequestError (used test key with production object) from Stripe while "
                        "creating subscription.",
                        "stripe",
                        error,
                    )

                    return Response(
                        {
                            "success": False,
                            "message": error["message"],
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                else:
                    request.user.log_event(
                        "InvalidRequestError from Stripe while creating subscription.",
                        "stripe",
                        error,
                    )
                    return Response(
                        {
                            "success": False,
                            "message": None,
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            except Exception as e:
                request.user.log_event(
                    "InvalidRequestError from Stripe while creating subscription.",
                    "stripe",
                    e,
                )
                capture_exception(e)
                return Response(
                    {
                        "success": False,
                        "message": None,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        new_subscription = create_subscription()

        try:
            if new_subscription.status == "active":
                request.user.profile.stripe_subscription_id = new_subscription.id
                request.user.profile.membership_plan = new_plan
                request.user.profile.subscription_status = "active"
                request.user.profile.save()

                request.user.log_event(
                    "Successfully created subscription in Stripe.",
                    "stripe",
                    "",
                )

                return Response({"success": True})

            elif new_subscription.status == "incomplete":
                # if we got here, that means the subscription wasn't successfully created
                request.user.log_event(
                    f"Failed to create subscription in Stripe with status {new_subscription.status}.",
                    "stripe",
                    "",
                )

                return Response(
                    {"success": True, "message": "signup.subscriptionFailed"}
                )

            else:
                request.user.log_event(
                    f"Failed to create subscription in Stripe with status {new_subscription.status}.",
                    "stripe",
                    "",
                )
                return Response({"success": True})

        except KeyError as e:
            capture_exception(e)
            return new_subscription or e


class CanSignup(APIView):
    """
    get: checks if the member is eligible to signup, and what actions they need to complete.
    """

    def get(self, request):
        return Response(request.user.profile.can_signup())


class AssignAccessCard(APIView):
    """
    post: assigns the access card to the member.
    """

    def post(self, request):
        profile = request.user.profile
        profile.rfid = request.data["accessCard"]
        profile.save()

        return Response({"success": True})


class CheckInductionStatus(APIView):
    """
    post: checks if the member has completed the induction (via the canvas/moodle API).
    """

    def post(self, request):
        if "induction" not in request.user.profile.can_signup()["requiredSteps"]:
            return Response({"success": True, "score": 0, "notRequired": True})

        score = 0

        if config.MOODLE_INDUCTION_ENABLED:
            user_id = moodle_get_user_from_email(request.user.email).get("id")
            activities = moodle_get_course_activity_completion_status(
                config.MOODLE_INDUCTION_COURSE_ID, user_id
            )
            score = activities["percentage_completed"]

        elif config.CANVAS_INDUCTION_ENABLED:
            try:
                canvas_api = Canvas()
            except OperationalError as error:
                capture_exception(error)
                return Response({"success": False, "score": 0})

            score = (
                canvas_api.get_student_score_for_course(
                    config.CANVAS_INDUCTION_COURSE_ID, request.user.email
                )
                or 0
            )

        try:
            if score or config.MIN_INDUCTION_SCORE == 0:
                induction_passed = score >= config.MIN_INDUCTION_SCORE

                if induction_passed:
                    request.user.profile.update_last_induction()

                    return Response({"success": True, "score": score})
            return Response({"success": False, "score": score})

        except Exception as e:
            capture_exception(e)
            return Response({"success": False, "score": 0, "error": str(e)})


class CompleteSignup(StripeAPIView):
    """
    post: completes the member's signup if they have completed all requirements and enables access
    """

    def post(self, request):
        member_profile = request.user.profile
        signupCheck = member_profile.can_signup()

        if signupCheck["success"]:
            member_profile.activate()

            # give default door access
            for door in Doors.objects.filter(all_members=True):
                member_profile.doors.add(door)

            # give default interlock access
            for interlock in Interlock.objects.filter(all_members=True):
                member_profile.interlocks.add(interlock)

            member_profile.user.email_membership_application()
            member_profile.user.email_welcome()

            return Response({"success": True})

        return Response(
            {
                "success": False,
                "message": "signup.requirementsNotMet",
                "items": signupCheck["requiredSteps"],
            }
        )


class SkipSignup(APIView):
    """
    post: skips the billing/tier signup process if they just want an account
    """

    def post(self, request):
        request.user.profile.set_account_only()

        return Response({"success": True})


class SubscriptionInfo(StripeAPIView):
    """
    get: retrieves information about the members subscription.
    """

    def get(self, request):
        current_plan = request.user.profile.membership_plan

        if not current_plan:
            return Response({"success": False})

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


class PaymentPlanResumeCancel(StripeAPIView):
    """
    post: attempts to cancel a member's membership plan.
    """

    def post(self, request, resume):
        current_plan = request.user.profile.membership_plan
        resume = True if resume == "resume" else False

        if not current_plan:
            request.user.log_event(
                "Member tried to modify nonexistant membership plan.", "stripe"
            )
            return Response(
                {"success": False, "message": "paymentPlan.notExists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        else:
            # this will modify the subscription to automatically cancel at the end of the current payment period
            if resume:
                modified_subscription = stripe.Subscription.modify(
                    request.user.profile.stripe_subscription_id,
                    cancel_at_period_end=False,
                )

                if modified_subscription.cancel_at_period_end == False:
                    request.user.profile.subscription_status = "active"
                    request.user.profile.save()
                    subject = f"{request.user.get_full_name()} resumed their about to cancel membership plan."
                    send_email_to_admin(
                        subject=subject,
                        template_vars={
                            "title": subject,
                            "message": subject,
                        },
                        user=request.user,
                        reply_to=request.user.email,
                    )
                    request.user.log_event(
                        subject,
                        "stripe",
                    )
                    return Response({"success": True})

                else:
                    subject = f"{request.user.get_full_name()} tried to resume their about to cancel membership plan but it failed."
                    send_email_to_admin(
                        subject=subject,
                        template_vars={
                            "title": subject,
                            "message": subject,
                        },
                        user=request.user,
                        reply_to=request.user.email,
                    )
                    request.user.log_event(
                        subject,
                        "stripe",
                    )

            else:
                modified_subscription = stripe.Subscription.modify(
                    request.user.profile.stripe_subscription_id,
                    cancel_at_period_end=True,
                )

                if modified_subscription.cancel_at_period_end == True:
                    request.user.profile.subscription_status = "cancelling"
                    request.user.profile.save()
                    subject = f"{request.user.get_full_name()} requested to cancel their membership plan."

                    send_email_to_admin(
                        subject=subject,
                        template_vars={
                            "title": subject,
                            "message": subject,
                        },
                        user=request.user,
                        reply_to=request.user.email,
                    )
                    request.user.log_event(
                        subject,
                        "stripe",
                    )
                    return Response({"success": True})

                else:
                    subject = f"{request.user.get_full_name()} requested to cancel their membership plan but it failed."
                    send_email_to_admin(
                        subject=subject,
                        template_vars={
                            "title": subject,
                            "message": subject,
                        },
                        user=request.user,
                        reply_to=request.user.email,
                    )
                    request.user.log_event(
                        subject,
                        "stripe",
                    )

            return Response({"success": False})


class StripeWebhook(StripeAPIView):
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
                capture_exception(e)
                return Response({"error": "Error validating Stripe signature."})

            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event["type"]
        else:
            data = request_data["data"]
            event_type = request_data["type"]

        data = data["object"]
        try:
            member_profile = Profile.objects.get(stripe_customer_id=data["customer"])

        except Profile.DoesNotExist as e:
            capture_exception(e)
            return Response()

        # Just in case the linked Stripe account also processes other payments we should just ignore a non existent
        # customer.
        if not member_profile:
            return Response()

        if event_type == "invoice.paid":
            invoice_status = data["status"]

            member_profile.user.log_event("Membership payment received", "stripe")

            # If they aren't an active member, are allowed to signup, and have paid the invoice
            # then lets activate their account (this could be a new OR returning member)
            if (
                member_profile.state != "active"
                and member_profile.can_signup()["success"]
                and invoice_status == "paid"
            ):
                subject = "Your payment was successful."
                message = (
                    "Thanks for making a membership payment using our online payment system. "
                    "You've already met all of the requirements for activating your site access. Please check "
                    "for another email message confirming this was successful."
                )
                member_profile.user.email_notification(subject, message)

                # set the subscription status to active
                member_profile.subscription_status = "active"
                member_profile.save()

                # activate their access card
                member_profile.activate()
                member_profile.user.email_enable_member()

                member_profile.user.log_event(
                    "Activated membership because member met all requirements.",
                    "stripe",
                )

            # If they aren't an active member, are NOT allowed to signup, and have paid the invoice
            # then we need to let them know and mark the subscription as active
            # (this could be a new OR returning member that's been too long since induction etc.)
            elif member_profile.state != "active" and invoice_status == "paid":
                subject = "Your payment was successful."
                message = (
                    "Thanks for making a membership payment using our online payment system. "
                    "You haven't yet met all of the requirements for automatically activating your site access. "
                    "You'll receive confirmation that your site access is enabled soon, or we'll be in touch. "
                    "If you don't hear from us soon or require assistance, please contact us."
                )
                member_profile.user.email_notification(subject, message)

                member_profile.subscription_status = "active"
                member_profile.save()

                # if this is a returning member then send the exec an email (new members have
                # already had this sent)
                if member_profile.state != "noob":
                    subject = "Action Required: Verify returning member"
                    title = subject
                    message = (
                        "An existing member (or someone who clicked 'skip signup I just want an account') "
                        "has setup a membership subscription. You must now decide whether to enable their site access."
                    )
                    send_email_to_admin(
                        subject, title, message, reply_to=member_profile.user.email
                    )

                member_profile.user.log_event(
                    "Did not activate membership because member did not meet all requirements.",
                    "stripe",
                )

            # in all other instances, we don't care about a paid invoice and can ignore it

        if event_type == "invoice.payment_failed":
            subject = "Your membership payment failed"
            message = (
                "Hi there, we tried to collect your membership payment but "
                "weren't successful. Please update your billing method or contact "
                "us if you need more time. We'll try again a few times, but if we're unable to "
                "collect your payment soon, your membership may be cancelled."
            )

            member_profile.user.email_notification(subject, message)
            member_profile.user.log_event("Membership payment failed", "stripe")

        if event_type == "customer.subscription.deleted":
            # the subscription was deleted, so deactivate the member
            subject = "Your membership has been cancelled"
            message = (
                "You will receive another email shortly confirming that your access has been deactivated. Your "
                "membership was cancelled because we couldn't collect your payment, or you chose not to renew it."
            )

            member_profile.deactivate()
            member_profile.user.email_notification(subject, message)

            member_profile.membership_plan = None
            member_profile.stripe_subscription_id = None
            member_profile.subscription_status = "inactive"
            member_profile.save()

            member_profile.user.log_event(
                "Membership was cancelled due to Stripe subscription ending", "stripe"
            )

            subject = f"The membership for {member_profile.get_full_name()} was just cancelled"
            title = subject
            message = (
                f"The Stripe subscription for {member_profile.get_full_name()} ended, so their membership has "
                f"been cancelled. Their site access has been turned off."
            )
            template_vars = {"title": title, "message": message}

            send_email_to_admin(
                subject,
                template_vars=template_vars,
                reply_to=member_profile.user.email,
                user=member_profile.user,
            )

        return Response()
