from django.http import JsonResponse, HttpResponseNotFound
from django.conf import settings
from constance import config
import json


def spacedirectory_status(request):
    if not config.SPACE_DIRECTORY_ENABLED:
        return HttpResponseNotFound("Space Directory is not enabled on this server.")

    else:
        return JsonResponse({
            "state": {
                "open": config.SPACE_DIRECTORY_OPEN,
                "message": config.SPACE_DIRECTORY_MESSAGE,
                "icon": {
                    "open": config.SPACE_DIRECTORY_ICON_OPEN,
                    "closed": config.SPACE_DIRECTORY_ICON_CLOSED
                }
            },
            "api": "0.13",
            "location": {
                "address": config.SPACE_DIRECTORY_LOCATION_ADDRESS,
                "lat": config.SPACE_DIRECTORY_LOCATION_LAT,
                "lon": config.SPACE_DIRECTORY_LOCATION_LON
            },
            "space": config.SITE_OWNER,
            "logo": config.SITE_URL + settings.MEDIA_URL + config.SITE_LOGO,
            "url": config.MAIN_SITE_URL,
            "spacefed": {"spacenet": config.SPACE_DIRECTORY_FED_SPACENET, "spacesaml": config.SPACE_DIRECTORY_FED_SPACESAML, "spacephone": config.SPACE_DIRECTORY_FED_SPACEPHONE},
            "cam": json.loads(config.SPACE_DIRECTORY_CAMS),
            "contact": {
                "email": config.SPACE_DIRECTORY_CONTACT_EMAIL,
                "twitter": config.SPACE_DIRECTORY_CONTACT_TWITTER,
                "phone": config.SPACE_DIRECTORY_CONTACT_PHONE,
                "facebook": config.SPACE_DIRECTORY_CONTACT_FACEBOOK
            },
            "projects": json.loads(config.SPACE_DIRECTORY_PROJECTS),
            "issue_report_channels": [
                "email"
            ]

        })
