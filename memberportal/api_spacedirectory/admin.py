from django.contrib import admin
from .models import SpaceAPI, SpaceAPISensor, SpaceAPISensorProperties


@admin.register(SpaceAPI)
class SpaceAPIAdmin(admin.ModelAdmin):
    pass


@admin.register(SpaceAPISensor)
class SpaceAPISensorAdmin(admin.ModelAdmin):
    pass


@admin.register(SpaceAPISensorProperties)
class SpaceAPISensorPropertiesAdmin(admin.ModelAdmin):
    pass
