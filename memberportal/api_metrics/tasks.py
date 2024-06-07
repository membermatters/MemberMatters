from membermatters.celeryapp import app
from api_metrics.metrics import *

import requests
from constance import config
import logging

logger = logging.getLogger("celery:api_metrics")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    if config.METRICS_INTERVAL:
        metrics_interval = config.METRICS_INTERVAL
        if metrics_interval < 3600 * 24:
            logger.warning(
                "METRICS_INTERVAL is less than 24 hours. This is NOT recommended for production and has little benefit."
            )
        if metrics_interval < 60:
            logger.warning(
                "METRICS_INTERVAL is less than 60 seconds, setting to 60 seconds."
            )
            metrics_interval = 60
        sender.add_periodic_task(
            metrics_interval,
            calculate_metrics.s(),
            expires=60,
            name="celery_calculate_metrics",
        )


@app.task
def calculate_metrics():
    logger.info("Calculating metrics!")

    calculate_member_count()
    calculate_member_count_6_months()
    calculate_member_count_12_months()
    calculate_subscription_count()
    calculate_memberbucks_balance()
    calculate_memberbucks_transactions()

    try:
        requests.post(config.SITE_URL + "/api/update-prom-metrics/")

    except Exception as e:
        logger.error(f"Failed to update Prometheus metrics: {e}")
