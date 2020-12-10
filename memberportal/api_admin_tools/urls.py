from django.urls import path
from . import views

# all of these urls start with "api/admin/"

urlpatterns = [
    path("members/", views.GetMembers.as_view(), name="GetMembers"),
    path(
        "members/<int:member_id>/state/<str:state>/",
        views.MemberState.as_view(),
        name="MemberState",
    ),
    path(
        "members/<int:member_id>/makemember/",
        views.MakeMember.as_view(),
        name="ActivateMember",
    ),
    path(
        "members/<int:member_id>/access/",
        views.MemberAccess.as_view(),
        name="MemberAccess",
    ),
    path(
        "members/<int:member_id>/sendwelcome/",
        views.MemberWelcomeEmail.as_view(),
        name="MemberWelcomeEmail",
    ),
    path(
        "members/<int:member_id>/profile/",
        views.MemberProfile.as_view(),
        name="MemberProfile",
    ),
    path(
        "members/<int:member_id>/invoice/<str:send_email>/",
        views.MemberCreateNewInvoice.as_view(),
        name="MemberCreateNewInvoice",
    ),
    path("doors/", views.Doors.as_view(), name="Doors"),
    path("interlocks/", views.Interlocks.as_view(), name="Interlocks"),
    path("doors/<int:door_id>/", views.Doors.as_view(), name="Doors"),
    path(
        "interlocks/<int:interlock_id>/", views.Interlocks.as_view(), name="Interlocks"
    ),
    path("plans/", views.Plans.as_view(), name="Plans"),
    path("plans/<int:plan_id>/", views.Plans.as_view(), name="Plans"),
]
