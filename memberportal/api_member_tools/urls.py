from django.urls import path
from . import views

urlpatterns = [
    path("api/tools/swipes/", views.SwipesList.as_view(), name="SwipesList"),
    path("api/tools/lastseen/", views.Lastseen, name="Lastseen"),
    path("api/tools/issue/", views.IssueDetail, name="IssueDetail"),
    path("api/tools/groups/", views.MemberGroupList, name="MemberGroupList"),
    path("api/tools/meetings/", views.MemberGroupList, name="MemberGroupList"),
    path("api/tools/members/", views.api_members, name="api_members"),
]
