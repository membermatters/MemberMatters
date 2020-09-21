from django.db import models
from datetime import timedelta
from django.utils import timezone
import pytz
from django.conf import settings
from uuid import uuid4

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


class SiteSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    signin_date = models.DateTimeField(default=timezone.now)
    signout_date = models.DateTimeField(null=True, blank=True)
    guests = models.TextField(default="[]")

    def signout(self):
        self.signout_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.profile.get_full_name()} - in: {self.signin_date} out: {self.signout_date}"


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    verification_token = models.UUIDField(default=uuid4)
