from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/interlock/<int:interlock_id>/check/<int:rfid_code>/",
        views.check_interlock_access,
        name="check_interlock_access",
    ),
    path(
        "api/interlock/check/<int:rfid_code>/",
        views.check_interlock_access,
        name="check_interlock_access",
    ),
    path(
        "api/interlock/session/<uuid:session_id>/heartbeat/",
        views.check_interlock_access,
        name="check_interlock_access",
    ),
    path(
        "api/interlock/session/<uuid:session_id>/end/",
        views.end_interlock_session,
        name="end_interlock_session",
    ),
    path(
        "api/interlock/session/<uuid:session_id>/end/<int:rfid>/",
        views.end_interlock_session,
        name="end_interlock_session",
    ),
    path(
        "api/interlock/<int:interlock>/checkin/",
        views.interlock_checkin,
        name="interlock_checkin",
    ),
    path("api/interlock/checkin/", views.interlock_checkin, name="interlock_checkin"),
    path(
        "api/interlock/authorised/",
        views.authorised_interlock_tags,
        name="authorised_interlock_tags",
    ),
    path(
        "api/interlock/<int:interlock>/authorised/",
        views.authorised_interlock_tags,
        name="authorised_interlock_tags",
    ),
    path("cron/interlock/", views.interlock_cron, name="interlock_cron"),
]
