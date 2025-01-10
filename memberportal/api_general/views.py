import sentry_sdk
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
import logging
from constance import config
import json
from django.utils.timezone import make_aware
import datetime
from pytz import UTC as utc
from profile.models import User, Profile

from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Kiosk, SiteSession, EmailVerificationToken
from services.discord import post_kiosk_swipe_to_discord
from services.docuseal import create_submission_for_subscription
from services.docuseal import get_docuseal_state
import base64
from urllib.parse import parse_qs, urlencode
import hmac
import hashlib

logger = logging.getLogger("general")


class GetConfig(APIView):
    """
    get: This method returns the site config used to customise the front end.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        features = {
            "memberbucks_topup_options": json.loads(
                config.STRIPE_MEMBERBUCKS_TOPUP_OPTIONS
            ),
            "enableProxyVoting": config.ENABLE_PROXY_VOTING,
            "enableStripe": config.ENABLE_STRIPE
            and len(config.STRIPE_PUBLISHABLE_KEY) > 0
            and len(config.STRIPE_SECRET_KEY) > 0,
            "enableMembershipPayments": config.ENABLE_STRIPE
            and config.ENABLE_STRIPE_MEMBERSHIP_PAYMENTS,
            "enableMemberBucks": config.ENABLE_MEMBERBUCKS,
            "signup": {
                "inductionLink": config.INDUCTION_ENROL_LINK,
                "requireAccessCard": config.REQUIRE_ACCESS_CARD,
                "postInductionUrl": config.POST_INDUCTION_URL,
                "collectVehicleRegistrationPlate": config.COLLECT_VEHICLE_REGISTRATION_PLATE,
            },
            "enableWebcams": config.ENABLE_WEBCAMS,
            "siteBanner": config.SITE_BANNER,
            "enableSiteSignIn": config.ENABLE_PORTAL_SITE_SIGN_IN,
            "enableMembersOnSite": config.ENABLE_PORTAL_MEMBERS_ON_SITE,
            "sms": {
                "enable": config.SMS_ENABLE,
                "senderId": config.SMS_SENDER_ID,
                "footer": config.SMS_FOOTER,
            },
            "enableStatsPage": config.ENABLE_STATS_PAGE,
        }

        keys = {"stripePublishableKey": config.STRIPE_PUBLISHABLE_KEY}

        with open("../package.json") as f:
            package = json.load(f)
            version = package.get("version")

        try:
            homepage_cards = json.loads(config.HOME_PAGE_CARDS)
        except:
            homepage_cards = [
                {
                    "title": "Error loading configuration",
                    "description": "There was an error loading the home page cards configuration. Please try re-saving the configuration in the admin panel.",
                    "icon": "mdi-alert",
                    "url": "#",
                    "btn_text": "",
                },
            ]

        try:
            webcam_links = json.loads(config.WEBCAM_PAGE_URLS)
        except:
            webcam_links = [
                ["Error Loading Webcam Configuration", ""],
            ]

        response = {
            "version": version,
            "loggedIn": request.user.is_authenticated,
            "general": {
                "siteName": config.SITE_NAME,
                "siteOwner": config.SITE_OWNER,
                "siteLocaleCurrency": config.SITE_LOCALE_CURRENCY,
            },
            "contact": {
                "admin": config.EMAIL_ADMIN,
                "sysadmin": config.EMAIL_SYSADMIN,
                "address": config.SITE_MAIL_ADDRESS,
            },
            "images": {
                "siteLogo": config.SITE_LOGO,
                "statsCard": config.STATS_CARD_IMAGE,
                "siteFavicon": config.SITE_FAVICON,
                "menuBackground": config.MENU_BACKGROUND,
            },
            "theme": {
                "themePrimary": config.THEME_PRIMARY,
                "themeToolbar": config.THEME_TOOLBAR,
                "themeAccent": config.THEME_ACCENT,
            },
            "homepageCards": homepage_cards,
            "webcamLinks": webcam_links,
            "keys": keys,
            "features": features,
            "analyticsId": config.GOOGLE_ANALYTICS_MEASUREMENT_ID,
            "sentryDSN": config.SENTRY_DSN_FRONTEND,
        }

        return Response(response)


class Login(APIView):
    """
    WEB_ONLY

    post: Attempts to authenticate a user then logs them in if successful.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        body = request.data
        discourse_nonce = None
        discourse_redirect = None
        discourse_login = False
        secret = config.DISCOURSE_SSO_PROTOCOL_SECRET_KEY.encode("utf-8")

        if body.get("sso") is not None:
            if config.ENABLE_DISCOURSE_SSO_PROTOCOL:
                sso_data = body.get("sso")
                computed_signature = hmac.new(
                    secret, sso_data["sso"].encode("utf-8"), digestmod=hashlib.sha256
                ).hexdigest()

                sso_payload = parse_qs(base64.b64decode(sso_data["sso"]))
                sig = sso_data["sig"]

                if computed_signature == sig:
                    discourse_nonce = sso_payload[b"nonce"][0].decode("utf-8")
                    discourse_redirect = sso_payload[b"return_sso_url"][0].decode(
                        "utf-8"
                    )
                    discourse_login = True

                else:
                    # if the sig doesn't match then exit
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                # if sso is disabled then exit
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            if discourse_login:
                payload = {
                    "nonce": discourse_nonce,
                    "email": request.user.email,
                    "external_id": request.user.id,
                    "username": request.user.profile.screen_name,
                    "name": request.user.profile.get_full_name(),
                }
                payload = base64.b64encode(urlencode(payload).encode("utf-8"))
                computed_signature = hmac.new(
                    secret, payload, digestmod=hashlib.sha256
                ).hexdigest()

                return Response(
                    {
                        "redirect": f"{discourse_redirect}?sso={payload.decode('utf-8')}&sig={computed_signature}"
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(status=status.HTTP_200_OK)

        if body.get("email") is None or body.get("password") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=body.get("email"), password=body.get("password"))

        # correct login details
        if user is not None:
            # if their email is verified
            if user.email_verified:
                login(request, user)

                if discourse_login:
                    payload = {
                        "nonce": discourse_nonce,
                        "email": user.email,
                        "external_id": user.id,
                        "username": user.profile.screen_name,
                        "name": user.profile.get_full_name(),
                    }
                    payload = base64.b64encode(urlencode(payload).encode("utf-8"))
                    computed_signature = hmac.new(
                        secret, payload, digestmod=hashlib.sha256
                    ).hexdigest()

                    return Response(
                        {
                            "redirect": f"{discourse_redirect}?sso={payload.decode('utf-8')}&sig={computed_signature}"
                        },
                        status=status.HTTP_200_OK,
                    )

                else:
                    return Response(status=status.HTTP_200_OK)

            else:
                new_token = EmailVerificationToken.objects.create(user=user)

                url = f"{config.SITE_URL}/profile/email/{new_token.verification_token}/verify/"
                new_token.user.email_link(
                    "Action Required: Verify Email",
                    "Verify Email",
                    "Please verify your email address to activate your account.",
                    url,
                    "Verify Now",
                )

                return Response(
                    {"message": "loginCard.emailNotVerified"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        logger.info("user was None")
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={})


class LoginKiosk(APIView):
    """
    KIOSK_ONLY

    post: Attempts to authenticate a user then logs them in if successful.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)

        body = json.loads(request.body.decode("utf-8"))

        if body.get("cardId") is None or body.get("kioskId") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            kiosk = Kiosk.objects.get(kiosk_id=body.get("kioskId"))

        except Kiosk.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not kiosk.authorised:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            user = Profile.objects.get(rfid=body.get("cardId")).user

        except Profile.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not user.email_verified:
            return Response(
                {"message": "error.emailNotVerified"}, status=status.HTTP_403_FORBIDDEN
            )

        # rfid matches a user so log them in
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    """
    WEB_ONLY, KIOSK_ONLY

    post: Ends the user's session and logs them out.
    """

    def post(self, request):
        logout(request)

        return Response({"success": True})


class ResetPassword(APIView):
    """
    post: Handles the various stages of the password reset flow.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        body = request.data

        # If we get a reset token and no password, the token is being validated
        if body.get("token") and not body.get("password"):
            try:
                user = User.objects.get(password_reset_key=body.get("token"))

            except User.DoesNotExist:
                return Response({"success": False})

            if (
                user
                and utc.localize(datetime.datetime.now()) < user.password_reset_expire
            ):
                return Response({"success": True})

            else:
                user.password_reset_key = None
                user.password_reset_expire = None
                user.save()
                return Response({"success": False})

        # If we get a reset token and email, the password should be reset
        if body.get("token") and body.get("password"):
            user = User.objects.get(password_reset_key=body.get("token"))

            if (
                user
                and utc.localize(datetime.datetime.now()) < user.password_reset_expire
            ):
                user.set_password(body.get("password"))
                user.password_reset_key = None
                user.password_reset_expire = None
                user.save()

                if user:
                    return Response({"success": True})

            return Response({"success": False})

        else:
            try:
                user = User.objects.get(email=body.get("email"))
                user.reset_password()
                return Response({"success": True})

            except:
                return Response({"success": False})


class ProfileDetail(generics.GenericAPIView):
    """
    get: Gets the user profile object.
    put: Updates the user profile object.
    """

    def get(self, request):
        p = request.user.profile
        user = request.user

        response = {
            "id": user.id,
            "email": user.email,
            "fullName": p.get_full_name(),
            "firstName": p.first_name,
            "lastName": p.last_name,
            "screenName": p.screen_name,
            "phone": p.phone,
            "memberStatus": p.state,
            "vehicleRegistrationPlate": p.vehicle_registration_plate,
            "lastInduction": p.last_induction,
            "lastSeen": p.last_seen,
            "firstJoined": p.created,
            "profileUpdateRequired": p.must_update_profile,
            "financial": {
                "memberBucks": {
                    "lastPurchase": p.last_memberbucks_purchase,
                    "balance": p.memberbucks_balance,
                    "savedCard": {
                        "last4": p.stripe_card_last_digits,
                        "expiry": p.stripe_card_expiry,
                    },
                },
                "membershipPlan": (
                    p.membership_plan.get_object() if p.membership_plan else None
                ),
                "membershipTier": (
                    p.membership_plan.member_tier.get_object()
                    if p.membership_plan
                    else None if p.membership_plan else None
                ),
                "subscriptionState": p.subscription_status,
            },
            "permissions": {"staff": user.is_staff},
        }
        # append induction link(s) if user has not been inducted
        response["inductionLink"] = []
        if p.last_induction is None:
            if p.last_induction is None:
                if config.MOODLE_INDUCTION_ENABLED or config.CANVAS_INDUCTION_ENABLED:
                    response["inductionLink"].append(config.INDUCTION_ENROL_LINK)
                if config.ENABLE_DOCUSEAL_INTEGRATION:
                    # TODO the following removed with a webhook callback from DocuSeal on submission signing
                    state = get_docuseal_state(p)
                    if state == "complete":
                        # in the event our induction process is *just* DocuSeal and the doc is signed, update unduction status
                        if not (config.MOODLE_INDUCTION_ENABLED or config.CANVAS_INDUCTION_ENABLED):
                            p.update_last_induction()
                            response["lastInduction"] = p.last_induction
                    elif state != "declined":
                        response["inductionLink"].append(p.memberdoc_url)
                    # remainder state is "declined"

        return Response(response)

    def put(self, request):
        p = request.user.profile
        body = json.loads(request.body)
        email = body.get("email").lower()
        screen_name = body.get("screenName").lower()

        # check if email is specified
        if not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check if email is already in use
        if User.objects.filter(email=email).exists() and email != request.user.email:
            return Response(
                {"message": "error.accountAlreadyExists"},
                status=status.HTTP_409_CONFLICT,
            )

        # check if screen name is already in use
        if (
            Profile.objects.filter(screen_name=screen_name).exists()
            and screen_name != request.user.profile.screen_name
        ):
            return Response(
                {"message": "error.screenNameAlreadyExists"},
                status=status.HTTP_409_CONFLICT,
            )

        request.user.email = body.get("email")
        p.first_name = body.get("firstName")
        p.last_name = body.get("lastName")
        p.phone = body.get("phone")
        p.screen_name = body.get("screenName")
        p.vehicle_registration_plate = body.get("vehicleRegistrationPlate")

        request.user.save()
        p.save()

        return Response({"success": True})


class ApiPassword(APIView):
    """
    put: Change the user's password.
    """

    def put(self, request):
        user = request.user
        body = json.loads(request.body)
        current = body.get("current")
        new = body.get("new")

        if user.check_password(current):
            user.set_password(new)
            user.save()

            return Response({"success": True})

        return Response(status=status.HTTP_403_FORBIDDEN)


class DigitalId(APIView):
    """
    get: retrieves the user's digital id token.
    """

    def get(self, request):
        return Response(
            {"success": True, "token": request.user.profile.generate_digital_id_token()}
        )


class Kiosks(APIView):
    """
    get: retrieves a list of all kiosks.
    post: creates a new kiosk.
    put: update an existing kiosk.
    delete: delete an existing kiosk.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if not request.user.is_authenticated and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        kiosks = Kiosk.objects.all()

        def get_kiosk(kiosk):
            return {
                "id": kiosk.id,
                "name": kiosk.name,
                "kioskId": kiosk.kiosk_id,
                "kioskIp": kiosk.ip_address,
                "lastSeen": kiosk.last_seen,
                "playTheme": kiosk.play_theme,
                "authorised": kiosk.authorised,
            }

        return Response(list(map(get_kiosk, kiosks)))

    def put(self, request, id=None):
        body = request.data

        try:
            if id:
                kiosk = Kiosk.objects.get(id=id)

                kiosk.ip_address = request.META.get(
                    "HTTP_X_REAL_IP", request.META.get("REMOTE_ADDR")
                )
                kiosk.checkin()
                if not request.user.is_authenticated and not request.user.is_staff:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                kiosk = Kiosk.objects.get(kiosk_id=body.get("kioskId"))

        except Kiosk.DoesNotExist:
            kiosk = Kiosk.objects.create(
                last_seen=make_aware(datetime.datetime.now()),
                kiosk_id=body.get("kioskId"),
                name=body.get("kioskId"),
                play_theme=False,
            )

        if request.user.is_authenticated and request.user.is_staff:
            if body.get("playTheme"):
                kiosk.play_theme = body.get("playTheme")

            if body.get("name"):
                kiosk.name = body.get("name")

            if body.get("authorised") is not None:
                kiosk.authorised = body.get("authorised")

        kiosk.save()

        return Response()

    def delete(self, request, id):
        if not request.user.is_authenticated and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        kiosk = Kiosk.objects.get(id=id)
        kiosk.delete()

        return Response()


class SiteSignIn(APIView):
    """
    post: sign a member in.
    """

    def post(self, request):
        body = request.data
        guests = body.get("guests")

        SiteSession.objects.create(user=request.user, guests=guests)
        post_kiosk_swipe_to_discord(request.user.profile.get_full_name(), True)

        for door in request.user.profile.doors.all():
            door.sync()

        for interlock in request.user.profile.interlocks.all():
            interlock.sync()

        return Response()


class SiteSignOut(APIView):
    """
    put: sign a member out.
    """

    def put(self, request):
        sessions = (
            SiteSession.objects.filter(user=request.user)
            .filter(signout_date__isnull=True)
            .all()
        )
        for session in sessions:
            session.signout()
        post_kiosk_swipe_to_discord(request.user.profile.get_full_name(), False)

        for door in request.user.profile.doors.all():
            door.sync()

        for interlock in request.user.profile.interlocks.all():
            interlock.sync()

        return Response()


class UserSiteSession(APIView):
    """
    get: checks if the member is signed into the site.
    """

    def get(self, request):
        sessions = SiteSession.objects.filter(
            user=request.user, signout_date=None
        ).order_by("-signin_date")

        return Response(sessions.values()[0] if len(sessions) else False)


class LoggedIn(APIView):
    """
    get: checks if the member is logged into the portal.
    """

    def get(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class Register(APIView):
    """
    post: registers a new member.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        body = request.data

        if User.objects.filter(email=body.get("email").lower()).exists():
            return Response(
                {"message": "error.accountAlreadyExists"},
                status=status.HTTP_409_CONFLICT,
            )

        if Profile.objects.filter(screen_name=body.get("screenName").lower()).exists():
            return Response(
                {"message": "error.screenNameAlreadyExists"},
                status=status.HTTP_409_CONFLICT,
            )

        new_user = User.objects.create(
            email=body.get("email").lower(),
            email_verified=False,
        )

        new_user.set_password(body.get("password"))
        new_user.save()

        profile = Profile.objects.create(
            user=new_user,
            first_name=body.get("firstName"),
            last_name=body.get("lastName"),
            screen_name=body.get("screenName"),
            phone=body.get("mobile"),
            vehicle_registration_plate=body.get("vehicleRegistrationPlate"),
        )

        profile.save()

        if config.ENABLE_DOCUSEAL_INTEGRATION:
            create_submission_for_subscription(profile)

        verification_token = EmailVerificationToken.objects.create(user=new_user)

        url = f"{config.SITE_URL}/profile/email/{verification_token.verification_token}/verify/"
        verification_token.user.email_link(
            "Action Required: Verify Email",
            "Verify Email",
            "Please verify your email address to activate your account.",
            url,
            "Verify Now",
        )

        profile.email_profile_to(config.EMAIL_ADMIN)

        if not config.ENABLE_STRIPE_MEMBERSHIP_PAYMENTS:
            subject = f"Action Required: {config.SITE_OWNER} New Member Signup"
            title = "Next Step: Register for an Induction"
            message = (
                f"Hi {profile.first_name}, thanks for signing up! The next step to becoming a fully "
                "fledged member is to book in for an induction. During this "
                "induction we will go over the basic safety and operational "
                f"aspects of {config.SITE_OWNER}. To book in, click the link below."
            )
            link = config.POST_INDUCTION_URL
            btn_text = "Register for Induction"

            new_user.email_link(subject, title, message, link, btn_text)

        try:
            if config.MAILCHIMP_API_KEY:
                import mailchimp_marketing
                from mailchimp_marketing.api_client import ApiClientError

                client = mailchimp_marketing.Client()
                client.set_config(
                    {
                        "api_key": config.MAILCHIMP_API_KEY,
                        "server": config.MAILCHIMP_SERVER,
                    }
                )

                list_id = config.MAILCHIMP_LIST_ID
                merge_fields = {
                    "FNAME": new_user.profile.first_name,
                    "LNAME": new_user.profile.last_name,
                    "PHONE": new_user.profile.phone,
                }

                payload = {
                    "email_address": new_user.email,
                    "email_type": "html",
                    "status": "subscribed",
                    "merge_fields": merge_fields,
                    "vip": False,
                    "tags": [
                        config.MAILCHIMP_TAG,
                    ],
                }
                client.lists.add_list_member(list_id, payload)

        except Exception as e:
            # gracefully catch and move on
            sentry_sdk.capture_exception(e)
            logger.error(e)
            return Response()

        return Response()


class VerifyEmail(APIView):
    """
    post: registers a new member.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, verify_token):
        try:
            verification_token = EmailVerificationToken.objects.get(
                verification_token=verify_token
            )

        except EmailVerificationToken.DoesNotExist:
            return Response(
                {"message": "error.emailVerificationFailed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if utc.localize(
            datetime.datetime.now()
        ) < verification_token.creation_date + datetime.timedelta(hours=24):
            verification_token.user.email_verified = True
            verification_token.user.save()

            # auto log the user in after verifying their email
            login(request, verification_token.user)

            # delete the verification token so it can't be used again
            verification_token.delete()

            return Response()

        else:
            new_token = EmailVerificationToken.objects.create(
                user=verification_token.user
            )

            url = f"{config.SITE_URL}/profile/email/{new_token.verification_token}/verify/"
            new_token.user.email_link(
                "Action Required: Verify Email",
                "Verify Email",
                "Please verify your email address to activate your account.",
                url,
                "Verify Now",
            )

            verification_token.delete()

            return Response(
                {"message": "error.emailVerificationExpired"},
                status=status.HTTP_403_FORBIDDEN,
            )
