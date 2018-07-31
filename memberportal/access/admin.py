from django.contrib import admin
from .models import *


@admin.register(Doors)
class DoorsAdmin(admin.ModelAdmin):
    pass


@admin.register(DoorLog)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Interlock)
class DoorsAdmin(admin.ModelAdmin):
    pass


@admin.register(InterlockLog)
class ProfileAdmin(admin.ModelAdmin):
    pass