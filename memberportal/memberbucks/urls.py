from django.urls import path
from . import views

urlpatterns = [
    path("api/memberbucks/debit/", views.memberbucks_debit, name="memberbucks_debit"),
    path(
        "api/memberbucks/debit/<int:rfid>/<int:amount>/",
        views.memberbucks_debit,
        name="memberbucks_debit",
    ),
    path(
        "api/spacebucks/debit/<int:rfid>/<int:amount>/",
        views.memberbucks_debit,
        name="memberbucks_debit",
    ),
    path(
        "api/memberbucks/balance/<int:rfid>/",
        views.memberbucks_balance,
        name="memberbucks_balance",
    ),
    path(
        "api/spacebucks/balance/<int:rfid>/",
        views.memberbucks_balance,
        name="memberbucks_balance",
    ),
    path(
        "api/memberbucks/groupdonation/<int:rfid>/<int:group_id>/<int:amount>/",
        views.memberbucks_group_donation,
        name="memberbucks_group_donation",
    ),
    path(
        "api/memberbucks/debit/<int:rfid>/<int:amount>/<str:description>",
        views.memberbucks_debit,
        name="memberbucks_debit",
    ),
    path(
        "api/spacebucks/debit/<int:rfid>/<int:amount>/<str:description>",
        views.memberbucks_debit,
        name="memberbucks_debit",
    ),
]
