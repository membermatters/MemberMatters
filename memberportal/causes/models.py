from django.db import models
import math


class Causes(models.Model):
    name = models.CharField("Cause Name", max_length=20, unique=True)
    description = models.CharField("Cause Description", max_length=100)
    leaders = models.ManyToManyField("profile.User")
    item_code = models.CharField("Item Code", max_length=50)
    account_code = models.IntegerField("Account Code")
    hidden = models.BooleanField(default=False)

    def get_active_count(self):
        return str(self.profile_set.filter(state="active").count())

    def get_quorum(self):
        quorum = math.ceil(self.profile_set.filter(state="active").count() * 0.4)
        if quorum < 3:
            quorum = 3
        if quorum > 10:
            quorum = 10

        return str(quorum)

    def get_active_set(self):
        return self.profile_set.filter(state="active")

    def __str__(self):
        return self.name


class CauseFund(models.Model):
    cause = models.ForeignKey('Causes', on_delete=models.CASCADE)
    name = models.CharField("Fund Name", max_length=20, unique=True)
    description = models.CharField(
        "Description of Fund", max_length=100)
    balance = models.FloatField("Amount", default=0)
