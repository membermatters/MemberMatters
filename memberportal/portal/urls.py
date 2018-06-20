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
    path('admin/member/edit/<int:member_id>', views.admin_edit_member, name='admin_edit_member'),
    path('', views.home, name='home'),
]