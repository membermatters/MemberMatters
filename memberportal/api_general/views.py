from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponse,
)
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from membermatters.decorators import login_required_401
from django.views.decorators.csrf import csrf_exempt
from constance import config
import json
from django.utils.timezone import make_aware
import datetime
from pytz import UTC as utc
from group.models import Group
from profile.models import MemberTypes

from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import Kiosk, SiteSession, EmailVerificationToken
from services.discord import post_kiosk_swipe_to_discord
import base64
from urllib.parse import parse_qs, urlencode
import hmac, hashlib


class GetConfig(APIView):
    """
    get: This method returns the site config used to customise the front end.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        groups = list(Group.objects.filter(hidden=False).values())
        membership_types = list(MemberTypes.objects.values())

        features = {
            "stripe": {
                "enabled": len(config.STRIPE_PUBLISHABLE_KEY) > 0,
                "memberBucksIntegration": config.ENABLE_MEMBERBUCKS_STRIPE_INTEGRATION,
                "memberbucks_topup_options": json.loads(
                    config.STRIPE_MEMBERBUCKS_TOPUP_OPTIONS
                ),
            },
            "trelloIntegration": config.ENABLE_TRELLO_INTEGRATION,
            "inductionLink": config.INDUCTION_ENROL_LINK,
        }

        keys = {"stripePublishableKey": config.STRIPE_PUBLISHABLE_KEY}

        response = {
            "loggedIn": request.user.is_authenticated,
            "general": {
                "siteName": config.SITE_NAME,
                "siteOwner": config.SITE_OWNER,
                "entityType": config.ENTITY_TYPE,
            },
            "contact": {
                "admin": config.EMAIL_ADMIN,
                "sysadmin": config.EMAIL_SYSADMIN,
                "address": config.SITE_MAIL_ADDRESS,
            },
            "images": {
                "siteLogo": config.SITE_LOGO,
                "siteFavicon": config.SITE_FAVICON,
            },
            "homepageCards": json.loads(config.HOME_PAGE_CARDS),
            "webcamLinks": json.loads(config.WEBCAM_PAGE_URLS),
            "groups": groups,
            "maxGroups": config.MAX_GROUPS,
            "memberTypes": membership_types,
            "keys": keys,
            "features": features,
            "analyticsId": config.GOOGLE_ANALYTICS_PROPERTY_ID,
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
                    "Verify Email",
                    "Please verify your email address to activate your account.",
                    url,
                    "Verify Now",
                )

                return Response(
                    {"message": "loginCard.emailNotVerified"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        print("user was None")
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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
            user = Profile.objects.get(rfid=body.get("cardId")).user

        except Profile.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        kiosk = Kiosk.objects.get(kiosk_id=body.get("kioskId"))

        if not kiosk.authorised:
            return Response(status=status.HTTP_403_FORBIDDEN)

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


@csrf_exempt
def Logout(request):
    """
    WEB_ONLY, KIOSK_ONLY

    post: Ends the user's session and logs them out.
    """

    logout(request)

    return HttpResponse()


@require_POST
def ResetPassword(request):
    """
    WEB_ONLY

    post: Handles the various stages of the password reset flow.
    """
    body = json.loads(request.body)

    # If we get a reset token and no password, the token is being validated
    if body.get("token") and not body.get("password"):
        try:
            user = User.objects.get(password_reset_key=body.get("token"))

        except User.DoesNotExist:
            return JsonResponse({"success": False})

        if user and utc.localize(datetime.datetime.now()) < user.password_reset_expire:
            return JsonResponse({"success": True})

        else:
            user.password_reset_key = None
            user.password_reset_expire = None
            user.save()
            return JsonResponse({"success": False})

    # If we get a reset token and email, the password should be reset
    if body.get("token") and body.get("password"):
        user = User.objects.get(password_reset_key=body.get("token"))

        if user and utc.localize(datetime.datetime.now()) < user.password_reset_expire:
            user.set_password(body.get("password"))
            user.password_reset_key = None
            user.password_reset_expire = None
            user.save()

            if user:
                return JsonResponse({"success": True})

        return JsonResponse({"success": False})

    else:
        try:
            user = User.objects.get(email=body.get("email"))
            user.reset_password()
            return JsonResponse({"success": True})

        except ObjectDoesNotExist:
            return JsonResponse({"success": False})


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
            "lastInduction": p.last_induction,
            "lastSeen": p.last_seen,
            "firstJoined": p.created,
            "profileUpdateRequired": p.must_update_profile,
            "groups": list(p.groups.values()),
            "memberLevel": {
                "name": str(p.member_type.name),
                "id": str(p.member_type.id),
            },
            "financial": {
                "xeroAccNumber": p.xero_account_number,
                "memberBucks": {
                    "lastPurchase": p.last_memberbucks_purchase,
                    "balance": p.memberbucks_balance,
                    "savedCard": {
                        "last4": p.stripe_card_last_digits,
                        "expiry": p.stripe_card_expiry,
                    },
                },
                "membershipPlan": p.membership_plan.get_object()
                if p.membership_plan
                else None,
                "membershipTier": p.membership_plan.member_tier.get_object()
                if p.membership_plan
                else None
                if p.membership_plan
                else None,
                "subscriptionState": p.subscription_status,
            },
            "permissions": {"admin": user.is_admin},
        }

        return JsonResponse(response)

    def put(self, request):
        p = request.user.profile
        body = json.loads(request.body)

        request.user.email = body.get("email")
        p.first_name = body.get("firstName")
        p.last_name = body.get("lastName")
        p.phone = body.get("phone")
        p.screen_name = body.get("screenName")
        p.groups.set([])

        for group in body.get("groups"):
            p.groups.add(Group.objects.get(id=group["id"]))

        request.user.save()
        p.save()

        return JsonResponse({"success": True})


@login_required_401
def api_password(request):
    """
    Change the user's password.
    :param request:
    :return:
    """
    if request.method == "PUT":
        user = request.user
        body = json.loads(request.body)
        current = body.get("current")
        new = body.get("new")

        if user.check_password(current):
            user.set_password(new)
            user.save()

            return JsonResponse({"success": True})

        return HttpResponseForbidden()

    return HttpResponseBadRequest


@csrf_exempt
@login_required_401
def api_digital_id(request):
    """
    Get the user's digital ID token.
    """
    if request.method == "GET":
        p = request.user.profile

        return JsonResponse({"success": True, "token": p.generate_digital_id_token()})

    elif request.method == "POST":
        token = json.loads(request.body).get("token")

        valid = Profile.objects.get(digital_id_token=token).validate_digital_id_token(
            token
        )

        return JsonResponse({"success": True, "valid": valid})

    return HttpResponseNotAllowed(["GET", "POST"])


class Kiosks(APIView):
    """
    get: retrieves a list of all kiosks.
    post: creates a new kiosk.
    put: update an existing kiosk.
    delete: delete an existing kiosk.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if not request.user.is_authenticated and not request.user.is_admin:
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
                if not request.user.is_authenticated and not request.user.is_admin:
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

        if request.user.is_authenticated:
            if request.user.is_admin:
                if body.get("playTheme"):
                    kiosk.play_theme = body.get("playTheme")

                if body.get("name"):
                    kiosk.name = body.get("name")

                if body.get("authorised") is not None and request.user.is_admin:
                    kiosk.authorised = body.get("authorised")

        kiosk.save()

        return Response()

    def delete(self, request, id):
        if not request.user.is_authenticated and not request.user.is_admin:
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

        return Response()


class SiteSignOut(APIView):
    """
    put: sign a member out.
    """

    def put(self, request):
        session = SiteSession.objects.filter(user=request.user).order_by(
            "-signin_date"
        )[0]
        session.signout()
        post_kiosk_swipe_to_discord(request.user.profile.get_full_name(), False)

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


class Statistics(APIView):
    """
    get: gets site statistics.
    """

    def get(self, request):
        members = SiteSession.objects.filter(signout_date=None).order_by("-signin_date")
        member_list = []

        for member in members:
            member_list.append(member.user.profile.get_full_name())

        statistics = {"onSite": {"members": member_list, "count": members.count()}}

        return Response(statistics)


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
            member_type_id=config.DEFAULT_MEMBER_TYPE,
            first_name=body.get("firstName"),
            last_name=body.get("lastName"),
            screen_name=body.get("screenName"),
            phone=body.get("mobile"),
        )

        # for group in data.
        for group in body.get("groups"):
            profile.groups.add(Group.objects.get(id=group["id"]))
        profile.save()

        verification_token = EmailVerificationToken.objects.create(user=new_user)

        url = f"{config.SITE_URL}/profile/email/{verification_token.verification_token}/verify/"
        verification_token.user.email_link(
            "Action Required: Verify Email",
            "Verify Email",
            "Verify Email",
            "Please verify your email address to activate your account.",
            url,
            "Verify Now",
        )

        profile.email_profile_to(config.EMAIL_ADMIN)

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
