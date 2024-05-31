import os
from celery import Celery, signals
from prometheus_client import CollectorRegistry, multiprocess, start_http_server
import logging

logger = logging.getLogger("celery:celeryapp")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "membermatters.settings")

app = Celery("membermatters")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logger.debug(f"Request: {self.request!r}")
    print(f"Request: {self.request!r}")


@signals.celeryd_init.connect
def name_this_what_you_want(sender=None, conf=None, **kwargs):
    logger.debug(
        "Starting CollectorRegistry() and multiprocess.MultiProcessCollector()..."
    )
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)

    logger.debug("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000, registry=registry)
    logger.info("Prometheus metrics server started on port 8000!")
