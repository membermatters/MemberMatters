from django.urls import path
from . import views

urlpatterns = [
    path("api/door/<int:door_id>/unlock/", views.bump_door, name="bump_door"),
    path("api/door/<int:door_id>/reboot/", views.reboot_door, name="reboot_door"),
    path(
        "api/door/<int:door_id>/check/<int:rfid_code>/",
        views.check_door_access,
        name="check_access",
    ),
    path(
        "api/door/check/<int:rfid_code>/", views.check_door_access, name="check_access"
    ),
    path(
        "api/door/<int:door>/authorised/",
        views.authorised_door_tags,
        name="authorised_tags",
    ),
    path("api/door/authorised/", views.authorised_door_tags, name="authorised_tags"),
    path("api/door/<int:door>/checkin/", views.door_checkin, name="door_checkin"),
    path("api/door/checkin/", views.door_checkin, name="door_checkin"),
    path(
        "api/door/reset-default-access",
        views.reset_default_door_access,
        name="reset_default_access",
    ),
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
    path(
        "api/interlock/reset-default-access/",
        views.reset_default_interlock_access,
        name="reset_default_interlock_access",
    ),
    path("cron/interlock/", views.interlock_cron, name="interlock_cron"),
]
