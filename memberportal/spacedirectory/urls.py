from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/spacedirectory/", views.spacedirectory_status, name="spacedirectory_status"
    ),
]
