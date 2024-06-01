import logging
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.utils import timezone
from prometheus_client import Gauge

from api_metrics.models import Metric
from profile.models import Profile

logger = logging.getLogger("celery:api_metrics")

member_count_total = Gauge(
    "mm_member_count_total",
    "Number of members in the system",
    ["state"],
)

member_6_months_count_total = Gauge(
    "mm_member_6_months_count_total",
    "Number of members in the system >6 months old",
    ["state"],
)

member_12_months_count_total = Gauge(
    "mm_member_12_months_count_total",
    "Number of members in the system >12 months old",
    ["state"],
)

subscription_count_total = Gauge(
    "mm_subscription_count_total",
    "Number of subscriptions in the system",
    ["state"],
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
        name=Metric.MetricName.MEMBER_COUNT_TOTAL, data=profile_states
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
        name=Metric.MetricName.MEMBER_COUNT_6_MONTHS, data=profile_states
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
        name=Metric.MetricName.MEMBER_COUNT_12_MONTHS, data=profile_states
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
        data=subscription_states_data,
    ).full_clean()
