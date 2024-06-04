from access.models import DoorLog, InterlockLog
from profile.models import Profile
from api_meeting.models import Meeting
from constance import config
from services.emails import send_email_to_admin
from random import shuffle
import requests
from django.utils import timezone

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class SwipesList(APIView):
    """
    get: This method returns the 300 most recent swipes for both doors and interlocks.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        recent_doors = (
            DoorLog.objects.all()
            .select_related("user__profile")
            .order_by("date")[::-1][:300]
        )
        recent_interlocks = (
            InterlockLog.objects.all()
            .select_related("user_started__profile", "user_ended__profile")
            .order_by("date_updated")[::-1][:300]
        )

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
            user_ended = None

            if interlock.user_ended:
                user_ended = interlock.user_ended.profile.get_full_name()

            interlocks.append(
                {
                    "name": interlock.interlock.name,
                    "sessionStart": interlock.date_started,
                    "sessionEnd": interlock.date_ended,
                    "sessionComplete": True if interlock.date_ended else False,
                    "userOn": interlock.user_started.profile.get_full_name(),
                    "userOff": user_ended,
                }
            )

        return Response(
            {"doors": doors, "interlocks": interlocks}, status=status.HTTP_200_OK
        )


class Lastseen(APIView):
    """
    get: This method returns when each user was last seen (ie when they last swiped).
    """

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
                request.user.log_event(
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
            subject = f"{request.user.profile.get_full_name()} submitted an issue about {title}"

            if send_email_to_admin(
                subject=subject,
                template_vars={
                    "title": subject,
                    "message": description,
                },
                user=request.user,
                reply_to=request.user.email,
            ):
                return Response(
                    {"success": True},
                    status=status.HTTP_201_CREATED,
                )

            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeetingList(APIView):
    """
    get: Returns a list of upcoming meetings that a member is entitled to vote at.
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Meeting.objects.filter(date__gt=timezone.now())

    def get(self, request):
        def get_meeting(meeting):
            date = timezone.localtime(meeting.date).strftime("%x %X")

            return {
                "id": meeting.id,
                "name": meeting.get_type_display(),
                "date": date,
            }

        response = list(map(get_meeting, self.queryset.all()))

        return Response(response)


class Members(APIView):
    """
    get: gets a list of all members.
    """

    def get(self, request):
        def get_member(member):
            return {
                "id": member.id,
                "name": member.get_full_name(),
                "screenName": member.screen_name,
            }

        members = list(map(get_member, Profile.objects.filter(state="active")))
        shuffle(members)

        return Response(members)
