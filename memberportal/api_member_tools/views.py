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
    post: Creates a new issue by creating a task card or emailing the management committee
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        body = request.data
        title = body["title"]
        description = request.user.profile.get_full_name() + ": " + body["description"]

        if not (title and description):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        failed = False

        request.user.log_event(
            "Submitted issue: " + title + " Content: " + description,
            "generic",
        )

        if config.REPORT_ISSUE_ENABLE_VIKUNJA and bool(
            config.VIKUNJA_DEFAULT_PROJECT_ID
        ):
            vikunja_project_id = config.VIKUNJA_DEFAULT_PROJECT_ID
            vikunja_label_id = config.VIKUNJA_DEFAULT_LABEL_ID

            try:
                task_body = {
                    "max_right": None,
                    "id": 0,
                    "title": title,
                    "description": description,
                    "done": False,
                    "done_at": None,
                    "priority": 0,
                    "labels": [],
                    "assignees": [],
                    "due_date": None,
                    "start_date": None,
                    "end_date": None,
                    "repeat_after": 0,
                    "repeat_from_current_date": False,
                    "repeat_mode": 0,
                    "reminders": [],
                    "parent_task_id": 0,
                    "hex_color": "",
                    "percent_done": 0,
                    "related_tasks": {},
                    "attachments": [],
                    "cover_image_attachment_id": None,
                    "identifier": "",
                    "index": 0,
                    "is_favorite": False,
                    "subscription": None,
                    "position": 64,
                    "reactions": {},
                    "created_by": {
                        "max_right": None,
                        "id": 0,
                        "email": "",
                        "username": "",
                        "name": "",
                        "exp": 0,
                        "type": 0,
                        "created": None,
                        "updated": None,
                        "settings": {
                            "max_right": None,
                            "name": "",
                            "email_reminders_enabled": False,
                            "discoverable_by_name": False,
                            "discoverable_by_email": True,
                            "overdue_tasks_reminders_enabled": False,
                            "week_start": 0,
                            "timezone": "",
                            "language": "en",
                            "frontend_settings": {
                                "play_sound_when_done": False,
                                "quick_add_magic_mode": "vikunja",
                                "color_schema": "auto",
                                "default_view": "first",
                            },
                        },
                    },
                    "created": "1970-01-01T00:00:00.000Z",
                    "updated": "1970-01-01T00:00:00.000Z",
                    "project_id": vikunja_project_id,
                    "bucket_id": 0,
                    "reminder_dates": None,
                }

                task_response = requests.request(
                    "PUT",
                    f"{config.VIKUNJA_URL}/api/v1/projects/{vikunja_project_id}/tasks",
                    json=task_body,
                    headers={"Authorization": "Bearer " + config.VIKUNJA_API_TOKEN},
                )

                if (vikunja_label_id is not None) and (
                    task_response.status_code == 200
                ):
                    try:
                        task_id = task_response.json["id"]
                        label_body = {
                            "label_id": vikunja_label_id,
                            "created": "1970-01-01T00:00:00.000Z",
                        }

                        label_response = requests.request(
                            "PUT",
                            f"{config.VIKUNJA_URL}/api/v1/tasks/{task_id}/labels",
                            json=label_body,
                            headers={
                                "Authorization": "Bearer " + config.VIKUNJA_API_TOKEN
                            },
                        )
                    except Exception:
                        pass

                if task_response.status_code != 200:
                    failed = True

            except Exception:
                # uh oh, but don't stop processing other ones
                failed = True

        if config.REPORT_ISSUE_ENABLE_TRELLO:
            try:
                trello_key = config.TRELLO_API_KEY
                trello_token = config.TRELLO_API_TOKEN
                trello_id_list = config.TRELLO_ID_LIST
                trello_url = "https://api.trello.com/1/cards"

                querystring = {
                    "name": title,
                    "desc": description,
                    "pos": "top",
                    "idList": trello_id_list,
                    "keepFromSource": "all",
                    "key": trello_key,
                    "token": trello_token,
                }

                response = requests.request("POST", trello_url, params=querystring)

                if response.status_code != 200:
                    failed = True

            except Exception:
                # uh oh, but don't stop processing other ones
                failed = True

        # email report
        if config.REPORT_ISSUE_ENABLE_EMAIL:
            try:
                subject = f"{request.user.profile.get_full_name()}: {title}"

                if not send_email_to_admin(
                    subject=subject,
                    template_vars={
                        "title": subject,
                        "message": description,
                    },
                    user=request.user,
                    reply_to=request.user.email,
                ):
                    failed = True

            except Exception:
                # uh oh, but don't stop processing other ones
                failed = True

        if failed:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                {"success": True},
                status=status.HTTP_201_CREATED,
            )


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
