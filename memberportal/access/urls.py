from django.urls import path
from . import views

urlpatterns = [
    path('doors/', views.manage_doors, name='manage_doors'),
    path('door/add/', views.add_door, name='add_door'),
    path('door/<int:door_id>/edit/', views.edit_door, name='edit_door'),
    path('api/door/<int:door_id>/delete/', views.delete_door, name='delete_door'),
    path('api/door/<int:door_id>/open/', views.open_door, name='open_door'),
    path('api/door/<int:door_id>/grant/<int:member_id>/', views.admin_grant_door, name='admin_grant_door'),
    path('api/door/<int:door_id>/revoke/<int:member_id>/', views.admin_revoke_door, name='admin_revoke_door'),
    path('api/door/<int:door_id>/request/', views.request_access, name='request_access'),
    path('api/door/<int:door_id>/check/<int:rfid_code>/', views.check_access, name='check_access'),
    path('api/door/check/<int:rfid_code>/', views.check_access, name='check_access'),
    path('api/door/authorised/<int:door_id>/', views.authorised_tags, name='authorised_tags'),
    path('api/door/authorised/', views.authorised_tags, name='authorised_tags'),
]
