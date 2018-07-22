from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
import pytz


class AdminLog(models.Model):
    log_user = models.ForeignKey(
        User, "Name of admin", related_name="log_user")
    action = models.CharField("Action taken", max_length=50)
    log_member = models.ForeignKey(
        User, "Name of member", related_name="log_member")
    description = models.CharField("Description of why", max_length=500)
    date = models.DateTimeField(auto_now_add=True)


class MemberTypes(models.Model):
    name = models.CharField("Member Type Name", max_length=20)
    conditions = models.CharField("Membership Conditions", max_length=100)
    cost = models.IntegerField("Monthly Cost")

    def __str__(self):
        return self.name + " - ${} per mth. {}".format(
            self.cost, self.conditions)


class Causes(models.Model):
    name = models.CharField("Cause Name", max_length=20, unique=True)
    description = models.CharField("Cause Description", max_length=100)

    def get_active_count(self):
        return str(self.profile_set.filter(state="active").count())

    def get_quorum(self):
        quorum = self.profile_set.filter(state="active").count() * 0.4
        if quorum < 3:
            quorum = 3
        return str(quorum)

    def get_active_set(self):
        return self.profile_set.filter(state="active")

    def __str__(self):
        return self.name


class Doors(models.Model):
    name = models.CharField("Door Name", max_length=20, unique=True)
    description = models.CharField("Door Description/Location", max_length=100)
    ip_address = models.GenericIPAddressField(
        "IP Address of Door", unique=True, null=True, blank=True)
    last_seen = models.DateTimeField(default=datetime.now, blank=True)
    all_members = models.BooleanField(
        "Members have access by default", default=False)

    def checkin(self):
        self.last_seen = datetime.now()
        self.save()

    def get_unavailable(self):
        utc = pytz.UTC
        if utc.localize(
                datetime.now()) - timedelta(minutes=5) > self.last_seen:
            return True

        return False

    def unlock(self):
        import requests
        r = requests.get('http://{}/open?key=key'.format(self.ip_address))
        if r.status_code == 200:
            return True
        else:
            return False

    def __str__(self):
        return self.name


class DoorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)


class Profile(models.Model):
    STATES = (
        ('noob', 'New Member'),
        ('active', 'Active Member'),
        ('inactive', 'Inactive Member'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    state = models.CharField(max_length=8, default='noob', choices=STATES)
    member_type = models.ForeignKey(
        MemberTypes, on_delete=models.PROTECT, related_name='member_type')
    causes = models.ManyToManyField(Causes)
    rfid = models.CharField(
        "RFID Tag", max_length=20, unique=True, null=True, blank=True)
    doors = models.ManyToManyField(Doors, blank=True)
    spacebucks_balance = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.user)


class SpaceBucks(models.Model):
    TRANSACTION_TYPES = (
        ('stripe', 'Stripe Payment'),
        ('card', 'Membership Card')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField("Amount")
    transaction_type = models.CharField(
        "Transaction Type", max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(
        "Description of Transaction", max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        super(SpaceBucks, self).save(*args, **kwargs)
        self.user.spacebucks_balance = SpaceBucks.objects.filter(
            user=self.user).aggregate(Sum('amount'))['amount__sum']
        self.user.save()
