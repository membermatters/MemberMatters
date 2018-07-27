from django.urls import path
from . import views

urlpatterns = [
    path('causes/', views.manage_causes, name='manage_causes'),
    path('cause/<int:cause_id>/delete/', views.delete_cause, name='delete_cause'),
    path('cause/<int:cause_id>/edit/', views.edit_cause, name='edit_cause'),
    path('cause/list/', views.list_causes, name='list_causes'),
]
