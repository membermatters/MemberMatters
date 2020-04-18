from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/memberbucks/transactions/",
        views.MemberBucksTransactions.as_view(),
        name="MemberBucksTransactions",
    ),
    path(
        "api/memberbucks/balance/",
        views.MemberBucksBalance.as_view(),
        name="MemberBucksBalance",
    ),
]
