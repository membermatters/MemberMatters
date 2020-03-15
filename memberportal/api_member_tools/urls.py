from django.urls import path
from . import views

urlpatterns = [
    path("api/tools/swipes/", views.api_get_swipes, name="api_get_swipes"),
    path("api/tools/lastseen/", views.api_get_lastseen, name="api_get_lastseen"),
    path("api/tools/issue/", views.api_submit_issue, name="api_submit_issue"),
]
