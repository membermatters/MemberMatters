from django.db import models
from django.utils import timezone
import pytz
from django_prometheus.models import ExportModelOperationsMixin

utc = pytz.UTC


class Metric(ExportModelOperationsMixin("metric"), models.Model):
    """Stores a single instance of a metric value."""

    class MetricName(models.TextChoices):
        MEMBER_COUNT_TOTAL = "member_count_total", "Member Count Total"
        SUBSCRIPTION_COUNT_TOTAL = (
            "subscription_count_total",
            "Subscription Count Total",
        )

    id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(default=timezone.now)
    data = models.JSONField("Data")
    name = models.CharField(
        "Metric Name",
        max_length=250,
        choices=MetricName.choices,
        default=None,
    )

    def __str__(self):
        return f"{self.name} - {self.creation_date}"
