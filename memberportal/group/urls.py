from django.urls import path
from . import views

urlpatterns = [
    path("group/<int:group_id>/delete/", views.delete_group, name="delete_group"),
]
