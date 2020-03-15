from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401
from access.models import DoorLog, InterlockLog
from profile.models import User
from constance import config
from membermatters.helpers import log_user_event
from profile.emailhelpers import send_single_email
import requests
import json


@require_GET
@login_required_401
def api_get_swipes(request):
    """
    This method returns the 50 most recent swipes on each door and interlock.
    :param request:
    :return:
    """
    recent_doors = DoorLog.objects.all().order_by("date")[::-1][:50]
    recent_interlocks = InterlockLog.objects.all().order_by("last_heartbeat")[::-1][:50]

    doors = []
    interlocks = []

    for door in recent_doors:
        doors.append({"name": door.door.name, "date": door.date, "user": door.user.profile.get_full_name()})

    for interlock in recent_interlocks:
        user_off = None

        if interlock.user_off:
            user_off = interlock.user_off.profile.get_full_name()

        interlocks.append({
            "name": interlock.interlock.name,
            "sessionStart": interlock.first_heartbeat,
            "sessionEnd": interlock.last_heartbeat,
            "sessionComplete": interlock.session_complete,
            "userOn": interlock.user.profile.get_full_name(),
            "userOff": user_off,
        })

    return JsonResponse({"doors": doors, "interlocks": interlocks}, safe=False)


@require_GET
@login_required_401
def api_get_lastseen(request):
    """
    This method returns when each user was last seen (ie when they last swiped).
    :param request:
    :return:
    """
    last_seen = list()
    members = User.objects.all().order_by('-profile__last_seen')

    for member in members:
        if not member.profile.state == "active":
            continue

        if member.profile.last_seen is not None:
            append_object = {
                    "user": member.profile.get_full_name(), "never": False,
                    "date": member.profile.last_seen
                }
            last_seen.append(append_object)

        else:
            last_seen.append({"user": member.profile.get_full_name(), "never": True})

    return JsonResponse(last_seen, safe=False)


@require_POST
# @login_required_401
def api_submit_issue(request):
    body = json.loads(request.body)
    title = body["title"]
    description = request.user.profile.get_full_name() + ": " + body["description"]

    if not (title and description):
        return HttpResponseBadRequest()

    use_trello = config.ENABLE_TRELLO_INTEGRATION
    trello_key = config.TRELLO_API_KEY
    trello_token = config.TRELLO_API_TOKEN
    trello_id_list = config.TRELLO_ID_LIST

    if use_trello:
        url = "https://api.trello.com/1/cards"

        querystring = {"name": title, "desc": description, "pos": "top",
                       "idList": trello_id_list,
                       "keepFromSource": "all", "key": trello_key, "token": trello_token}

        response = requests.request("POST", url, params=querystring)

        if response.status_code == 200:
            log_user_event(request.user, "Submitted issue: " + title + " Content: " + description,
                           "generic")

            return JsonResponse({"success": True, "url": response.json()["shortUrl"]})

        else:
            return JsonResponse({"success": False})

    # if Trello isn't configured, use email instead
    else:
        subject = f"{request.user.profile.get_full_name()} submitted an issue ({title})"

        try:
            if send_single_email(request.user, config.EMAIL_ADMIN, subject, subject, description):
                return JsonResponse({"success": True})

            else:
                return JsonResponse({"success": False})

        except:
            return JsonResponse({"success": False})
