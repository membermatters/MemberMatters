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
from django.core.validators import URLValidator
from django_prometheus.models import ExportModelOperationsMixin
import access.metrics as metrics

logger = logging.getLogger("access")
User = auth.get_user_model()
utc = pytz.UTC


class AccessControlledDeviceAPIKey(AbstractAPIKey):
    class Meta:
        # Add verbose name
        verbose_name = "API Key For Access Controlled Device"
        app_label = "access"


class HasAccessControlledDeviceAPIKey(BaseHasAPIKey):
    model = AccessControlledDeviceAPIKey


class ExternalAccessControlAPIKey(AbstractAPIKey):
    class Meta:
        # Add verbose name
        verbose_name = "API Key For External Access Control API"

    pass


class HasExternalAccessControlAPIKey(BaseHasAPIKey):
    model = ExternalAccessControlAPIKey


class AccessControlledDevice(
    ExportModelOperationsMixin("access-controlled-device"), models.Model
):
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
    play_theme = models.BooleanField("Play theme on successful swipe", default=False)
    post_to_discord = models.BooleanField("Post to discord on swipe", default=True)
    exempt_signin = models.BooleanField(
        "Exempt this device from requiring a sign in", default=False
    )
    report_online_status = models.BooleanField(
        "Report the online status of this device and fail the uptime check if it's offline.",
        default=True,
    )
    hidden = models.BooleanField(
        "Hidden from members in their access permissions screen", default=False
    )

    type = "unknown"

    def get_metrics_labels(self):
        return {
            "type": self.type,
            "id": self.id,
            "name": self.name,
        }

    def checkin(self):
        self.last_seen = timezone.now()
        self.save(update_fields=["last_seen"])
        metrics.device_checkins_total.labels(**self.get_metrics_labels()).inc()

    def get_unavailable(self):
        if self.last_seen:
            if timezone.now() - timedelta(minutes=3) > self.last_seen:
                return True

        return False

    def __str__(self):
        return self.name

    def log_access(self, member_id, success=True):
        metrics.device_access_successes_total.labels(**self.get_metrics_labels()).inc()

    def log_event(self, description=None, data=None):
        if self.type == "door":
            log_event(description=description, event_type="door", data=data, door=self)
            return True
        elif self.type == "interlock":
            log_event(
                description=description,
                event_type="interlock",
                data=data,
                interlock=self,
            )
            return True
        elif self.type == "memberbucks":
            log_event(
                description=description,
                event_type="memberbucksdevice",
                data=data,
                memberbucks_device=self,
            )
            return True

    def log_connected(self):
        self.log_event(
            description=f"Device connected.",
        )
        metrics.device_connections_total.labels(**self.get_metrics_labels()).inc()

    def log_disconnected(self):
        self.log_event(
            description=f"Device disconnected.",
        )
        metrics.device_disconnections_total.labels(**self.get_metrics_labels()).inc()

    def log_authenticated(self):
        self.log_event(
            description=f"Device authenticated.",
        )
        metrics.device_authentications_total.labels(**self.get_metrics_labels()).inc()

    def log_force_rebooted(self):
        self.log_event(
            description=f"Device manually rebooted.",
        )
        metrics.device_force_reboots_total.labels(**self.get_metrics_labels()).inc()

    def log_force_sync(self):
        self.log_event(
            description=f"Device manually synced.",
        )
        metrics.device_syncs_total.labels(**self.get_metrics_labels()).inc()

    def log_force_bump(self):
        self.log_event(
            description=f"Device manually bumped.",
        )
        metrics.device_force_bumps_total.labels(**self.get_metrics_labels()).inc()

    def log_force_lock(self):
        self.log_event(
            description=f"Device manually locked.",
        )
        metrics.device_force_locks_total.labels(**self.get_metrics_labels()).inc()

    def log_force_unlock(self):
        self.log_event(
            description=f"Device manually unlocked.",
        )
        metrics.device_force_unlocks_total.labels(**self.get_metrics_labels()).inc()

    def sync(self, request=None):
        logger.info("Sending device sync to channels for {}".format(self.serial_number))

        if self.serial_number:
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

    def lock(self, request=None):
        logger.info(f"Sending device lock to channels for {self.name}")

        if self.serial_number:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                self.serial_number, {"type": "device_lock"}
            )

            if request:
                request.user.log_event(
                    f"Sent a lock request to the {self.name} {self._meta.verbose_name}.",
                    "admin",
                )

    def unlock(self, request=None):
        logger.info(f"Sending device unlock to channels for {self.name}")

        if self.serial_number:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                self.serial_number, {"type": "device_unlock"}
            )

            if request:
                request.user.log_event(
                    f"Sent an unlock request to the {self.name} {self._meta.verbose_name}.",
                    "admin",
                )

    def reboot(self, request=None):
        logger.info(f"Sending door reboot to channels for {self.name}")

        if self.serial_number:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                self.serial_number, {"type": "device_reboot"}
            )

            if request:
                request.user.log_event(
                    f"Sent a reboot request to the {self.name} {self._meta.verbose_name}.",
                    "admin",
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


class MemberbucksDevice(
    ExportModelOperationsMixin("memberbucks-device"), AccessControlledDevice
):
    all_members = True
    type = "memberbucks"

    class Meta:
        verbose_name = "Memberbucks Device"
        verbose_name_plural = "Memberbucks Devices"


class Doors(ExportModelOperationsMixin("door"), AccessControlledDevice):
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

        metrics.device_force_bumps_total.labels(**self.get_metrics_labels()).inc()
        return False

    def log_access(self, member_id, success=True):
        logger.debug("Logging access for {}".format(self.name))

        user_object = User.objects.get(pk=member_id)
        door_log = DoorLog.objects.create(
            user=user_object, door=self, success=success is True
        )
        profile = user_object.profile
        profile.last_seen = timezone.now()
        profile.save()

        if success is True:
            metrics.device_access_successes_total.labels(
                **self.get_metrics_labels()
            ).inc()
            if self.post_to_discord:
                post_door_swipe_to_discord(profile.get_full_name(), self.name, success)

        elif success == "locked_out":
            metrics.device_access_failures_total.labels(
                **self.get_metrics_labels()
            ).inc()
            post_door_swipe_to_discord(profile.get_full_name(), self.name, "locked_out")

            sms_message = sms.SMS()
            sms_message.send_locked_out_swipe_alert(profile.phone)

        elif not success:
            metrics.device_access_failures_total.labels(
                **self.get_metrics_labels()
            ).inc()
            if self.post_to_discord:
                post_door_swipe_to_discord(
                    profile.get_full_name(), self.name, "rejected"
                )
            sms_message = sms.SMS()
            sms_message.send_inactive_swipe_alert(profile.phone)

        return door_log


class Interlock(ExportModelOperationsMixin("interlock"), AccessControlledDevice):
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

    def log_access(self, user, log_type="activated"):
        logger.debug("Logging access for {}".format(self.name))

        profile = user.profile
        profile.last_seen = timezone.now()
        profile.save()

        if self.post_to_discord:
            post_interlock_swipe_to_discord(
                profile.get_full_name(), self.name, type=log_type
            )

        if log_type == "activated":
            metrics.device_interlock_session_activations_total.labels(
                **self.get_metrics_labels()
            ).inc()
            return True

        elif log_type == "left_on":
            metrics.device_interlock_sessions_left_on_total.labels(
                **self.get_metrics_labels()
            ).inc()
            return True

        elif log_type == "deactivated":
            metrics.device_interlock_sessions_deactivated_total.labels(
                **self.get_metrics_labels()
            ).inc()
            return True

        elif log_type == "rejected":
            sms_message = sms.SMS()
            sms_message.send_inactive_swipe_alert(profile.phone)

        elif log_type == "locked_out":
            sms_message = sms.SMS()
            sms_message.send_locked_out_swipe_alert(profile.phone)

        elif log_type == "not_signed_in":
            pass

        metrics.device_interlock_sessions_rejected_total.labels(
            **self.get_metrics_labels()
        ).inc()
        self.session_rejected(user, reason=log_type)
        return True


class DoorLog(ExportModelOperationsMixin("door-log"), models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.profile.screen_name}) swiped at {self.door.name} {'successfully' if self.success else 'unsuccessfully'} on {self.date.date()}"


class InterlockLog(ExportModelOperationsMixin("interlock-log"), models.Model):
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

    def __str__(self):
        return f"{self.user_started.get_full_name()} ({self.user_started.profile.screen_name}) swiped at {self.interlock.name} {'successfully' if self.success else 'unsuccessfully'} for {round(self.total_time.total_seconds() / 60)} mins at {self.date_started.date()}"

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

        metrics.device_interlock_sessions_cost_cents.labels(
            **self.interlock.get_metrics_labels()
        ).inc(self.total_cost)
        metrics.device_interlock_session_duration_seconds.labels(
            **self.interlock.get_metrics_labels()
        ).observe(self.total_time.total_seconds())

        if skip_cost or self.total_time.total_seconds() < 10:
            self.total_cost = 0
            self.save()
            return True

        else:
            minutes = round(self.total_time.total_seconds() / 60)
            description = f"For using {self.interlock.name} for {minutes} minutes."
            MemberBucks.objects.create(
                user=self.user_started,
                amount=(self.total_cost / 100) * -1,
                transaction_type="interlock",
                description=description,
            )

            return True
