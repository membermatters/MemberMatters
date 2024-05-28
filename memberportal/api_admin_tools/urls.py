from django.urls import path
from . import views

# all of these urls start with "api/admin/"

urlpatterns = [
    path("api/admin/members/", views.GetMembers.as_view(), name="GetMembers"),
    path(
        "api/admin/members/<int:member_id>/state/<str:state>/",
        views.MemberState.as_view(),
        name="MemberState",
    ),
    path(
        "api/admin/members/<int:member_id>/makemember/",
        views.MakeMember.as_view(),
        name="ActivateMember",
    ),
    path(
        "api/admin/members/<int:member_id>/access/",
        views.MemberAccess.as_view(),
        name="MemberAccess",
    ),
    path(
        "api/admin/members/<int:member_id>/sendwelcome/",
        views.MemberWelcomeEmail.as_view(),
        name="MemberWelcomeEmail",
    ),
    path(
        "api/admin/members/<int:member_id>/sendsms/",
        views.MemberSendSms.as_view(),
        name="MemberSendSms",
    ),
    path(
        "api/admin/members/<int:member_id>/profile/",
        views.MemberProfile.as_view(),
        name="MemberProfile",
    ),
    path(
        "api/admin/members/<int:member_id>/billing/",
        views.MemberBillingInfo.as_view(),
        name="MemberBillingInfo",
    ),
    path(
        "api/admin/members/<int:member_id>/logs/",
        views.MemberLogs.as_view(),
        name="MemberLogs",
    ),
    path("api/admin/doors/", views.Doors.as_view(), name="Doors"),
    path("api/admin/interlocks/", views.Interlocks.as_view(), name="Interlocks"),
    path("api/admin/doors/<int:door_id>/", views.Doors.as_view(), name="Doors"),
    path(
        "api/admin/interlocks/<int:interlock_id>/",
        views.Interlocks.as_view(),
        name="Interlocks",
    ),
    path(
        "api/admin/memberbucks-devices/",
        views.MemberbucksDevices.as_view(),
        name="MemberbucksDevices",
    ),
    path(
        "api/admin/memberbucks-devices/<int:device_id>/",
        views.MemberbucksDevices.as_view(),
        name="MemberbucksDevices",
    ),
    path("api/admin/tiers/", views.MemberTiers.as_view(), name="ManageMemberTiers"),
    path(
        "api/admin/tiers/<int:tier_id>/",
        views.ManageMemberTier.as_view(),
        name="ManageMemberTier",
    ),
    path(
        "api/admin/tiers/<int:tier_id>/plans/",
        views.ManageMemberTierPlans.as_view(),
        name="GetPlans",
    ),
    path(
        "api/admin/plans/",
        views.ManageMemberTierPlans.as_view(),
        name="ManagePlans",
    ),
    path(
        "api/admin/plans/<int:plan_id>/",
        views.ManageMemberTierPlans.as_view(),
        name="ManagePlan",
    ),
]
