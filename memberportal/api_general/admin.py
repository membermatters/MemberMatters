from django.contrib import admin
from .models import *


@admin.register(Kiosk)
class AdminLogAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteSession)
class AdminLogAdmin(admin.ModelAdmin):
    pass
