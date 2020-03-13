from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401
from access.models import DoorLog, InterlockLog
from profile.models import User


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
