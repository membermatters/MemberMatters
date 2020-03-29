from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401, staff_required
from .models import Meeting, ProxyVote
import json


@staff_required
@login_required_401
def api_meeting(request):
    """
    This method handles the /api/meetings/ endpoint
    :param request:
    :return:
    """
    if request.method == "GET":
        meetings = Meeting.objects.all()

        def get_attendee(attendee):
            return attendee.profile.get_full_name()

        def get_proxy(proxy):
            return {
                "name": proxy.user.profile.get_full_name(),
                "proxyName": proxy.proxy_user.profile.get_full_name(),
                "date": proxy.created_date,
            }

        def get_meeting(meeting):
            return {
                "id": meeting.id,
                "date": meeting.date,
                "chair": meeting.chair,
                "type": meeting.get_type(),
                "attendeeCount": meeting.attendees.count(),
                "attendees": list(map(get_attendee, meeting.attendees.all())),
                "proxyList": list(map(get_proxy, meeting.proxyvote_set.all())),
            }

        meetings_object = list(map(get_meeting, meetings))

        return JsonResponse(meetings_object, safe=False)

    elif request.method == "POST":
        body = json.loads(request.body)

        meeting = Meeting.objects.create(
            date=body.get("date"),
            type=body.get("type")["value"],
            group_id=body.get("group")["id"],
            chair=body.get("chair"),
        )

        meeting.save()

        return JsonResponse({"success": True})

    return HttpResponseBadRequest()


@require_POST
@login_required_401
def api_proxy(request):
    """
    This method parses the proxy creation form
    :param request:
    :return:
    """
    pass


@require_GET
@login_required_401
def api_meeting_types(request):
    """
    This method returns all of the meeting types.
    :param request:
    :return:
    """

    def get_type(type):
        return {"label": type[1], "value": type[0]}

    return JsonResponse(list(map(get_type, Meeting.MEETING_TYPES)), safe=False)
