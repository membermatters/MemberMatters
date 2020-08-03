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
    path("doors/", views.Doors.as_view(), name="Doors"),
    path("interlocks/", views.Interlocks.as_view(), name="Interlocks"),
]
