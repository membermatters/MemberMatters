from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from profile.models import Profile
import pytz

utc = pytz.UTC

def spacedirectory_status(request):


    return JsonResponse({
    "state": {
        "open": False,
        "message": "Closed until Tuesday 5PM",
        "icon": {
            "open": "http://hsbne.org/assets/img/headerlogo.png",
            "closed": "http://hsbne.org/assets/img/headerlogo.png"
        }
    },
    "api": "0.13",
    "location": {
        "address": "221C Macarthur Avenue, Eagle Farm QLD 4009",
        "lat": -27.4432052,
        "lon": 153.0770233
    },
    "space": "HSBNE",
    "logo": "http://hsbne.org/assets/img/headerlogo.png",
    "url": "http://hsbne.org/",

    "contact": {
        "email": "contact@hsbne.org",
        "twitter": "@HSBNE"
    },
    
    "issue_report_channels": [
        "email"
    ]

}
        )


