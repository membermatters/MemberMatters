import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers import json
from django.utils import timezone
from rest_framework import permissions

from .tasks import update_ical_feeds
from .models import Event


logger = logging.getLogger("app")


class Events(APIView):
    """
    get: gets a list of upcoming events.
    """

    def get(self, request):
        # get the next 10 events
        events = (
            Event.objects.filter(end_time__gt=timezone.now())
            .order_by("start_time")
            .all()[:10]
        )

        json_serializer = json.Serializer()
        serialized = json_serializer.serialize(events)

        return Response(serialized)


class UpdateCalendarFeeds(APIView):
    """
    post: fetches the list of calendar feeds and updates the events.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        update_ical_feeds.delay()

        return Response({"success": True})
