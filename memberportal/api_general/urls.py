from django.urls import path
from . import views

urlpatterns = [
    path("api/config/", views.api_get_config, name="api_get_config"),
    path("api/login/", views.api_login, name="api_login"),
    path("api/password/reset/", views.api_reset_password, name="api_reset_password"),
    path("api/logout/", views.api_logout, name="api_logout"),
    path("api/profile/", views.api_profile, name="api_profile"),
    path("api/profile/password/", views.api_password, name="api_password"),
    path("api/profile/idtoken/", views.api_digital_id, name="api_digital_id"),
]
