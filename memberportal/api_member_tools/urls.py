from django.urls import path
from . import views

urlpatterns = [
    path("api/tools/swipes/", views.api_get_swipes, name="api_get_swipes"),
    path("api/tools/lastseen/", views.api_get_lastseen, name="api_get_lastseen"),
    path("api/tools/issue/", views.api_submit_issue, name="api_submit_issue"),
    path(
        "api/tools/groups/", views.api_get_member_groups, name="api_get_member_groups"
    ),
    path("api/tools/meetings/", views.api_meetings, name="api_meetings"),
    path("api/tools/members/", views.api_members, name="api_members"),
]
