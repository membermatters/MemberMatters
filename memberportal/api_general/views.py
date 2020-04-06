from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
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
import time
import datetime
from pytz import UTC as utc
from group.models import Group

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class GetConfig(APIView):
    """
    get: This method returns the site config used to customise the front end.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        groups = list(Group.objects.filter(hidden=False).values())

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
        }

        return Response(response)


class DjangoModelPermissionsWithRead(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class UserCreate(APIView):
    """
    post: Creates a new user account.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # TODO: implement sign up endpoint

        return Response("", status=status.HTTP_501_NOT_IMPLEMENTED)


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


class Logout(APIView):
    """
    WEB_ONLY

    post: Ends the user's session and logs them out.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        logout(request)

        return Response()


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
                "savedCard": {
                    "last4": p.stripe_card_last_digits,
                    "expiry": p.stripe_card_expiry,
                },
                "lastMemberbucksPurchase": p.last_memberbucks_purchase,
                "memberbucksBalance": p.memberbucks_balance,
            },
            # "permissions": {
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
            # },
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
