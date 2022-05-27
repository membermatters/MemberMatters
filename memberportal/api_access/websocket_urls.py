from django.urls import path
from . import consumers

urlpatterns = [
    path("access/door/<str:door_id>", consumers.AccessDoorConsumer.as_asgi()),
]
