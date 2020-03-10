from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from constance import config
import json


@require_GET
def api_get_config(request):
    response = {
        "general": {
            "siteName": config.SITE_NAME,
            "siteOwner": config.SITE_OWNER,
            "entityType": config.ENTITY_TYPE,
        },
        "images": {
            "siteLogo": config.SITE_LOGO,
            "siteFavicon": config.SITE_FAVICON,
        },
        "homepageCards": json.loads(config.HOME_PAGE_CARDS)
    }
    return JsonResponse(response)
