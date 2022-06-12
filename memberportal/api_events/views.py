import logging
from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger("app")


class Events(APIView):
    """
    get: gets a list of upcoming events.
    """

    def get(self, request):
        events = []
        event_list = []

        for event in events:
            event_list.append(event.get_json_object())

        statistics = {"events": event_list}

        return Response(statistics)
