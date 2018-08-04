from django.db import models
from datetime import timedelta
from django.utils import timezone
from memberportal.helpers import log_event
from django.contrib.auth import get_user_model
import pytz
from django.conf import settings
from django.contrib import auth
import uuid
User = auth.get_user_model()
utc = pytz.UTC


class AccessControlledDevice(models.Model):
    name = models.CharField("Name", max_length=20, unique=True)
    description = models.CharField("Description/Location", max_length=100)
    ip_address = models.GenericIPAddressField("IP Address of device", unique=True, null=True, blank=True)
    last_seen = models.DateTimeField(null=True)
    all_members = models.BooleanField("Members have access by default", default=False)

    def checkin(self):
        log_event(self.name + " checked in with server.", "door")
        self.last_seen = timezone.now()
        self.save()

    def get_unavailable(self):
        if self.last_seen:
            if timezone.now() - timedelta(minutes=5) > self.last_seen:
                return True

        return False

    def unlock(self):
        import requests
        r = requests.get('http://{}/unlock?key=key'.format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " unlocked from admin interface.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " unlock from admin interface failed.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

    def lock(self):
        import requests
        r = requests.get('http://{}/lock?key=key'.format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " unlocked from admin interface.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " unlock from admin interface failed.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

    def __str__(self):
        return self.name


class Doors(AccessControlledDevice):
    def log_access(self, member_id):
        return DoorLog.objects.create(user=User.objects.get(pk=member_id), door=self)


class Interlock(AccessControlledDevice):
    def create_session(self, user):
        session = InterlockLog.objects.create(id=uuid.uuid4(), user=user, interlock=self, first_heartbeat=timezone.now(), last_heartbeat=timezone.now())

        if session:
            return session

        return False

    def get_last_active(self):
        interlocklog = InterlockLog.objects.filter(interlock=self).latest('last_heartbeat')
        return interlocklog.last_heartbeat


class DoorLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class InterlockLog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interlock = models.ForeignKey(Interlock, on_delete=models.CASCADE)
    first_heartbeat = models.DateTimeField(default=timezone.now)
    last_heartbeat = models.DateTimeField(default=timezone.now)
    session_complete = models.BooleanField(default=False)

    def heartbeat(self):
        self.last_heartbeat = timezone.now()
        self.interlock.checkin()
        self.save()
