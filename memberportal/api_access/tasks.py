from membermatters.celeryapp import app
from celery.schedules import crontab


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, heartbeat_logger.s(), name="celery_heartbeat_logger")


@app.task
def heartbeat_logger():
    print("Celery is alive!")
