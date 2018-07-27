from django.contrib import admin
from .models import Causes


@admin.register(Causes)
class CausesAdmin(admin.ModelAdmin):
    pass
