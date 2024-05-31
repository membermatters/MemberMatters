from django.contrib import admin
from api_metrics.models import *


@admin.register(Metric)
class Metric(admin.ModelAdmin):
    pass
