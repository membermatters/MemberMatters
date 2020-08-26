from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401
from profile.models import User, Profile
from group.models import Group
from api_meeting.models import Meeting
from constance import config
from membermatters.helpers import log_user_event
from profile.emailhelpers import send_single_email
from random import shuffle
import requests
import datetime
from django.utils import timezone

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class SwipesList(APIView):
    """
    get: This method returns the 50 most recent swipes on each door and interlock.
    """

    permission_classes = (permissions.IsAuthenticated,)

    # TODO: refactor this into two separate API requests for each resource so it's more RESTful

    def get(self, request):
        recent_doors = DoorLog.objects.all().order_by("date")[::-1][:50]
        recent_interlocks = InterlockLog.objects.all().order_by("last_heartbeat")[::-1][
            :50
        ]

        doors = []
        interlocks = []

        for door in recent_doors:
            doors.append(
                {
                    "name": door.door.name,
                    "date": door.date,
                    "user": door.user.profile.get_full_name(),
                }
            )

        for interlock in recent_interlocks:
            user_off = None

            if interlock.user_off:
                user_off = interlock.user_off.profile.get_full_name()

            interlocks.append(
                {
                    "name": interlock.interlock.name,
                    "sessionStart": interlock.first_heartbeat,
                    "sessionEnd": interlock.last_heartbeat,
                    "sessionComplete": interlock.session_complete,
                    "userOn": interlock.user.profile.get_full_name(),
                    "userOff": user_off,
                }
            )

        return Response(
            {"doors": doors, "interlocks": interlocks}, status=status.HTTP_200_OK
        )


class Lastseen(APIView):
    """
    get: This method returns when each user was last seen (ie when they last swiped).
    """

    # TODO: refactor this so it utilises DRF more

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.filter(state="active").order_by("-last_seen")

    def get(self, request):
        last_seen = list()

        for member in self.queryset.all():
            if not member.state == "active":
                continue

            if member.last_seen is not None:
                last_seen.append(
                    {
                        "id": member.id,
                        "user": member.get_full_name(),
                        "never": False,
                        "date": member.last_seen,
                    }
                )

            else:
                last_seen.append(
                    {"id": member.id, "user": member.get_full_name(), "never": True}
                )

        return Response(last_seen, status=status.HTTP_200_OK)


class IssueDetail(APIView):
    """
    post: Creates a new issue by creating a trello card or emailing the management committee
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        body = request.data
        title = body["title"]
        description = request.user.profile.get_full_name() + ": " + body["description"]

        if not (title and description):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        use_trello = config.ENABLE_TRELLO_INTEGRATION
        trello_key = config.TRELLO_API_KEY
        trello_token = config.TRELLO_API_TOKEN
        trello_id_list = config.TRELLO_ID_LIST

        if use_trello:
            url = "https://api.trello.com/1/cards"

            querystring = {
                "name": title,
                "desc": description,
                "pos": "top",
                "idList": trello_id_list,
                "keepFromSource": "all",
                "key": trello_key,
                "token": trello_token,
            }

            response = requests.request("POST", url, params=querystring)

            if response.status_code == 200:
                log_user_event(
                    request.user,
                    "Submitted issue: " + title + " Content: " + description,
                    "generic",
                )

                return Response(
                    {"success": True, "url": response.json()["shortUrl"]},
                    status=status.HTTP_201_CREATED,
                )

            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # if Trello isn't configured, use email instead
        else:
            subject = (
                f"{request.user.profile.get_full_name()} submitted an issue ({title})"
            )

            if send_single_email(
                request.user,
                config.EMAIL_ADMIN,
                subject,
                subject,
                description,
                from_user=True,
            ):
                return Response({"success": True}, status=status.HTTP_201_CREATED,)

            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MemberGroupList(APIView):
    """
    get: This method returns a list of all active members and their groups.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        def get_groups(groups):
            temp_groups = []

            for group in groups:
                if group.hidden:
                    continue
                else:
                    temp_groups.append(group.name)

            return temp_groups

        members = User.objects.filter(profile__state="active")

        groups = Group.objects.filter(hidden=False).prefetch_related()
        parsed_groups = []
        parsed_members = []

        for member in members:
            parsed_members.append(
                {
                    "member": f"{member.profile.get_full_name()} ({member.profile.screen_name})",
                    "groups": get_groups(member.profile.groups.all()),
                }
            )

        for group in groups:
            parsed_groups.append(
                {
                    "name": group.name,
                    "activeMembers": group.get_active_count(),
                    "quorum": group.get_quorum(),
                }
            )

        response = {"groups": parsed_groups, "members": parsed_members}
        return Response(response, status=status.HTTP_200_OK)


class MeetingList(APIView):
    """
    get: Returns a list of upcoming meetings that a member is entitled to vote at.
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Meeting.objects.filter(date__gt=datetime.datetime.now())

    def get(self, request):
        def get_meeting(meeting):
            date = timezone.localtime(meeting.date).strftime("%x %X")

            if meeting.type == "group":
                return {
                    "id": meeting.id,
                    "name": meeting.group.name,
                    "date": date,
                }
            return {
                "id": meeting.id,
                "name": meeting.get_type_display(),
                "date": date,
            }

        def check_meeting(meeting):
            if meeting.type != "group":
                return True

            elif meeting.group in request.user.profile.groups.all():
                return True

            return False

        response = list(map(get_meeting, filter(check_meeting, self.queryset.all())))

        return JsonResponse(response, safe=False)


@require_GET
@login_required_401
def api_members(request):
    """
    Gets a list of all members.
    :param request:
    :return:
    """

    def get_member(member):
        return {
            "id": member.id,
            "name": member.get_full_name(),
            "screenName": member.screen_name,
        }

    members = list(map(get_member, Profile.objects.filter(state="active")))
    shuffle(members)

    return JsonResponse(members, safe=False)
