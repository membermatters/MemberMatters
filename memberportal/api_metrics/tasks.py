from membermatters.celeryapp import app
from api_metrics.metrics import *

import requests
from constance import config
import logging

logger = logging.getLogger("celery:api_metrics")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        config.METRICS_INTERVAL,
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

    try:
        requests.post(config.SITE_URL + "/api/update-prom-metrics/")

    except Exception as e:
        logger.error(f"Failed to update Prometheus metrics: {e}")
