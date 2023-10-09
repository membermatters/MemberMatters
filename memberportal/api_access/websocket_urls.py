from django.urls import path
from . import consumers

urlpatterns = [
    path("access/door/<str:door_id>", consumers.AccessDeviceConsumer.as_asgi()),
    path(
        "access/interlock/<str:interlock_id>", consumers.AccessDeviceConsumer.as_asgi()
    ),
    path(
        "access/memberbucks/<str:memberbucks_id>",
        consumers.AccessDeviceConsumer.as_asgi(),
    ),
]
