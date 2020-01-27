from django.contrib import admin
from .models import MemberBucks


@admin.register(MemberBucks)
class MemberBucksAdmin(admin.ModelAdmin):
    pass
