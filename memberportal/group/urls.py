from django.urls import path
from . import views

urlpatterns = [
    path('causes/', views.manage_causes, name='manage_causes'),
    path('cause/<int:cause_id>/delete/', views.delete_cause, name='delete_cause'),
    path('cause/<int:cause_id>/edit/', views.edit_cause, name='edit_cause'),
    path('cause/<int:cause_id>/email', views.email_cause_members, name='email_cause_members'),
    path('cause/list/', views.list_causes, name='list_causes'),
    path('cause/<int:cause_id>/funds/', views.manage_cause_funds, name='manage_cause_funds'),
    path('cause/fund/<int:fund_id>/delete/', views.delete_cause_fund, name='delete_cause_fund'),
    path('cause/fund/<int:fund_id>/edit/', views.edit_cause_fund, name='edit_cause_fund'),
    path('cause/<int:cause_id>/fund/list/', views.list_cause_funds, name='list_cause_funds'),
]