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
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401
from django.views.decorators.csrf import csrf_exempt
from constance import config
import json
from django.utils.timezone import make_aware
import datetime
from pytz import UTC as utc
from group.models import Group

from rest_framework import status, permissions, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import Kiosk, SiteSession
from django.core import serializers


class GetConfig(APIView):
    """
    get: This method returns the site config used to customise the front end.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        groups = list(Group.objects.filter(hidden=False).values())

        features = {
            "stripe": {
                "enabled": len(config.STRIPE_PUBLISHABLE_KEY) > 0,
                "memberBucksIntegration": config.ENABLE_MEMBERBUCKS_STRIPE_INTEGRATION,
            },
            "trelloIntegration": config.ENABLE_TRELLO_INTEGRATION,
        }

        keys = {"stripePublishableKey": config.STRIPE_PUBLISHABLE_KEY}

        response = {
            "loggedIn": request.user.is_authenticated,
            "general": {
                "siteName": config.SITE_NAME,
                "siteOwner": config.SITE_OWNER,
                "entityType": config.ENTITY_TYPE,
            },
            "images": {
                "siteLogo": config.SITE_LOGO,
                "siteFavicon": config.SITE_FAVICON,
            },
            "homepageCards": json.loads(config.HOME_PAGE_CARDS),
            "webcamLinks": json.loads(config.WEBCAM_PAGE_URLS),
            "groups": groups,
            "keys": keys,
            "features": features,
        }

        return Response(response)


class Login(APIView):
    """
    WEB_ONLY

    post: Attempts to authenticate a user then logs them in if successful.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)

        body = json.loads(request.body.decode("utf-8"))

        if body.get("email") is None or body.get("password") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=body.get("email"), password=body.get("password"))

        # correct login details
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        else:
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

        if body.get("cardId") is None and body.get("kioskId") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Profile.objects.get(rfid=body.get("cardId")).user

        except Profile.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        kiosk = Kiosk.objects.get(kiosk_id=body.get("kioskId"))

        if not kiosk.authorised:
            return Response(status=status.HTTP_403_FORBIDDEN)

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
def api_reset_password(request):
    """
    WEB_ONLY

    post: Handles the various stages of the password reset flow.
    """
    body = json.loads(request.body)

    # If we get a reset token and no password, the token is being validated
    if body.get("token") and not body.get("password"):
        user = User.objects.get(password_reset_key=body.get("token"))

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
                    "savedCard": {
                        "last4": p.stripe_card_last_digits,
                        "expiry": p.stripe_card_expiry,
                    },
                },
            },
            "permissions": {
                "admin": user.is_admin
                #     "generateInvoice": p.can_generate_invoice,
                #     "adminOfGroups": list(p.can_manage_group.values()),
                #     "groups": p.can_manage_groups,
                #     "addGroup": p.can_add_group,
                #     "interlocks": p.can_manage_interlocks,
                #     "doors": p.can_manage_doors,
                #     "seeMemberLogs": p.can_see_members_logs,
                #     "seeMemberbucks": p.can_see_members_memberbucks,
                #     "seeMemberPersonalDetails": p.can_see_members_personal_details,
                #     "disableMembers": p.can_disable_members,
                #     "manageAccess": p.can_manage_access,
            },
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

        new_user = User.objects.create(
            email=body.get("email").lower(), password=body.get("password")
        )
        profile = Profile.objects.create(
            user=new_user,
            member_type_id=2,
            first_name=body.get("firstName"),
            last_name=body.get("lastName"),
            screen_name=body.get("screenName"),
            phone=body.get("mobile"),
        )

        # for group in data.
        for group in body.get("groups"):
            profile.groups.add(Group.objects.get(id=group["id"]))
        profile.save()

        profile.email_profile_to(config.EMAIL_ADMIN)

        new_user.email_link(
            f"{config.SITE_OWNER} New Member Signup - Action Required",
            "Next Step: Register for an Induction",
            "Important. Please read this email for details on how to "
            "register for an induction.",
            "Hi {profile.first_name}, thanks for signing up! The next step to becoming a fully "
            "fledged member is to book in for an induction. During this "
            "induction we will go over the basic safety and operational "
            f"aspects of {config.SITE_OWNER}. To book in, click the link below.",
            f"{config.INDUCTION_URL}",
            "Register for Induction",
        )

        # for convenience, we should now log the user in
        login(request, new_user)

        return Response()
