from django.urls import path
from . import views

urlpatterns = [
    path("api/tools/swipes/", views.SwipesList.as_view(), name="SwipesList"),
    path("api/tools/lastseen/", views.Lastseen.as_view(), name="Lastseen"),
    path("api/tools/issue/", views.IssueDetail.as_view(), name="IssueDetail"),
    path("api/tools/meetings/", views.MeetingList.as_view(), name="MeetingList"),
    path("api/tools/members/", views.Members.as_view(), name="api_members"),
]
