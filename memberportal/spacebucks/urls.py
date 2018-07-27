from django.urls import path
from . import views

urlpatterns = [
    path('profile/spacebucks/history/',
         views.manage_spacebucks, name='manage_spacebucks'),
    path('profile/spacebucks/add/',
         views.add_spacebucks, name='add_spacebucks'),
    path('profile/spacebucks/add/<int:amount>',
         views.add_spacebucks, name='add_spacebucks'),
    path('profile/spacebucks/paymentdetails/save/',
         views.add_spacebucks_payment_info,
         name='add_spacebucks_payment_info'),
    path('profile/spacebucks/paymentdetails/delete/',
         views.delete_spacebucks_payment_info,
         name='delete_spacebucks_payment_info'),
    path('api/spacebucks/debit/',
         views.spacebucks_debit, name="spacebucks_debit"),
]
