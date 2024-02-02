"""membermatters URL Configuration
"""

import os
import django.db.utils
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from constance import config
import json
from asgiref.sync import sync_to_async


@sync_to_async
def safe_constance_get(fld: str):
    return getattr(config, fld)


# try:
#     SENTRY_DSN_BACKEND = safe_constance_get("SENTRY_DSN_BACKEND")
#     if (
#             SENTRY_DSN_BACKEND
#             and os.environ.get("MM_ENV")
#             and os.environ.get("MM_ENV") != "Development"
#     ):
#         version = None
#         with open("../package.json") as f:
#             d = json.load(f)
#
#         sentry_sdk.init(
#             release=d.get("version"),
#             dsn=SENTRY_DSN_BACKEND,
#             integrations=[DjangoIntegration()],
#         )
# except django.db.utils.OperationalError as e:
#     pass

urlpatterns = [
    path("api/openid/", include("oidc_provider.urls", namespace="oidc_provider")),
    path("", include("api_spacedirectory.urls")),
    path("", include("api_general.urls")),
    path("", include("api_access.urls")),
    path("", include("api_member_tools.urls")),
    path("", include("api_meeting.urls")),
    path("", include("api_member_bucks.urls")),
    path("", include("api_billing.urls")),
    path("", include("api_admin_tools.urls")),
    path("api/", include("django_prometheus.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root="")
