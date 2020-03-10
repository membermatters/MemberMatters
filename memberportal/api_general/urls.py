from django.urls import path
from . import views

urlpatterns = [
    path("api/config/", views.api_get_config, name="api_get_config"),
    path("api/login/", views.api_login, name="api_login"),
    path("api/logout/", views.api_logout, name="api_logout"),
]
