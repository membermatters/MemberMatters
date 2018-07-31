from django.db import models


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
