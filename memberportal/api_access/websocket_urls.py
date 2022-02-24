from django.urls import path
from . import consumers

urlpatterns = [
    path("access", consumers.AccessConsumer.as_asgi()),
]
