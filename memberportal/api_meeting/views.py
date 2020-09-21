from .models import Meeting, ProxyVote
from profile.models import Profile
from django.utils.timezone import make_aware, localtime
from datetime import datetime

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from profile.emailhelpers import send_single_email


class Meetings(APIView):
    """
    get: retrieves a list of all meetings.
    post: creates a new meeting.
    put: update an existing meeting.
    delete: delete an existing meeting.
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
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
                "typeValue": meeting.type,
                "group": meeting.group.name if meeting.group else None,
                "groupValue": meeting.group.id if meeting.group else None,
                "attendeeCount": meeting.attendees.count(),
                "attendees": list(map(get_attendee, meeting.attendees.all())),
                "proxyList": list(map(get_proxy, meeting.proxyvote_set.all())),
            }

        meetings_object = list(map(get_meeting, meetings))

        return Response(meetings_object)

    def post(self, request):
        body = request.data

        meeting = Meeting.objects.create(
            date=make_aware(datetime.strptime(body["date"], "%Y-%m-%d %H:%M")),
            type=body["type"]["value"],
            group_id=body["group"]["id"] if len(body["group"]) else "",
            chair=body["chair"],
        )

        meeting.save()

        return Response({"success": True})

    def put(self, request, meeting_id):
        body = request.data

        meeting = Meeting.objects.get(id=meeting_id)
        meeting.date = make_aware(datetime.strptime(body["date"], "%Y-%m-%d %H:%M"))
        meeting.chair = body["chair"]
        meeting.save()

        return Response()

    def delete(self, request, meeting_id):
        meeting = Meeting.objects.get(id=meeting_id)
        meeting.delete()

        return Response()


class Proxies(APIView):
    """
    get: retrieve a list of user's proxy votes.
    post: create a new proxy vote.
    delete: delete an existing proxy vote.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        proxies = ProxyVote.objects.filter(user=request.user)

        def get_proxy_details(proxy):
            return {
                "id": proxy.id,
                "name": proxy.proxy_user.profile.get_full_name(),
                "date": proxy.meeting.date,
                "type": proxy.meeting.get_type(),
            }

        return Response(list(map(get_proxy_details, proxies)))

    def post(self, request):
        body = request.data
        member_city = body.get("memberCity")
        proxy_id = body.get("proxy")
        proxy_city = body.get("proxyCity")
        meeting_id = body.get("meeting")

        existing_proxies = ProxyVote.objects.filter(
            user=request.user, meeting_id=meeting_id
        )

        # if the user already has a proxy for this meeting we'll override it
        if existing_proxies:
            for proxy in existing_proxies:
                proxy.delete()

        if member_city and proxy_id and proxy_city and meeting_id:
            meeting = Meeting.objects.get(pk=meeting_id)
            proxy_user = Profile.objects.get(id=proxy_id).user
            ProxyVote.objects.create(
                user=request.user,
                user_city=member_city,
                proxy_user=proxy_user,
                proxy_city=proxy_city,
                meeting=meeting,
            )

            subject = (
                f"{request.user.profile.get_full_name()} just assigned you as a proxy"
            )
            message = f"{request.user.profile.get_full_name()} just assigned you as a proxy for the {meeting.get_type()} meeting on {localtime(meeting.date)}."
            send_single_email(request.user, proxy_user.email, subject, subject, message)

            subject = f"{proxy_user.profile.get_full_name()} is confirmed as your proxy for the {meeting.get_type()} meeting"
            message = f"{proxy_user.profile.get_full_name()} is confirmed as your proxy for the {meeting.get_type()} meeting on {localtime(meeting.date)}. You can manage this proxy from the member portal."
            send_single_email(
                request.user, request.user.email, subject, subject, message
            )

            return Response({"success": True})

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, proxy_id):
        proxy = ProxyVote.objects.get(id=proxy_id)

        if request.user == proxy.user:
            proxy.delete()
            subject = (
                f"{request.user.profile.get_full_name()} just removed you as a proxy"
            )
            message = f"{request.user.profile.get_full_name()} just removed you as a proxy for the {proxy.meeting.get_type()} meeting on {localtime(proxy.meeting.date)}."
            send_single_email(
                request.user, proxy.proxy_user.email, subject, subject, message
            )

            subject = f"{proxy.proxy_user.profile.get_full_name()} is no longer your proxy for the {proxy.meeting.get_type()} meeting"
            message = f"{proxy.proxy_user.profile.get_full_name()} is no longer your proxy for the {proxy.meeting.get_type()} meeting on {localtime(proxy.meeting.date)}. You can manage this proxy from the member portal."
            send_single_email(
                request.user, request.user.email, subject, subject, message
            )
            return Response()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class MeetingTypes(APIView):
    """
    get: retrieves all of the meeting types.
    """

    def get(self, request):
        def get_type(type):
            return {"label": type[1], "value": type[0]}

        return Response(list(map(get_type, Meeting.MEETING_TYPES)))
