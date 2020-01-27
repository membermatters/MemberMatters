from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.manage_groups, name='manage_groups'),
    path('group/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('group/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('group/<int:group_id>/email', views.email_group_members, name='email_group_members'),
    path('group/list/', views.list_groups, name='list_groups'),
    path('group/<int:group_id>/funds/', views.manage_group_funds, name='manage_group_funds'),
    path('group/fund/<int:fund_id>/delete/', views.delete_group_fund, name='delete_group_fund'),
    path('group/fund/<int:fund_id>/edit/', views.edit_group_fund, name='edit_group_fund'),
    path('group/<int:group_id>/fund/list/', views.list_group_funds, name='list_group_funds'),
]