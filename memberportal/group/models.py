from django.db import models
from constance import config
import math

def divround_down(value, step):
    return value//step*step

class Group(models.Model):
    name = models.CharField(f"{config.GROUP_NAME} Name", max_length=20, unique=True)
    description = models.CharField(f"{config.GROUP_NAME} Description", max_length=100)
    leaders = models.ManyToManyField("profile.User")
    item_code = models.CharField("Xero Item Code", max_length=50)
    account_code = models.IntegerField("Xero Account Code")
    hidden = models.BooleanField(default=False)

    def get_active_count(self):
        return str(self.profile_set.filter(state="active").count())

    def get_quorum(self):
        quorum = int(divround_down(self.profile_set.filter(state="active").count(),5)/5)
        if quorum < 5:
            quorum = 5
        return str(quorum)

    def get_active_set(self):
        return self.profile_set.filter(state="active")

    def __str__(self):
        return self.name




class CauseFund(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    name = models.CharField("Fund Name", max_length=20, unique=True)
    description = models.CharField(
        "Description of Fund", max_length=100)
    balance = models.FloatField("Amount", default=0)
