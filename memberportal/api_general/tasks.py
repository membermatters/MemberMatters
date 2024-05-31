import api_general.metrics as metrics
from profile.models import Profile
from membermatters.celeryapp import app

from django.db.models import Count
from constance import config
import logging

logger = logging.getLogger("celery:api_general")


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
    metric_results = {
        "member_count": [],
        "subscription_count": [],
    }

    # get the count of all the different member profile states
    logger.debug("Calculating member count total")
    profile_states = (
        Profile.objects.all()
        .values("state")
        .annotate(total=Count("state"))
        .order_by("total")
    )
    # TODO: store the last X months in the database too
    for state in profile_states:
        logger.debug(f"State: {state['state']} - Total: {state['total']}")
        metrics.member_count_total.labels(state=state["state"]).set(state["total"])
        metric_results["member_count"].append(
            {"state": state["state"], "total": state["total"]}
        )

    # get the count of all the different subscription states
    logger.debug("Calculating subscription count total")
    subscription_states = (
        Profile.objects.all()
        .values("subscription_status")
        .annotate(total=Count("subscription_status"))
        .order_by("total")
    )
    # TODO: store the last X months in the database too
    for status in subscription_states:
        logger.debug(
            f"State: {status['subscription_status']} - Total: {status['total']}"
        )
        metrics.subscription_count_total.labels(
            status=status["subscription_status"]
        ).set(status["total"])
        metric_results["subscription_count"].append(
            {"status": status["subscription_status"], "total": status["total"]}
        )

    return metric_results
