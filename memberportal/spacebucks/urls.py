from django.urls import path
from . import views

urlpatterns = [
    path('profile/spacebucks/manage/', views.manage_spacebucks, name='manage_spacebucks'),
    path('profile/spacebucks/add/', views.add_spacebucks_page, name='add_spacebucks'),
    path('profile/spacebucks/add/<int:amount>', views.add_spacebucks, name='add_spacebucks'),
    path('profile/spacebucks/paymentdetails/save/', views.add_spacebucks_payment_info,
         name='add_spacebucks_payment_info'),
    path('profile/spacebucks/paymentdetails/delete/', views.delete_spacebucks_payment_info,
         name='delete_spacebucks_payment_info'),
    path('api/spacebucks/debit/', views.spacebucks_debit, name="spacebucks_debit"),
    path('api/spacebucks/debit/<int:rfid>/<int:amount>/', views.spacebucks_debit, name="spacebucks_debit"),
    path('api/spacebucks/balance/<int:rfid>/', views.spacebucks_balance, name="spacebucks_balance"),
    path('api/spacebucks/causedonation/<int:rfid>/<int:cause_id>/<int:amount>/', views.spacebucks_cause_donation,
         name="spacebucks_cause_donation"),
    path('api/spacebucks/debit/<int:rfid>/<int:amount>/<str:description>', views.spacebucks_debit,
         name="spacebucks_debit"),
]
