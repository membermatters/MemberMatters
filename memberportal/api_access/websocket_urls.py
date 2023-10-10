from django.urls import path
from . import consumers

urlpatterns = [
    path("access/door/<str:device_id>", consumers.DoorConsumer.as_asgi()),
    path("access/interlock/<str:device_id>", consumers.InterlockConsumer.as_asgi()),
    path(
        "access/memberbucks/<str:device_id>",
        consumers.MemberbucksConsumer.as_asgi(),
    ),
]
