from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/events/",
        views.Events.as_view(),
        name="api_events",
    ),
]
