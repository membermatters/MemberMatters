from django.contrib import admin
from .models import *


@admin.register(User)
class AdminLogAdmin(admin.ModelAdmin):
    pass


@admin.register(UserEventLog)
class AdminLogAdmin(admin.ModelAdmin):
    pass


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberTypes)
class MemberTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
