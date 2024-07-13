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
    path(
        "api/memberbucks/add/<int:amount>/",
        views.MemberBucksAddFunds.as_view(),
        name="MemberBucksAddFunds",
    ),
    path(
        "api/memberbucks/pay/<int:amount>/",
        views.MemberBucksDonateFunds.as_view(),
        name="MemberBucksDonateFunds",
    ),
    path(
        "api/memberbucks/balance-list/",
        views.GetMemberbucksBalanceList.as_view(),
        name="GetMemberbucksBalanceList",
    ),
]
