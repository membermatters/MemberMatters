from django.urls import path
from . import views

urlpatterns = [
    path("profile/memberbucks/manage/", views.manage_memberbucks, name="manage_memberbucks"),
    path("profile/memberbucks/add/", views.add_memberbucks_page, name="add_memberbucks"),
    path("profile/memberbucks/add/<int:amount>", views.add_memberbucks, name="add_memberbucks"),
    path("profile/memberbucks/paymentdetails/save/", views.add_memberbucks_payment_info,
         name="add_memberbucks_payment_info"),
    path("profile/memberbucks/paymentdetails/delete/", views.delete_memberbucks_payment_info,
         name="delete_memberbucks_payment_info"),
    path("api/memberbucks/debit/", views.memberbucks_debit, name="memberbucks_debit"),
    path("api/memberbucks/debit/<int:rfid>/<int:amount>/", views.memberbucks_debit, name="memberbucks_debit"),
    path("api/memberbucks/balance/<int:rfid>/", views.memberbucks_balance, name="memberbucks_balance"),
    path("api/memberbucks/groupdonation/<int:rfid>/<int:group_id>/<int:amount>/", views.memberbucks_group_donation,
         name="memberbucks_group_donation"),
    path("api/memberbucks/debit/<int:rfid>/<int:amount>/<str:description>", views.memberbucks_debit,
         name="memberbucks_debit"),
]
