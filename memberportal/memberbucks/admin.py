from django.contrib import admin
from .models import MemberBucks, MemberbucksProduct, MemberbucksProductPurchaseLog


@admin.register(MemberBucks)
class MemberBucksAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberbucksProduct)
class MemberbucksProductAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberbucksProductPurchaseLog)
class MemberbucksProductPurchaseLogAdmin(admin.ModelAdmin):
    pass
