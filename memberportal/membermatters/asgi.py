import os

import django
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from membermatters.websocket_urls import urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "membermatters.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": AsgiHandler(),
        "websocket": AuthMiddlewareStack(URLRouter(urlpatterns)),
    }
)
