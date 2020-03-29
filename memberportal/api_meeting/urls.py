from django.urls import path
from . import views

urlpatterns = [
    path("api/meetings/", views.api_meeting, name="api_meeting"),
    path("api/meetings/types/", views.api_meeting_types, name="api_meeting_types"),
    path("api/meetings/<uuid:meeting_id>/", views.api_meeting, name="api_meeting"),
    path("api/proxy/", views.api_proxy, name="api_proxy"),
]
