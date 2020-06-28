from django.urls import path
from . import views

urlpatterns = [
    path("members/", views.GetMembers.as_view(), name="GetMembers"),
]
