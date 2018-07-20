from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signin/', auth_views.login, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', auth_views.logout, {'next_page': '/loggedout'}, name='signout'),
    path('loggedout/', views.loggedout, name='loggedout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/causes/edit/', views.edit_causes, name='edit_causes'),
    path('profile/access/view/', views.access_permissions, name='access_permissions'),
    path('profile/theme/edit/', views.edit_theme_song, name='edit_theme_song'),
    path('members/list/', views.member_list, name='member_list'),
    path('member/<int:member_id>/edit', views.admin_edit_member, name='admin_edit_member'),
    path('manage/doors/', views.manage_doors, name='manage_doors'),
    path('manage/door/<int:door_id>/edit', views.edit_door, name='edit_door'),
    path('manage/door/<int:door_id>/delete', views.delete_door, name='delete_door'),
    path('manage/causes/', views.manage_causes, name='manage_causes'),
    path('api/member/<int:member_id>/state/<str:state>', views.set_state, name='set_state'),
    path('api/member/<int:member_id>/edit', views.admin_edit_member, name='admin_edit_member'),
    path('api/member/<int:member_id>/access', views.admin_edit_access, name='admin_edit_access'),
    path('api/door/<int:door_id>/grant/<int:member_id>', views.admin_grant_door, name='admin_grant_door'),
    path('api/door/<int:door_id>/revoke/<int:member_id>', views.admin_revoke_door, name='admin_revoke_door'),
    path('api/door/<int:door_id>/request', views.request_access, name='request_access'),
    path('api/door/<int:door_id>/check/<int:rfid_code>', views.check_access, name='check_access'),
    path('api/door/check/<int:rfid_code>', views.check_access, name='check_access'),
    path('cause/<int:cause_id>/delete', views.delete_cause, name='delete_cause'),
    path('cause/<int:cause_id>/edit', views.edit_cause, name='edit_cause'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
