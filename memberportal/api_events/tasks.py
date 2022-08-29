from membermatters.celeryapp import app
from api_events.models import create_or_update_event_from_ical
import json
from constance import config
from icalevents.icalevents import events

import logging

logger = logging.getLogger("app")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        5 * 60.0, update_ical_feeds.s(), expires=30, name="update_ical_feeds"
    )


@app.task
def update_ical_feeds():
    logger.info("Fetching / updating iCal feeds!")

    feed_urls = json.loads(config.ICAL_FEEDS)

    for feed_url in feed_urls:
        logger.info("Fetching: " + feed_url)
        fetched_events = events(feed_url)
        logger.info(f"Got {len(fetched_events)} events from {feed_url}")

        for fetched_event in fetched_events:
            create_or_update_event_from_ical(fetched_event)
