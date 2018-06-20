from django.db import models
from django.contrib.auth.models import User


class MemberState(models.Model):
    name = models.CharField("Member State", max_length=20)

    def __str__(self):
        return self.name


class MemberTypes(models.Model):
    name = models.CharField("Member Type Name", max_length=20)
    conditions = models.CharField("Membership Conditions", max_length=100)
    cost = models.IntegerField("Monthly Cost")

    def __str__(self):
        if self.name == "Woofing Hacker":
            return self.name + " - email exec to apply".format(self.cost)
        return self.name + " - ${} per mth".format(self.cost)


class Causes(models.Model):
    name = models.CharField("Cause Name", max_length=20, unique=True)
    description = models.CharField("Cause Description", max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    state = models.ForeignKey(MemberState, on_delete=models.CASCADE, related_name='state')
    member_type = models.ForeignKey(MemberTypes, on_delete=models.CASCADE, related_name='member_type')
    cause1 = models.ForeignKey(Causes, on_delete=models.CASCADE, verbose_name="Cause 1", related_name='Cause1')
    cause2 = models.ForeignKey(Causes, on_delete=models.CASCADE, verbose_name="Cause 2", related_name='Cause2')
    cause3 = models.ForeignKey(Causes, on_delete=models.CASCADE, verbose_name="Cause 3", related_name='Cause3')

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
