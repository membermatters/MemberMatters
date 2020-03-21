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
    This method returns the site config used by the front end.
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
        "images": {
            "siteLogo": config.SITE_LOGO,
            "siteFavicon": config.SITE_FAVICON,
        },
        "homepageCards": json.loads(config.HOME_PAGE_CARDS),
        "webcamLinks": json.loads(config.WEBCAM_PAGE_URLS),
    }
    return JsonResponse(response)


@require_POST
def api_login(request):
    response_success = {
        "success": True
    }

    response_failure = {
        "success": False
    }

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
    logout(request)

    return JsonResponse({"success": True})


@require_POST
def api_reset_password(request):
    # This will help mitigate any brute force attempts on this API
    time.sleep(2)
    body = json.loads(request.body)

    # If we get a reset token and no email, the token is being validated
    if body.get('token') and not body.get('password'):
        user = User.objects.get(password_reset_key=body.get('token'))

        if user and utc.localize(datetime.datetime.now()) < user.password_reset_expire:
            return JsonResponse({"success": True})

        else:
            user.password_reset_key = None
            user.password_reset_expire = None
            user.save()
            return JsonResponse({"success": False})

    # If we get a reset token and email, the password should be reset
    if body.get('token') and body.get('password'):
        user = User.objects.get(password_reset_key=body.get('token'))

        if user and utc.localize(datetime.datetime.now()) < user.password_reset_expire:
            user.set_password(body.get('password'))
            user.password_reset_key = None
            user.password_reset_expire = None
            user.save()

            if user:
                return JsonResponse({"success": True})

        return JsonResponse({"success": False})

    else:
        try:
            user = User.objects.get(email=body.get('email'))
            user.reset_password()
            return JsonResponse({'success': True})

        except ObjectDoesNotExist:
            return JsonResponse({'success': False})


@require_GET
@login_required_401
def api_get_profile(request):
    user = request.user

    profile = {
        "fullName": user.profile.get_full_name(),
        "screenName": user.profile.screen_name,
        "memberStatus": user.profile.state,
    }

    return JsonResponse(profile)
