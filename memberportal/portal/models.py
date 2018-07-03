from django.db import models
from django.contrib.auth.models import User


class MemberState(models.Model):
    name = models.CharField("Member State", max_length=20)

    def __str__(self):
        return self.name


class AdminLog(models.Model):
    log_user = models.ForeignKey(User, "Name of admin", related_name="log_user")
    action = models.CharField("Action taken", max_length=50)
    log_member = models.ForeignKey(User, "Name of member", related_name="log_member")
    description = models.CharField("Description of why", max_length=500)
    date = models.DateTimeField(auto_now_add=True)


class MemberTypes(models.Model):
    name = models.CharField("Member Type Name", max_length=20)
    conditions = models.CharField("Membership Conditions", max_length=100)
    cost = models.IntegerField("Monthly Cost")

    def __str__(self):
        return self.name + " - ${} per mth. {}".format(self.cost, self.conditions)


class Causes(models.Model):
    name = models.CharField("Cause Name", max_length=20, unique=True)
    description = models.CharField("Cause Description", max_length=100)

    def __str__(self):
        return self.name


class Doors(models.Model):
    name = models.CharField("Door Name", max_length=20, unique=True)
    description = models.CharField("Door Description/Location", max_length=100)
    ip_address = models.CharField("IP Address of Door", max_length=16, unique=True)

    def __str__(self):
        return self.name


class DoorPermissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

    class Meta:
        unique_together = ('user', 'door')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    state = models.ForeignKey(MemberState, on_delete=models.PROTECT, related_name='state', default="1")
    member_type = models.ForeignKey(MemberTypes, on_delete=models.PROTECT, related_name='member_type')
    cause1 = models.ForeignKey(Causes, on_delete=models.SET_NULL, verbose_name="Cause 1", related_name='Cause1', null=True)
    cause2 = models.ForeignKey(Causes, on_delete=models.SET_NULL, verbose_name="Cause 2", related_name='Cause2', null=True)
    cause3 = models.ForeignKey(Causes, on_delete=models.SET_NULL, verbose_name="Cause 3", related_name='Cause3', null=True)
    rfid = models.CharField("RFID Tag", max_length=20, unique=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_state(self):
        if self.state == "noob":
            return "New Member"
        if self.state == "active":
            return "Active Member"
        if self.state == "inactive":
            return "Inactive Member"
        return self.state
