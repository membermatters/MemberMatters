from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.utils import timezone

class UserResource(resources.ModelResource):
    first_name = fields.Field(
        column_name="first_name", attribute="first_name", widget=ForeignKeyWidget(Profile, "first_name")
    )
    last_name = fields.Field(
        column_name="last_name", attribute="last_name", widget=ForeignKeyWidget(Profile, "last_name")
    )
    screen_name = fields.Field(
        column_name="screen_name", attribute="screen_name", widget=ForeignKeyWidget(Profile, "screen_name")
    )
    rfid = fields.Field(
        column_name="rfid", attribute="rfid", widget=ForeignKeyWidget(Profile, "rfid")
    )
    state = fields.Field(
        column_name="state", attribute="state", widget=ForeignKeyWidget(Profile, "state")
    )

    def dehydrate_first_name(self, user):
        try:
            return user.profile.first_name
        except Exception:
            return ""
    def dehydrate_last_name(self, user):
        try:
            return user.profile.last_name
        except Exception:
            return ""
    def dehydrate_screen_name_name(self, user):
        try:
            return user.profile.screen_name
        except Exception:
            return ""
    def dehydrate_rfid(self, user):
        try:
            return user.profile.rfid
        except Exception:
            return None
    def dehydrate_state(self, user):
        try:
            return user.profile.state
        except Exception:
            return "noob"

    def before_import_row(self, row, **kwargs):
        user, created = User.objects.get_or_create(
            email=row["email"],
            defaults={
                "email": row["email"],
                "email_verified": True,
                "admin": row["admin"],
                "staff": row["staff"],
            }
        )

        # new User needs a Profile
        if created:
            # mandatory fields with profile
            Profile.objects.create(
                user=user,
                first_name=row["first_name"],
                last_name=row["last_name"],
                screen_name=row["screen_name"],
                rfid=row["rfid"] or None,
            )

    def skip_row(self, instance, original, row, import_validation_errors):
        return (row["email"] == "default@example.com")

    class Meta:
        model = User
        import_id_fields = ["email"]
        fields = ('email', 'staff', 'admin', 'first_name', 'last_name', 'screen_name', 'rfid')

class ProfileResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row["user"] = (User.objects.get_or_create(
            email=email,
            defaults={
                "email": email,
                "email_verified": email_verified,
                "staff": staff,
                "admin": admin,
            }
            ))[0]
        print("Got user {}".format(row["user"]))
        if row["user"].profile is None:
            print("Creating a profile for user {} result: {}".format(row["user"].email, Profile.objects.create(
                user=row["user"]
            )))

    class Meta:
        model = Profile
        import_id_fields = ["user__email"]
        fields = ('user__email', 'user__staff', 'user__admin', 'screen_name', 'first_name', 'last_name', 'rfid')


@admin.register(User)
class AdminLogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserResource
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "subscription_first_created")
    pass


@admin.register(UserEventLog)
class UserEventLogAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)
