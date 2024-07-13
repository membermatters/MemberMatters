import logging
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Sum
from django.utils import timezone
from prometheus_client import Gauge

from api_metrics.models import Metric
from profile.models import Profile
from memberbucks.models import MemberBucks

logger = logging.getLogger("celery:api_metrics")

member_count_total = Gauge(
    "mm_member_count_total",
    "Number of members in the system",
    ["state"],
)

member_count_6_months_total = Gauge(
    "member_count_6_months_total",
    "Number of members in the system >6 months old",
    ["state"],
)

member_count_12_months_total = Gauge(
    "member_count_12_months_total",
    "Number of members in the system >12 months old",
    ["state"],
)

subscription_count_total = Gauge(
    "mm_subscription_count_total",
    "Number of subscriptions in the system",
    ["state"],
)

memberbucks_balance_total = Gauge(
    "mm_memberbucks_balance_total",
    "Total balance of memberbucks in the system",
)

memberbucks_transactions_total = Gauge(
    "mm_memberbucks_transactions_total",
    "Total balance of memberbucks transactions in the system",
    ["type"],
)


def calculate_member_count():
    # get the count of all the different member profile states
    logger.debug("Calculating member count total")
    profile_states = []

    for state in (
        Profile.objects.values("state").annotate(count=Count("pk")).order_by("count")
    ):
        profile_states.append({"state": state["state"], "total": state["count"]})

    Metric.objects.create(
        name=Metric.MetricName.MEMBER_COUNT_TOTAL,
        data=(
            profile_states if len(profile_states) else [{"state": "active", "total": 0}]
        ),
    ).full_clean()


def calculate_member_count_6_months():
    logger.debug("Calculating member 6 months count total")
    profile_states = []

    for state in (
        Profile.objects.filter(created__lt=timezone.now() + relativedelta(months=-6))
        .values("state")
        .annotate(count=Count("pk"))
        .order_by("count")
    ):
        profile_states.append({"state": state["state"], "total": state["count"]})

    Metric.objects.create(
        name=Metric.MetricName.MEMBER_COUNT_6_MONTHS,
        data=(
            profile_states if len(profile_states) else [{"state": "active", "total": 0}]
        ),
    ).full_clean()


def calculate_member_count_12_months():
    logger.debug("Calculating member 12 months count total")
    profile_states = []

    for state in (
        Profile.objects.filter(created__lt=timezone.now() + relativedelta(months=-12))
        .values("state")
        .annotate(count=Count("pk"))
        .order_by("count")
    ):
        profile_states.append({"state": state["state"], "total": state["count"]})

    Metric.objects.create(
        name=Metric.MetricName.MEMBER_COUNT_12_MONTHS,
        data=(
            profile_states if len(profile_states) else [{"state": "active", "total": 0}]
        ),
    ).full_clean()


def calculate_subscription_count():
    # get the count of all the different subscription states
    logger.debug("Calculating subscription count total")
    subscription_states_data = []
    for state in (
        Profile.objects.values("subscription_status")
        .annotate(count=Count("pk"))
        .order_by("count")
    ):
        subscription_states_data.append(
            {"state": state["subscription_status"], "total": state["count"]}
        )
    Metric.objects.create(
        name=Metric.MetricName.SUBSCRIPTION_COUNT_TOTAL,
        data=(
            subscription_states_data
            if len(subscription_states_data)
            else [{"state": "inactive", "total": 0}]
        ),
    ).full_clean()


def calculate_memberbucks_balance():
    logger.debug("Calculating memberbucks balance total")
    total_balance = Profile.objects.filter(memberbucks_balance__lt=1000).aggregate(
        Sum("memberbucks_balance")
    )
    Metric.objects.create(
        name=Metric.MetricName.MEMBERBUCKS_BALANCE_TOTAL,
        data={"value": total_balance["memberbucks_balance__sum"]},
    ).full_clean()


def calculate_memberbucks_transactions():
    # get the sum of all the different subscription states
    logger.debug("Calculating subscription count total")
    transaction_data = []
    for transaction_type in (
        MemberBucks.objects.filter(amount__lt=1000)
        .values("transaction_type")
        .annotate(amount=Sum("amount"))
        .order_by("-amount")
    ):
        transaction_data.append(
            {
                "type": transaction_type["transaction_type"],
                "total": transaction_type["amount"],
            }
        )
    Metric.objects.create(
        name=Metric.MetricName.MEMBERBUCKS_TRANSACTIONS_TOTAL,
        data=(
            transaction_data
            if len(transaction_data)
            else [{"type": "stripe", "total": 0.0}]
        ),
    ).full_clean()
