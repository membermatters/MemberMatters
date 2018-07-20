from django.contrib import admin
from .models import AdminLog, MemberTypes, Causes, Doors, Profile, SpaceBucks


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberTypes)
class MemberTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(Causes)
class CausesAdmin(admin.ModelAdmin):
    pass


@admin.register(Doors)
class DoorsAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(SpaceBucks)
class ProfileAdmin(admin.ModelAdmin):
    pass
