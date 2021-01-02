from django.contrib import admin
from .models import *


@admin.register(MemberTier)
class AdminLogAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentPlan)
class AdminLogAdmin(admin.ModelAdmin):
    pass
