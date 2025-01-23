from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class MemberResource(resources.ModelResource):
    email = fields.Field(
        column_name="email", attribute="email", widget=ForeignKeyWidget(User, "email")
    )
    email_verified = fields.Field(
        column_name="email_verified",
        attribute="email_verified",
        widget=ForeignKeyWidget(User, "email_verified"),
    )
    staff = fields.Field(
        column_name="staff", attribute="staff", widget=ForeignKeyWidget(User, "staff")
    )
    admin = fields.Field(
        column_name="admin", attribute="admin", widget=ForeignKeyWidget(User, "admin")
    )
    user = fields.Field(attribute="id", widget=ForeignKeyWidget(User, "id"))

    def before_import_row(self, row, **kwargs):
        email = row["email"]
        email_verified = row["email_verified"]
        staff = row["staff"]
        admin = row["admin"]
        row["user"] = User.objects.get_or_create(
            email=email,
            defaults={
                "email": email,
                "email_verified": email_verified,
                "staff": staff,
                "admin": admin,
            },
        ).id

    def dehydrate_email(self, profile):
        try:
            return profile.user.email
        except Exception:
            return "NADA"

    def dehydrate_email_verified(self, profile):
        try:
            return profile.user.email_verified
        except Exception:
            return "False"

    def dehydrate_staff(self, profile):
        try:
            return profile.user.staff
        except Exception:
            return "False"

    def dehydrate_admin(self, profile):
        try:
            return profile.user.admin
        except Exception:
            return "False"

    class Meta:
        model = Profile
        import_id_fields = ("user",)
        fields = (
            "email",
            "email_verified",
            "staff",
            "admin",
            "digital_id_token",
            "digital_id_token_expire",
            "created",
            "modified",
            "screen_name",
            "first_name",
            "last_name",
            "phone_regex",
            "phone",
            "state",
            "vehicle_registration_plate",
            "membership_plan",
            "rfid",
            "doors",
            "interlocks",
            "memberbucks_balance",
            "last_memberbucks_purchase",
            "must_update_profile",
            "exclude_from_email_export",
            "last_seen",
            "last_induction",
            "stripe_customer_id",
            "stripe_card_expiry",
            "stripe_card_last_digits",
            "stripe_payment_method_id",
            "stripe_subscription_id",
            "subscription_status",
            "subscription_first_created",
        )


# class UserResource(resources.ModelResource):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'email_verified', 'staff', 'admin',)

# class ProfileResource(resources.ModelResource):
#     class Meta:
#         model = Profile
#         fields = ('id', 'user', 'digital_id_token', 'digital_id_token_expire', 'created', 'modified',
#         'screen_name', 'first_name', 'last_name', 'phone_regex', 'phone', 'state', 'vehicle_registration_plate',
#         'membership_plan', 'rfid', 'doors', 'interlocks', 'memberbucks_balance', 'last_memberbucks_purchase',
#         'must_update_profile', 'exclude_from_email_export', 'last_seen', 'last_induction', 'stripe_customer_id',
#         'stripe_card_expiry', 'stripe_card_last_digits', 'stripe_payment_method_id', 'stripe_subscription_id',
#         'subscription_status', 'subscription_first_created',)


@admin.register(User)
class AdminLogAdmin(admin.ModelAdmin):
    # resource_class = UserResource
    # resource_class = MemberResource
    # resource_classes = [UserResource, ProfileResource]
    pass


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # resource_class = ProfileResource
    resource_class = MemberResource
    readonly_fields = ("created", "subscription_first_created")
    pass


@admin.register(UserEventLog)
class UserEventLogAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)
