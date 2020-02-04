from django.db import models
from datetime import timedelta
from django.utils import timezone
from membermatters.helpers import log_event
from django.contrib.auth import get_user_model
import pytz
from django.conf import settings
from django.contrib import auth
import uuid
User = auth.get_user_model()
utc = pytz.UTC


class AccessControlledDevice(models.Model):
    name = models.CharField("Name", max_length=30, unique=True)
    description = models.CharField("Description/Location", max_length=100)
    ip_address = models.GenericIPAddressField("IP Address of device", unique=True, null=True, blank=True)
    last_seen = models.DateTimeField(null=True)
    all_members = models.BooleanField("Members have access by default", default=False)
    locked_out = models.BooleanField("Maintenance lockout enabled", default=False)
    play_theme = models.BooleanField("Play theme on door swipe", default=False)

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


class MemberbucksDevice(AccessControlledDevice):
    all_members = False

    def lock(self):
        return False

    def unlock(self):
        return False

    def reboot(self):
        import requests
        r = requests.get("http://{}/reboot".format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " rebooted from admin interface.", "memberbucks", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " rebooted from admin interface failed.", "memberbucks", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False


class Doors(AccessControlledDevice):
    def bump(self):
        import requests
        r = requests.get("http://{}/bump".format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " bumped from admin interface.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " bumped from admin interface failed.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

    def reboot(self):
        import requests
        r = requests.get("http://{}/reboot".format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " rebooted from admin interface.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " rebooted from admin interface failed.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

    def log_access(self, member_id):
        return DoorLog.objects.create(user=User.objects.get(pk=member_id), door=self)


class Interlock(AccessControlledDevice):
    def lock(self):
        import requests
        r = requests.get("http://{}/end".format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " locked from admin interface.", "interlock", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " lock request from admin interface failed.", "interlock", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

    def create_session(self, user):
        session = InterlockLog.objects.create(id=uuid.uuid4(), user=user, interlock=self, first_heartbeat=timezone.now(), last_heartbeat=timezone.now())

        if session:
            return session

        return False

    def get_last_active(self):
        interlocklog = InterlockLog.objects.filter(interlock=self).latest("last_heartbeat")
        return interlocklog.last_heartbeat

    def reboot(self):
        import requests
        r = requests.get("http://{}/reboot".format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " rebooted from admin interface.", "interlock", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " rebooted from admin interface failed.", "interlock", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

class DoorLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class InterlockLog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_off = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="user_off")
    interlock = models.ForeignKey(Interlock, on_delete=models.CASCADE)
    first_heartbeat = models.DateTimeField(default=timezone.now)
    last_heartbeat = models.DateTimeField(default=timezone.now)
    session_complete = models.BooleanField(default=False)

    def heartbeat(self):
        self.last_heartbeat = timezone.now()
        self.interlock.checkin()
        self.save()
