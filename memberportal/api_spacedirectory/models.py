from django.core.exceptions import ValidationError
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class SpaceAPI(ExportModelOperationsMixin("space-api"), models.Model):
    # The Hackspace is always closed by default to prevent people from showing up by accident.
    space_is_open = models.BooleanField(default=False)
    space_message = models.CharField(max_length=255, blank=True, null=True)
    status_last_change = models.DateTimeField(auto_now=True)

    def clean(self):
        if SpaceAPI.objects.exists() and not self.pk:
            raise ValidationError("You can only have one SpaceAPI Setting")

    def __str__(self):
        open_text = "CLOSED"
        if self.space_is_open is True:
            open_text = "OPEN"

        return f"Currently {open_text} - last updated: {self.status_last_change}"


# Because Sensors are tied to a space, and we only have one space in the system for now
# We have the luxury of not requiring foreign keys here!
class SpaceAPISensor(ExportModelOperationsMixin("space-api-sensor"), models.Model):
    SENSOR_TYPE_CHOICES = [
        ("temperature", "Temperature"),
        ("barometer", "Barometer"),
        ("radiation", "Radiation"),
        ("humidity", "Humidity"),
        ("beverage_supply", "Beverage Supply"),
        ("power_consumption", "Power Consumption"),
        ("wind", "Wind Data"),
        ("network_connections", "Network Connections"),
        ("account_balance", "Account Balance"),
        ("network_traffic", "Network Traffic"),
    ]
    sensor_type = models.CharField(max_length=100, choices=SENSOR_TYPE_CHOICES)
    name = models.CharField(
        max_length=255
    )  # The sensor name ("main door", "external", etc)
    value = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.location} ({self.sensor_type})"


# Some sensors have properties, let's track those in a separate model
class SpaceAPISensorProperties(
    ExportModelOperationsMixin("space-api-sensor-properties"), models.Model
):
    sensor_id = models.ForeignKey(
        SpaceAPISensor, related_name="properties", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sensor_id.name}/{self.name}"
