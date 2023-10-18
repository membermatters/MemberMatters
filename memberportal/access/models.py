import logging
from services.discord import post_door_swipe_to_discord, post_interlock_swipe_to_discord
from services import sms
from profile.models import Profile, log_event
from memberbucks.models import MemberBucks
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
        "IP Address of device", null=True, blank=True
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

    def log_event(self, description=None, event_type=None, data=None):
        if self.type == "door":
            log_event(
                description=description, event_type=event_type, data=data, door=self
            )
            return True
        elif self.type == "interlock":
            log_event(
                description=description,
                event_type=event_type,
                data=data,
                interlock=self,
            )
            return True
        elif self.type == "memberbucks":
            log_event(
                description=description,
                event_type=event_type,
                data=data,
                memberbucks_device=self,
            )
            return True

    def log_connected(self):
        self.log_event(
            description=f"Device connected.",
        )

    def log_disconnected(self):
        self.log_event(
            description=f"Device disconnected.",
        )

    def log_authenticated(self):
        self.log_event(
            description=f"Device authenticated.",
        )

    def log_force_rebooted(self):
        self.log_event(
            description=f"Device manually rebooted.",
        )

    def log_force_sync(self):
        self.log_event(
            description=f"Device manually synced.",
        )

    def log_force_bump(self):
        self.log_event(
            description=f"Device manually bumped.",
        )

    def sync(self, request=None):
        if self.type != "door":
            logger.debug(
                "Cannot sync device that is not a door (for {})!".format(self.name)
            )
            return True

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


class Doors(AccessControlledDevice):
    type = "door"

    class Meta:
        verbose_name = "Door"
        verbose_name_plural = "Doors"
        permissions = [
            ("manage_doors", "Can manage doors"),
        ]

    def bump(self, request=None):
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
            if self.post_to_discord:
                post_door_swipe_to_discord(
                    profile.get_full_name(), self.name, "rejected"
                )
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

    cost_per_session = models.IntegerField(
        "Fixed cost per session (in cents)", default=0
    )
    cost_per_hour = models.IntegerField("Cost per hour (in cents)", default=0)
    cost_per_kwh = models.IntegerField("Cost per kWh (in cents)", default=0)

    def get_active_sessions(self):
        return InterlockLog.objects.filter(interlock=self, date_ended=None).all()

    def session_start(self, user):
        self.session_end_all(reason="new_session")
        return InterlockLog.objects.create(interlock=self, user_started=user)

    def session_rejected(self, user, reason):
        active_sessions = self.get_active_sessions()
        for session in active_sessions:
            session.session_end(user)

        session = InterlockLog.objects.create(
            interlock=self, user_started=user, success=False, reason=reason
        )
        session.session_end(user, skip_cost=True)
        return session

    def session_end_all(self, reason="timeout"):
        active_sessions = self.get_active_sessions()
        for session in active_sessions:
            session.session_end(None)

    def log_access(self, user, type="activated"):
        logger.debug("Logging access for {}".format(self.name))

        profile = user.profile
        profile.last_seen = timezone.now()
        profile.save()

        if self.post_to_discord:
            post_interlock_swipe_to_discord(
                profile.get_full_name(), self.name, type=type
            )

        if type == "activated":
            return True

        elif type == "left_on":
            return True

        elif type == "deactivated":
            return True

        elif type == "rejected":
            sms_message = sms.SMS()
            sms_message.send_inactive_swipe_alert(profile.phone)

        elif type == "maintenance_lock_out":
            sms_message = sms.SMS()
            sms_message.send_locked_out_swipe_alert(profile.phone)

        elif type == "not_signed_in":
            pass

        self.session_rejected(user, reason=type)
        return True


class DoorLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=True)


class InterlockLog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    interlock = models.ForeignKey(Interlock, on_delete=models.CASCADE)
    user_started = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_ended = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_ended",
    )
    success = models.BooleanField(default=True)
    reason = models.CharField(max_length=100, blank=True, null=True)

    date_started = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(default=timezone.now)
    date_ended = models.DateTimeField(default=None, blank=True, null=True)

    total_time = models.DurationField(default=timedelta(0))
    total_kwh = models.FloatField(default=None, blank=True, null=True)
    total_cost = models.FloatField(default=None, blank=True, null=True)

    def calculate_cost(self):
        total_cost = self.interlock.cost_per_session

        if self.interlock.cost_per_hour:
            total_cost += (
                self.total_time.total_seconds() / 3600 * self.interlock.cost_per_hour
            )
        if self.interlock.cost_per_kwh:
            total_cost += (self.total_kwh or 0) * (self.interlock.cost_per_kwh or 0)

        return round(total_cost)

    def session_update(self, kwh=None):
        self.date_updated = timezone.now()
        self.total_time = self.date_updated - self.date_started
        self.interlock.checkin()
        self.total_cost = self.calculate_cost()

        if kwh:
            self.total_kwh = kwh

        self.save()

        return True

    def session_end(self, user=None, kwh=None, skip_cost=False):
        self.session_update(kwh)
        self.user_ended = user
        self.date_ended = timezone.now()
        self.save()

        if skip_cost:
            return True

        else:
            minutes = round(self.total_time.total_seconds() / 60)
            description = f"For using {self.interlock.name} for {minutes} minutes."
            transaction = MemberBucks.objects.create(
                user=self.user_started,
                amount=(self.total_cost / 100) * -1,
                transaction_type="interlock",
                description=description,
            )

            return True
