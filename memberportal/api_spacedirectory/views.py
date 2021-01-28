from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from constance import config
import json


class SpaceDirectoryStatus(APIView):
    """Generates a spaceapi compliant status message if enabled."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if not config.SPACE_DIRECTORY_ENABLED:
            return Response(
                "Space Directory is not enabled on this server.",
                status=status.HTTP_404_NOT_FOUND,
            )

        else:
            return Response(
                {
                    "state": {
                        "open": config.SPACE_DIRECTORY_OPEN,
                        "message": config.SPACE_DIRECTORY_MESSAGE,
                        "icon": {
                            "open": config.SPACE_DIRECTORY_ICON_OPEN,
                            "closed": config.SPACE_DIRECTORY_ICON_CLOSED,
                        },
                    },
                    "api": "0.13",
                    "location": {
                        "address": config.SPACE_DIRECTORY_LOCATION_ADDRESS,
                        "lat": config.SPACE_DIRECTORY_LOCATION_LAT,
                        "lon": config.SPACE_DIRECTORY_LOCATION_LON,
                    },
                    "space": config.SITE_OWNER,
                    "logo": config.SITE_LOGO,
                    "url": config.MAIN_SITE_URL,
                    "spacefed": {
                        "spacenet": config.SPACE_DIRECTORY_FED_SPACENET,
                        "spacesaml": config.SPACE_DIRECTORY_FED_SPACESAML,
                        "spacephone": config.SPACE_DIRECTORY_FED_SPACEPHONE,
                    },
                    "cam": json.loads(config.SPACE_DIRECTORY_CAMS),
                    "contact": {
                        "email": config.SPACE_DIRECTORY_CONTACT_EMAIL,
                        "twitter": config.SPACE_DIRECTORY_CONTACT_TWITTER,
                        "phone": config.SPACE_DIRECTORY_CONTACT_PHONE,
                        "facebook": config.SPACE_DIRECTORY_CONTACT_FACEBOOK,
                    },
                    "projects": json.loads(config.SPACE_DIRECTORY_PROJECTS),
                    "issue_report_channels": ["email"],
                }
            )
