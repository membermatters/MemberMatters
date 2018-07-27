from django.contrib import admin
from .models import SpaceBucks


@admin.register(SpaceBucks)
class SpaceBucksAdmin(admin.ModelAdmin):
    pass
