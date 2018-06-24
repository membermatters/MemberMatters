from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signin/', auth_views.login, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', auth_views.logout, {'next_page': '/loggedout'}, name='signout'),
    path('loggedout/', views.loggedout, name='loggedout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('members/list/', views.member_list, name='member_list'),
    path('member/<int:member_id>/state/<int:state>', views.set_state, name='set_state'),
    path('member/<int:member_id>/edit', views.admin_edit_member, name='admin_edit_member'),
    path('admin/doors/', views.manage_doors, name='manage_doors'),
    path('api/access/<int:member_id>/edit', views.admin_edit_member, name='admin_edit_member'),
    path('', views.home, name='home'),
]