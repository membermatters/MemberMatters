from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signin/', auth_views.login, name='signin'),
    path('signout/', auth_views.logout,
         {'next_page': '/loggedout'}, name='signout'),
    path('loggedout/', views.loggedout, name='loggedout'),
    path('webcams/', views.webcams, name='webcams'),
    path('spacebug/report/', views.spacebug, name='report_spacebug'),
    path('', views.home, name='home'),
]
