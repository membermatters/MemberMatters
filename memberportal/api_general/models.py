from django.db import models
from datetime import timedelta
from django.utils import timezone
import pytz
from django.contrib import auth

User = auth.get_user_model()
utc = pytz.UTC


class Kiosk(models.Model):
    name = models.CharField("Name", max_length=30, unique=True)
    kiosk_id = models.CharField("Kiosk Id", max_length=70, unique=True)
    ip_address = models.GenericIPAddressField(
        "IP Address of device", unique=True, null=True, blank=True
    )
    last_seen = models.DateTimeField(null=True)
    play_theme = models.BooleanField("Play theme on door swipe", default=False)
    authorised = models.BooleanField("Is this kiosk authorised?", default=False)

    def checkin(self):
        self.last_seen = timezone.now()
        self.save()

    def get_unavailable(self):
        if self.last_seen:
            if timezone.now() - timedelta(minutes=5) > self.last_seen:
                return True

        return False

    def __str__(self):
        return self.name
