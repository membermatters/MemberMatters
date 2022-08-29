from django.db import models
from django.utils import timezone
import pytz
from uuid import uuid4

import logging

logger = logging.getLogger("app")

utc = pytz.UTC


EVENT_SOURCE_CHOICES = (("ical", "iCal Calendar Feed"), ("other", "Other Source"))


class Event(models.Model):
    id = models.AutoField(primary_key=True)  # internal event ID
    name = models.TextField(
        "Name",
    )
    description = models.TextField("Description", default="")
    location = models.TextField("Location", default="")
    source = models.CharField(
        max_length=30, choices=EVENT_SOURCE_CHOICES, default="other"
    )
    hidden = models.BooleanField(default=False)  # hidden from members
    paid = models.BooleanField(default=False)  # if the event is a paid event

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    uid_external = models.TextField(
        unique=True, default=uuid4
    )  # external uid (such as from ical)
    repeat_rule_ical = models.TextField(
        "Repeat Rule (iCal)", null=True, blank=True, default=None
    )

    # when the system updated this event
    _created = models.DateTimeField(default=timezone.now)
    _updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name[:50]  # cut off after 50 characters


def create_or_update_event_from_ical(ical_event):
    required_attributes = [
        "uid",
        "summary",
        "description",
        "start",
        "end",
        "created",
        "last_modified",
    ]
    missing_attributes = []

    for attr in required_attributes:
        attr_value = getattr(ical_event, attr, None)

        if attr_value is None:
            missing_attributes.append(attr)

    if len(missing_attributes):
        logger.error(
            "Failed to parse event with missing required attributes: "
            + ", ".join(missing_attributes)
        )
        return None

    else:
        # we have all the attributes that we need!
        existing_event = Event.objects.filter(uid_external=ical_event.uid).first()

        if existing_event:
            logger.info("Updating existing event: " + ical_event.uid)
            existing_event.name = ical_event.summary
            existing_event.description = ical_event.description
            existing_event.start_time = ical_event.start
            existing_event.end_time = ical_event.end
            existing_event.updated = ical_event.last_modified
            existing_event.save()

            return existing_event

        else:
            event = Event(
                name=ical_event.summary,
                description=ical_event.description,
                start_time=ical_event.start,
                end_time=ical_event.end,
                created=ical_event.created,
                updated=ical_event.last_modified,
                uid_external=ical_event.uid,
            )

            # save and return the new event
            event.save()
            return event
