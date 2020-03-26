from django.urls import path
from . import views

urlpatterns = [
    path("api/meeting/", views.api_meeting, name="api_meeting"),
    path("api/proxy/", views.api_proxy, name="api_proxy"),
]
