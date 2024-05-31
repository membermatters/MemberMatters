from api_metrics.models import Metric
from profile.models import Profile
from membermatters.celeryapp import app

import requests
from django.db.models import Count
from constance import config
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    profile_states = (
        Profile.objects.all()
        .values("state")
        .annotate(total=Count("state"))
        .order_by("total")
    )
    profile_states_data = [
        f"{item['state']}: {item['total']}" for item in profile_states
    ]
    Metric.objects.create(
        name=Metric.MetricName.MEMBER_COUNT_TOTAL, data=profile_states_data
    ).full_clean()

    # get the count of all the different subscription states
    logger.debug("Calculating subscription count total")
    subscription_states = (
        Profile.objects.all()
        .values("subscription_status")
        .annotate(total=Count("subscription_status"))
        .order_by("total")
    )
    subscription_states_data = [
        f"{item['subscription_status']}: {item['total']}"
        for item in subscription_states
    ]
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
