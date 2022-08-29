from django.contrib import admin
from .models import *


@admin.register(Event)
class AdminLogAdmin(admin.ModelAdmin):
    ordering = ("-start_time",)
