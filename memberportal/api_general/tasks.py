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

    # get the count of all the different subscription states
    logger.debug("Calculating subscription count total")
    subscription_states = (
        Profile.objects.all()
        .values("subscription_status")
        .annotate(total=Count("subscription_status"))
        .order_by("total")
    )
    # TODO: store the last X months in the database too
    for state in subscription_states:
        logger.debug(f"State: {state['subscription_status']} - Total: {state['total']}")
        metrics.subscription_count_total.labels(state=state["subscription_status"]).set(
            state["total"]
        )
