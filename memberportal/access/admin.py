from django.contrib import admin
from .models import Doors, DoorLog


@admin.register(Doors)
class DoorsAdmin(admin.ModelAdmin):
    pass


@admin.register(DoorLog)
class ProfileAdmin(admin.ModelAdmin):
    pass
