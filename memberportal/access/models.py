import logging

from profile.models import log_event

logger = logging.getLogger("app")

from django.db import models
from datetime import timedelta
from django.utils import timezone
import pytz
from django.conf import settings
from django.contrib import auth
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = auth.get_user_model()
utc = pytz.UTC


class AccessControlledDevice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=30, unique=True)
    description = models.CharField("Description/Location", max_length=100)
    ip_address = models.GenericIPAddressField(
        "IP Address of device", unique=True, null=True, blank=True
    )
    serial_number = models.CharField(
        "Serial Number", max_length=50, unique=True, null=True, blank=True
    )
    last_seen = models.DateTimeField(null=True, blank=True)
    all_members = models.BooleanField("Members have access by default", default=False)
    locked_out = models.BooleanField("Maintenance lockout enabled", default=False)
    play_theme = models.BooleanField("Play theme on door swipe", default=False)
    post_to_discord = models.BooleanField("Post to discord on door swipe", default=True)
    exempt_signin = models.BooleanField(
        "Exempt this device from requiring a sign in", default=False
    )
    report_online_status = models.BooleanField(
        "Report the online status of this device.", default=True
    )
    hidden = models.BooleanField(
        "Hidden from members in their access permissions screen", default=False
    )

    def checkin(self):
        self.last_seen = timezone.now()
        self.save(update_fields=["last_seen"])

    def get_unavailable(self):
        if self.last_seen:
            if timezone.now() - timedelta(minutes=3) > self.last_seen:
                return True

        return False

    def __str__(self):
        return self.name

    def sync(self):
        if self.serial_number:
            logger.info(
                "Sending door sync to channels for {}".format(
                    "door_" + self.serial_number
                )
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "door_" + self.serial_number, {"type": "sync_users"}
            )

            return True

        else:
            logger.error(
                "Cannot sync door without websocket support (for {})!".format(self.name)
            )

    def reboot(self):
        if self.serial_number:
            logger.info(
                "Sending door reboot to channels for {}".format(
                    "door_" + self.serial_number
                )
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "door_" + self.serial_number, {"type": "device_reboot"}
            )

        else:
            logger.error(
                "Cannot sync door without websocket support (for {})!".format(self.name)
            )


class MemberbucksDevice(AccessControlledDevice):
    all_members = False

    def lock(self):
        return False

    def unlock(self):
        return False


class Doors(AccessControlledDevice):
    class Meta:
        verbose_name = "Door"
        verbose_name_plural = "Doors"
        permissions = [
            ("manage_doors", "Can manage doors"),
        ]

    def unlock(self, request=None):
        if self.serial_number:
            logger.info(f"Sending door bump to channels for {self.name}")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "door_" + self.serial_number, {"type": "door_bump"}
            )

            if request:
                self.log_access(request.user.id)
                request.user.log_event(
                    f"Bumped the {self.name} {self.Meta.verbose_name}.",
                    "admin",
                )

            else:
                log_event(
                    f"Unknown user (system) bumped the {self.name} {self.Meta.verbose_name}.",
                    "admin",
                )

            return True

        return False

    def log_access(self, member_id, success=True):
        logger.debug("Logging access for {}".format(self.name))

        user_object = User.objects.get(pk=member_id)
        door_log = DoorLog.objects.create(user=user_object, door=self, success=success)

        profile = user_object.profile
        profile.last_seen = timezone.now()
        profile.save()

        return door_log


class Interlock(AccessControlledDevice):
    class Meta:
        permissions = [
            ("manage_interlocks", "Can manage interlocks"),
        ]

    def lock(self):
        import requests

        r = requests.get("http://{}/end".format(self.ip_address), timeout=10)
        if r.status_code == 200:
            log_event(
                self.name + " locked from admin interface.",
                "interlock",
                "Status: {}. Content: {}".format(r.status_code, r.content),
            )
            return True
        else:
            log_event(
                self.name + " lock request from admin interface failed.",
                "interlock",
                "Status: {}. Content: {}".format(r.status_code, r.content),
            )
            return False

    def create_session(self, user):
        session = InterlockLog.objects.create(
            id=uuid.uuid4(),
            user=user,
            interlock=self,
            first_heartbeat=timezone.now(),
            last_heartbeat=timezone.now(),
        )

        if session:
            return session

        return False

    def get_last_active(self):
        interlocklog = InterlockLog.objects.filter(interlock=self).latest(
            "last_heartbeat"
        )
        return interlocklog.last_heartbeat


class DoorLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=True)


class InterlockLog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_off = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_off",
    )
    interlock = models.ForeignKey(Interlock, on_delete=models.CASCADE)
    first_heartbeat = models.DateTimeField(default=timezone.now)
    last_heartbeat = models.DateTimeField(default=timezone.now)
    session_complete = models.BooleanField(default=False)

    def heartbeat(self):
        self.last_heartbeat = timezone.now()
        self.interlock.checkin()
        self.save()
