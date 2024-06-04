from celery import signals
import logging

logger = logging.getLogger("api_general:tasks")


@signals.task_failure.connect
@signals.task_revoked.connect
def on_task_failure(**kwargs):
    """Abort transaction on task errors."""
    # celery exceptions will not be published to `sys.excepthook`. therefore we have to create another handler here.
    from traceback import format_tb

    logger.error(
        "[task:%s:%s]"
        % (
            kwargs.get("task_id"),
            kwargs["sender"].request.correlation_id,
        )
        + "\n"
        + "".join(format_tb(kwargs.get("traceback", [])))
        + "\n"
        + str(kwargs.get("exception", ""))
    )
