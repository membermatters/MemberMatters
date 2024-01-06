from django.contrib import admin
from .models import *


@admin.register(User)
class AdminLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "subscription_first_created")
    pass


@admin.register(UserEventLog)
class UserEventLogAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)
