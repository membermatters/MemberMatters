from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401
from constance import config
from profile.models import User, Profile
import json
import time
import datetime
from pytz import UTC as utc


@require_GET
def api_get_config(request):
    """
    This method returns the site config used to customise the front end.
    :param request:
    :return:
    """
    response = {
        "loggedIn": request.user.is_authenticated,
        "general": {
            "siteName": config.SITE_NAME,
            "siteOwner": config.SITE_OWNER,
            "entityType": config.ENTITY_TYPE,
        },
        "images": {"siteLogo": config.SITE_LOGO, "siteFavicon": config.SITE_FAVICON,},
        "homepageCards": json.loads(config.HOME_PAGE_CARDS),
        "webcamLinks": json.loads(config.WEBCAM_PAGE_URLS),
    }
    return JsonResponse(response)


@require_POST
def api_login(request):
    """
    Attempts to authenticate a user then logs them in if successful.
    :param request:
    :return:
    """
    response_success = {"success": True}

    response_failure = {"success": False}

    if request.user.is_authenticated:
        return JsonResponse(response_success)

    body = json.loads(request.body.decode("utf-8"))

    if body.get("email") is None or body.get("password") is None:
        return HttpResponseBadRequest()

    user = authenticate(username=body.get("email"), password=body.get("password"))

    # correct login details
    if user is not None:
        login(request, user)
        return JsonResponse(response_success)

    else:
        return JsonResponse(response_failure)


@require_POST
@login_required_401
def api_logout(request):
    """
    Ends the user's session and logs them out.
    :param request:
    :return:
    """
    logout(request)

    return JsonResponse({"success": True})


@require_POST
def api_reset_password(request):
    """
    Handles the various stages of the password reset flow.
    :param request:
    :return:
    """
    # This will help mitigate any brute force attempts on this API
    time.sleep(2)
    body = json.loads(request.body)

    # If we get a reset token and no email, the token is being validated
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


@login_required_401
def api_profile(request):
    """
    Gets or updates the user profile object.
    :param request:
    :return:
    """

    if request.method == "GET":
        p = request.user.profile

        response = {
            "email": request.user.email,
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
            "permissions": {
                "generateInvoice": p.can_generate_invoice,
                "adminOfGroups": list(p.can_manage_group.values()),
                "manageGroups": p.can_manage_groups,
                "addGroup": p.can_add_group,
                "manageInterlocks": p.can_manage_interlocks,
                "manageDoors": p.can_manage_doors,
                "seeMemberLogs": p.can_see_members_logs,
                "seeMemberbucks": p.can_see_members_memberbucks,
                "seeMemberPersonalDetails": p.can_see_members_personal_details,
                "disableMembers": p.can_disable_members,
                "manageAccess": p.can_manage_access,
            },
        }

        return JsonResponse(response)

    elif request.method == "PUT":
        p = request.user.profile
        body = json.loads(request.body)

        request.user.email = body.get("email")
        p.first_name = body.get("firstName")
        p.last_name = body.get("lastName")
        p.phone = body.get("phone")
        p.screen_name = body.get("screenName")

        request.user.save()
        p.save()

        return JsonResponse({"success": True})

    else:
        return HttpResponseBadRequest()
