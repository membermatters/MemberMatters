from django.urls import path
from . import views

urlpatterns = [
    path('spacedirectory/', views.spacedirectory_status, name='spacedirectory_status'),
    ]

