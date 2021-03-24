from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/memberbucks/debit/",
        views.MemberbucksDebit.as_view(),
        name="memberbucks_debit",
    ),
    path(
        "api/memberbucks/debit/<int:rfid>/<int:amount>/",
        views.MemberbucksDebit.as_view(),
        name="memberbucks_debit",
    ),
    path(
        "api/spacebucks/debit/<int:rfid>/<int:amount>/",
        views.MemberbucksDebit.as_view(),
        name="memberbucks_debit",
    ),
    path(
        "api/memberbucks/debit/<int:rfid>/<int:amount>/<str:description>",
        views.MemberbucksDebit.as_view(),
        name="memberbucks_debit",
    ),
    path(
        "api/spacebucks/debit/<int:rfid>/<int:amount>/<str:description>",
        views.MemberbucksDebit.as_view(),
        name="memberbucks_debit",
    ),
    path(
        "api/memberbucks/balance/<int:rfid>/",
        views.MemberbucksBalance.as_view(),
        name="memberbucks_balance",
    ),
    path(
        "api/spacebucks/balance/<int:rfid>/",
        views.MemberbucksBalance.as_view(),
        name="memberbucks_balance",
    ),
]
