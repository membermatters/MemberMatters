from django.urls import path
from . import views

urlpatterns = [
    path("api/access/permissions/", views.api_get_access_permissions, name="api_get_access_permissions"),
]
