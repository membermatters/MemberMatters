from api_metrics.models import Metric
from profile.models import Profile
from membermatters.celeryapp import app

import requests
from django.db.models import Count
from constance import config
import logging

logger = logging.getLogger("celery:api_metrics")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        config.METRICS_INTERVAL,
        calculate_metrics.s(),
        expires=30,
        name="celery_calculate_metrics",
    )


@app.task
def calculate_metrics():
    logger.info("Calculating metrics!")

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

    try:
        requests.post(config.SITE_URL + "/api/update-prom-metrics/")

    except Exception as e:
        logger.error(f"Failed to update Prometheus metrics: {e}")

    return {
        "member_count": Profile.objects.count(),
        "subscription_count": Profile.objects.filter(
            subscription_status__in=["active", "cancelling"]
        ).count(),
    }
