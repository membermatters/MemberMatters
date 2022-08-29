from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/events/",
        views.Events.as_view(),
        name="api_events",
    ),
    path(
        "api/events/calendar-feeds/update",
        views.UpdateCalendarFeeds.as_view(),
        name="api_update_calendar_feeds",
    ),
]
