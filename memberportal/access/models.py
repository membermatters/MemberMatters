import logging
from services.discord import post_door_swipe_to_discord
from services import sms
from profile.models import Profile, log_event
from django.db import models
from datetime import timedelta
from django.utils import timezone
import pytz
from django.conf import settings
from django.contrib import auth
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework_api_key.permissions import BaseHasAPIKey, AbstractAPIKey
from constance import config
import hashlib

logger = logging.getLogger("app")
User = auth.get_user_model()
utc = pytz.UTC


class AccessControlledDeviceAPIKey(AbstractAPIKey):
    class Meta:
        # Add verbose name
        verbose_name = "API Key For Access Controlled Device"

    pass


class HasAccessControlledDeviceAPIKey(BaseHasAPIKey):
    model = AccessControlledDeviceAPIKey


class ExternalAccessControlAPIKey(AbstractAPIKey):
    class Meta:
        # Add verbose name
        verbose_name = "API Key For External Access Control API"

    pass


class HasExternalAccessControlAPIKey(BaseHasAPIKey):
    model = ExternalAccessControlAPIKey


class AccessControlledDevice(models.Model):
    id = models.AutoField(primary_key=True)
    authorised = models.BooleanField(
        "Is this device authorised to access the system?", default=False
    )
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

    def log_access(self, member_id, success=True):
        pass

    def sync(self, request=None):
        if self.serial_number:
            logger.info(
                "Sending device sync to channels for {}".format(self.serial_number)
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                self.serial_number, {"type": "sync_users"}
            )

            if request:
                request.user.log_event(
                    f"Sent a sync request to the {self.name} {self._meta.verbose_name}.",
                    "admin",
                )

            return True

        else:
            logger.error(
                "Cannot sync device without websocket support (for {})!".format(
                    self.name
                )
            )

    def reboot(self, request=None):
        if self.serial_number:
            logger.info(f"Sending door reboot to channels for {self.name}")

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                self.serial_number, {"type": "device_reboot"}
            )

            if request:
                request.user.log_event(
                    f"Sent a reboot request to the {self.name} {self._meta.verbose_name}.",
                    "admin",
                )

        else:
            logger.error(
                "Cannot reboot device without websocket support (for {})!".format(
                    self.name
                )
            )

    def get_tags(self):
        # Find profiles that are active and have an RFID tag assigned to them
        ProfileQueryset = Profile.objects.filter(state="active").exclude(
            rfid__isnull=True
        )
        authorised_tags = list()

        # Get the device object
        if self.type == "door":
            ProfileQueryset = ProfileQueryset.filter(doors__in=[self])
        elif self.type == "interlock":
            ProfileQueryset = ProfileQueryset.filter(interlocks__in=[self])
        elif self.type == "memberbucks":
            pass
            # all profiles are authorised for memberbucks devices
        else:
            raise Exception("Unknown device type")

        for profile in ProfileQueryset.all():
            # If the site sign in feature is disabled, or the device is exempt
            # from sign in, then all tags are authorised.
            # Otherwise check if the member is signed in to the site
            if config.ENABLE_PORTAL_SITE_SIGN_IN == False or (
                self.exempt_signin is True or profile.is_signed_into_site()
            ):
                authorised_tags.append(profile.rfid)

        return (
            authorised_tags,
            hashlib.md5(str(authorised_tags).encode("utf-8")).hexdigest(),
        )


class MemberbucksDevice(AccessControlledDevice):
    all_members = False
    type = "memberbucks"

    def lock(self):
        return False

    def unlock(self):
        return False


class Doors(AccessControlledDevice):
    type = "door"

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
                self.serial_number, {"type": "door_bump"}
            )

            if request:
                self.log_access(request.user.id)
                request.user.log_event(
                    f"Bumped the {self.name} {self._meta.verbose_name}.",
                    "admin",
                )

            else:
                log_event(
                    f"Unknown user (system) bumped the {self.name} {self._meta.verbose_name}.",
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

        if success == True:
            if self.post_to_discord:
                post_door_swipe_to_discord(profile.get_full_name(), self.name, success)

        elif success == False:
            sms_message = sms.SMS()
            sms_message.send_inactive_swipe_alert(profile.phone)

        elif success == "locked out":
            post_door_swipe_to_discord(
                profile.get_full_name(), self.name, "maintenance_lock_out"
            )

            sms_message = sms.SMS()
            sms_message.send_locked_out_swipe_alert(profile.phone)

        return door_log


class Interlock(AccessControlledDevice):
    type = "interlock"

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
