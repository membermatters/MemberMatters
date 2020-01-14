from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signin/', auth_views.LoginView.as_view(), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(),
         {'next_page': '/loggedout'}, name='signout'),
    path('loggedout/', views.loggedout, name='loggedout'),
    path('webcams/', views.webcams, name='webcams'),
    path('spacebug/report/', views.spacebug, name='report_spacebug'),
    path('proxy/', views.proxy, name='submit_proxy'),
    path('', views.home, name='home'),
    # path('cron/invoices/', views.invoice_cron, name='invoice_cron'),
    # path('cron/overdue/', views.overdue_cron, name='overdue_cron'),
]
