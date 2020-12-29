from django.db import models
from django.conf import settings
from group.models import Group


class Meeting(models.Model):
    """
    Model to store meeting objects.
    """

    MEETING_TYPES = (
        ("general", "General"),
        ("agm", "Annual General"),
        ("group", "Group"),
        ("other", "Other"),
    )

    date = models.DateTimeField("Date and time of meeting")
    type = models.CharField("Meeting Type", max_length=10, choices=MEETING_TYPES)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    chair = models.CharField(max_length=20, null=True, blank=True)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def get_type(self):
        return self.group.name if self.type == "group" else self.get_type_display()

    def __str__(self):
        return f"{self.date} - {self.group if self.group else ''} {self.type} meeting"


class ProxyVote(models.Model):
    """
    Model to store proxy votes that may be attached to a Meeting object.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_city = models.CharField(max_length=30, null=True, blank=True)
    proxy_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="held_proxies"
    )
    proxy_city = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField("Date proxy was created", auto_now_add=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
