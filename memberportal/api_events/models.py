from django.db import models
from django.utils import timezone
import pytz
from uuid import uuid4

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
    # external updated timestamp (such as from ical)
    date_updated_external = models.DateTimeField(default=timezone.now)
    repeat_rule_ical = models.TextField(
        "Repeat Rule (iCal)", null=True, blank=True, default=None
    )

    def __str__(self):
        return self.name[:50]  # cut off after 50 characters
