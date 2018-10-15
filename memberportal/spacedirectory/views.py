from django.http import JsonResponse
import pytz

utc = pytz.UTC


def spacedirectory_status(request):
    return JsonResponse({
        "state": {
            "open": True,
            "message": "Open Tuesday nights to the public. All other times membership is required.",
            "icon": {
                "open": "https://hsbne.org/assets/img/headerlogo.png",
                "closed": "https://hsbne.org/assets/img/headerlogo.png"
            }
        },
        "api": "0.13",
        "location": {
            "address": "221C Macarthur Avenue, Eagle Farm QLD 4009",
            "lat": -27.4432052,
            "lon": 153.0770233
        },
        "space": "HSBNE",
        "logo": "https://hsbne.org/assets/img/headerlogo.png",
        "url": "https://hsbne.org/",

        "spacefed": {"spacenet": False, "spacesaml": False, "spacephone": False},

        "cam": ["https://portal.hsbne.org/webcamsnapshots/greenroom.jpg", "https://portal.hsbne.org/webcamsnapshots/quad.jpg"],

        "contact": {
            "email": "contact@hsbne.org",
            "twitter": "@HSBNE"
        },

        "issue_report_channels": [
            "email"
        ]

    })
