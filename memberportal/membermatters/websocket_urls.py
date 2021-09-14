"""
URL configuration for websocket endpoints
"""

from channels.routing import URLRouter
from django.urls import path
import api_access.websocket_urls

urlpatterns = [
    path(
        "ws/", URLRouter([path("", URLRouter(api_access.websocket_urls.urlpatterns))])
    ),
]
