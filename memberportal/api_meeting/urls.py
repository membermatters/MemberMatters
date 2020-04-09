from django.urls import path
from . import views

urlpatterns = [
    path("api/meetings/", views.Meetings.as_view(), name="Meetings"),
    path("api/meetings/types/", views.MeetingTypes.as_view(), name="MeetingTypes"),
    path("api/meetings/<uuid:meeting_id>/", views.Meetings.as_view(), name="Meetings"),
    path("api/proxies/", views.Proxies.as_view(), name="Proxies"),
    path("api/proxies/<int:meeting_id>/", views.Proxies.as_view(), name="Proxies"),
]
