from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from memberportal.helpers import log_event
import pytz
utc = pytz.UTC


class Doors(models.Model):
    name = models.CharField("Door Name", max_length=20, unique=True)
    description = models.CharField("Door Description/Location", max_length=100)
    ip_address = models.GenericIPAddressField(
        "IP Address of Door", unique=True, null=True, blank=True)
    last_seen = models.DateTimeField(null=True)
    all_members = models.BooleanField(
        "Members have access by default", default=False)

    def checkin(self):
        log_event(self.name + " checked in with server.", "door")
        self.last_seen = datetime.now()
        self.save()

    def get_unavailable(self):
        if self.last_seen:
            if utc.localize(datetime.now()) - timedelta(minutes=5) > self.last_seen:
                return True

        return False

    def unlock(self):
        import requests
        r = requests.get('http://{}/open?key=key'.format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " unlocked from admin interface.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " unlock from admin interface failed.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

    def log_access(self, member_id):
        DoorLog(user=User.objects.get(pk=member_id), door=self).save()

    def __str__(self):
        return self.name


class DoorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
