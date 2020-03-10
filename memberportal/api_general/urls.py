from django.urls import path
from . import views

urlpatterns = [
    path("api/config/", views.api_get_config, name="api_get_config"),
]
