from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from .models import *


@admin.register(AccessControlledDeviceAPIKey)
class AccessControlledDeviceAPIKey(APIKeyModelAdmin):
    pass


@admin.register(ExternalAccessControlAPIKey)
class ExternalAccessControlAPIKey(APIKeyModelAdmin):
    pass


@admin.register(Doors)
class DoorsAdmin(admin.ModelAdmin):
    pass


@admin.register(DoorLog)
class DoorLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Interlock)
class InterlockAdmin(admin.ModelAdmin):
    pass


@admin.register(InterlockLog)
class InterlockLogAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberbucksDevice)
class MemberbucksDeviceAdmin(admin.ModelAdmin):
    pass


# TODO:
# @admin.register(MemberbucksDeviceLog)
# class MemberbucksDeviceLogAdmin(admin.ModelAdmin):
#     pass
