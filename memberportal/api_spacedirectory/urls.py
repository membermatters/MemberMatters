from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/spacedirectory/",
        views.SpaceDirectoryStatus.as_view(),
        name="spacedirectory_status",
    ),
    path(
        "api/spacedirectory/update",
        views.SpaceDirectoryUpdate.as_view(),
        name="spacedirectory_update",
    ),
]
