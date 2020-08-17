from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/access/permissions/",
        views.UserAccessPermissions.as_view(),
        name="UserAccessPermissions",
    ),
    path(
        "api/access/doors/<int:door_id>/authorise/<int:user_id>/",
        views.AuthoriseDoor.as_view(),
        name="AuthoriseDoor",
    ),
    path(
        "api/access/doors/<int:door_id>/revoke/<int:user_id>/",
        views.RevokeDoor.as_view(),
        name="RevokeDoor",
    ),
    path(
        "api/access/interlocks/<int:interlock_id>/authorise/<int:user_id>/",
        views.AuthoriseInterlock.as_view(),
        name="AuthoriseInterlock",
    ),
    path(
        "api/access/interlocks/<int:interlock_id>/revoke/<int:user_id>/",
        views.RevokeInterlock.as_view(),
        name="RevokeInterlock",
    ),
]
