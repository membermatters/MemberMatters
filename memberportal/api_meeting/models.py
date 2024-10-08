from django.db import models
from django.conf import settings
from django_prometheus.models import ExportModelOperationsMixin


class Meeting(ExportModelOperationsMixin("meeting"), models.Model):
    """
    Model to store meeting objects.
    """

    MEETING_TYPES = (
        ("general", "General"),
        ("agm", "Annual General"),
        ("other", "Other"),
    )

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField("Date and time of meeting")
    type = models.CharField("Meeting Type", max_length=10, choices=MEETING_TYPES)
    chair = models.CharField(max_length=20, null=True, blank=True)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def get_type(self):
        return self.get_type_display()

    def __str__(self):
        return f"{self.date} - {self.type} meeting"


class ProxyVote(ExportModelOperationsMixin("proxy-vote"), models.Model):
    """
    Model to store proxy votes that may be attached to a Meeting object.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_city = models.CharField(max_length=30, null=True, blank=True)
    proxy_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="held_proxies"
    )
    proxy_city = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField("Date proxy was created", auto_now_add=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
