from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
import os
from django.utils.timezone import make_aware
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.conf import settings
from constance import config
from api_general.models import SiteSession
from api_admin_tools.models import PaymentPlan
import json
import uuid
import logging
from services.emails import send_single_email, send_email_to_admin
from services import sms

logger = logging.getLogger("app")

utc = pytz.UTC

LOG_TYPES = (
    ("generic", "Generic log entry"),
    ("usage", "Generic usage access"),
    ("stripe", "Stripe related event"),
    ("memberbucks", "Memberbucks related event"),
    ("spacebucks", "Spacebucks related event"),
    ("profile", "Member profile was edited or updated"),
    ("interlock", "Interlock device related event"),
    ("door", "Door device related event"),
    ("memberbucksdevice", "Memberbucks device related event"),
    ("email", "An email was sent or attempted to be sent"),
    ("admin", "An admin performed an action"),
    ("error", "An event or action caused an error"),
    ("xero", "Generic xero log entry"),
)


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    logtype = models.CharField(
        "Type of action/event", choices=LOG_TYPES, max_length=30, default="generic"
    )
    description = models.CharField("Description of action/event", max_length=500)
    data = models.TextField("Extra data for debugging action/event")
    date = models.DateTimeField(auto_now_add=True)
    door = models.ForeignKey(
        "access.Doors",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True,
    )
    interlock = models.ForeignKey(
        "access.Interlock",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True,
    )
    memberbucks_device = models.ForeignKey(
        "access.MemberbucksDevice",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True,
    )


class UserEventLog(Log):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class EventLog(Log):
    pass


def log_event(
    description,
    event_type="generic",
    data="",
    door=None,
    interlock=None,
    memberbucks_device=None,
):
    EventLog(
        description=description,
        logtype=event_type,
        data=data,
        door=door,
        interlock=interlock,
        memberbucks_device=memberbucks_device,
    ).save()


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD + "__iexact": username})

    def create_user(self, email, password=None, is_superuser=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_superuser=True,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    id = models.AutoField(primary_key=True)
    email_verified = models.BooleanField(default=True)
    password_reset_key = models.UUIDField(default=None, blank=True, null=True)
    password_reset_expire = models.DateTimeField(default=None, blank=True, null=True)
    staff = models.BooleanField(default=False)  # an admin user for the portal
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.profile.get_short_name()

    def get_full_name(self):
        return self.profile.get_full_name()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def log_event(self, description, event_type, data=""):
        UserEventLog(
            description=description, logtype=event_type, user=self, data=data
        ).save()

    def __send_email(self, subject, template_vars, template_name=None):
        return send_single_email(
            to_email=self.email,
            subject=subject,
            template_vars=template_vars,
            user=self,
            template_name=template_name,
        )

    def email_link(self, subject, title, message, link, btn_text):
        template_vars = {
            "title": title,
            "message": message,
            "link": link,
            "btn_text": btn_text,
        }

        return self.__send_email(
            subject=subject,
            template_vars=template_vars,
            template_name="email_with_button.html",
        )

    def email_notification(self, subject, message):
        template_vars = {"title": subject, "message": message}
        return self.__send_email(subject, template_vars=template_vars)

    def email_password_reset(self, link):
        template_vars = {"link": link}

        return self.__send_email(
            f"Reset your {config.SITE_OWNER} password",
            template_vars,
            template_name="email_password_reset.html",
        )

    def email_membership_application(self):
        subject = "Your membership application has been submitted"
        message = "Thanks for submitting your membership application! Your membership application has been submitted and you are now a 'member applicant'. Your membership will be officially accepted shortly, but we have granted site access immediately. You will receive an email confirming that your access card has been enabled. If for some reason your membership is rejected within this period, you will receive an email with further information."

        self.email_notification(subject, message)

        subject = f"A new person just became a member applicant: {self.profile.get_full_name()}"
        message = f"{self.profile.get_full_name()} just completed all steps required to sign up and is now a member applicant. Their site access has been enabled and membership will automatically be accepted within 7 days without objection."
        template_vars = {"message": message}

        return send_email_to_admin(
            subject, template_vars=template_vars, reply_to=self.email, user=self
        )

    def email_welcome(self):
        cards = (
            config.WELCOME_EMAIL_CARDS
            if config.WELCOME_EMAIL_CARDS
            else config.HOME_PAGE_CARDS
        )
        cards = json.loads(cards)

        subject = f"Welcome to {config.SITE_OWNER}"
        template_vars = {"title": subject, "cards": cards}

        if self.__send_email(
            subject=subject,
            template_vars=template_vars,
            template_name="email_welcome.html",
        ):
            return "Successfully sent welcome email to user. ✉"

        return False

    def email_disable_member(self):
        return self.email_notification(
            f"Your {config.SITE_OWNER} site access has been disabled.",
            f"Your access to {config.SITE_OWNER} has been disabled. This could be due to many reasons, but is "
            f"usually due to a failed membership payment. If this is unexpected, please let us know.",
        )

    def email_enable_member(self):
        message = f"Great news {self.profile.first_name}, your {config.SITE_OWNER} site access has been enabled."
        subject = f"Your {config.SITE_OWNER} site access has been enabled."

        return self.email_notification(subject, message)

    def reset_password(self):
        self.log_event("Password reset requested", "profile")
        self.password_reset_key = uuid.uuid4()
        self.password_reset_expire = timezone.now() + timedelta(hours=24)
        self.save()
        self.email_password_reset(
            f"{config.SITE_URL}/profile/password/reset/{self.password_reset_key}"
        )

        return True


class Profile(models.Model):
    def path_and_rename(self, filename):
        ext = filename.split(".")[-1]
        # set filename as random string
        filename = f"profile_pics/{str(uuid.uuid4())}.{ext}"
        # return the new path to the file
        return os.path.join(filename)

    STATES = (
        ("noob", "Needs Induction"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("accountonly", "Account only"),
    )

    SUBSCRIPTION_STATES = (
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("cancelling", "Cancelling"),
    )

    class Meta:
        permissions = [
            ("change_staff", "Can change if the user is a staff member or not"),
            ("manage_access", "Can manage a user's access permissions"),
            ("deactivate_member", "Can deactivate or activate a member"),
            ("see_personal_details", "Can see and update a member's personal details"),
            ("manage_memberbucks_balance", "Can see and modify memberbucks balance"),
            ("member_logs", "Can see a members log"),
        ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    digital_id_token = models.UUIDField(
        "Digital ID Token", default=uuid.uuid4, null=True, blank=True
    )
    digital_id_token_expire = models.DateTimeField(
        editable=False, default=datetime.now, null=True, blank=True
    )
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    screen_name = models.CharField("Screen Name", max_length=30)
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '0417123456'."
        "Up to 12 characters allowed.",
    )
    phone = models.CharField(validators=[phone_regex], max_length=12, blank=True)
    state = models.CharField(max_length=11, default="noob", choices=STATES)
    vehicle_registration_plate = models.CharField(max_length=30, blank=True, null=True)

    membership_plan = models.ForeignKey(
        PaymentPlan,
        on_delete=models.PROTECT,
        related_name="membership_plan",
        null=True,
        blank=True,
    )

    rfid = models.CharField(
        "RFID Tag", max_length=20, unique=True, null=True, blank=True
    )
    doors = models.ManyToManyField("access.Doors", blank=True)
    interlocks = models.ManyToManyField("access.Interlock", blank=True)
    memberbucks_balance = models.FloatField(default=0.0)
    last_memberbucks_purchase = models.DateTimeField(default=timezone.now)
    must_update_profile = models.BooleanField(default=False)
    exclude_from_email_export = models.BooleanField(default=False)

    last_seen = models.DateTimeField(default=None, blank=True, null=True)
    last_induction = models.DateTimeField(default=None, blank=True, null=True)

    stripe_customer_id = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )
    stripe_card_expiry = models.CharField(
        max_length=10, blank=True, null=True, default=""
    )
    stripe_card_last_digits = models.CharField(
        max_length=4, blank=True, null=True, default=""
    )
    stripe_payment_method_id = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )
    stripe_subscription_id = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )
    subscription_status = models.CharField(
        max_length=10, default="inactive", choices=SUBSCRIPTION_STATES
    )
    subscription_first_created = models.DateTimeField(
        default=None, blank=True, null=True, editable=False
    )

    def generate_digital_id_token(self):
        self.digital_id_token = uuid.uuid4()
        self.digital_id_token_expire = make_aware(
            datetime.now() + timedelta(minutes=10)
        )
        self.save()

        return self.digital_id_token

    def validate_digital_id_token(self, token):
        if make_aware(
            datetime.now()
        ) < self.digital_id_token_expire and self.digital_id_token == uuid.UUID(token):
            return True

        else:
            return False

    def sync_access(self):
        for door in self.doors.all():
            door.sync()

        for interlock in self.interlocks.all():
            interlock.sync()

    def deactivate(self, request=None):
        if request:
            request.user.log_event(
                f"{request.user.profile.get_full_name()} deactivated member ({self.get_full_name()}).",
                "admin",
            )
            self.user.log_event(
                f"{request.user.profile.get_full_name()} deactivated member.",
                "admin",
            )
        else:
            self.user.log_event(
                f"system deactivated member ({self.get_full_name()}).",
                "profile",
            )

        self.user.email_disable_member()
        sms_message = sms.SMS()
        sms_message.send_deactivated_access(self.phone)
        self.state = "inactive"
        self.save()
        self.sync_access()
        return True

    def activate(self, request=None):
        if request:
            request.user.log_event(
                f"{request.user.profile.get_full_name()} activated member ({self.get_full_name()}).",
                "admin",
            )
            self.user.log_event(
                f"{request.user.profile.get_full_name()} activated member.",
                "admin",
            )
        else:
            self.user.log_event(
                f"system activated member ({self.get_full_name()})",
                "profile",
            )

        if self.state != "noob":
            sms_message = sms.SMS()
            sms_message.send_activated_access(self.phone)
            self.user.email_enable_member()

        self.state = "active"
        self.save()
        self.sync_access()
        return True

    def set_account_only(self):
        self.state = "accountonly"
        self.save()

    def email_profile_to(self, to_email):
        message = (
            f"{self.get_full_name()} has just signed up on the portal."
            f"Their email is {self.user.email}."
        )
        template_vars = {"title": "New member signup", "message": message}
        subject = "A new member signed up! ({})".format(self.get_full_name())

        return send_single_email(
            to_email,
            subject,
            template_vars=template_vars,
            user=self.user,
            reply_to=self.user.email,
        )

    def get_logs(self):
        return UserEventLog.objects.filter(user=self.user)

    def __str__(self):
        return str(self.user)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def update_last_seen(self):
        self.last_seen = timezone.now()
        return self.save()

    def update_last_induction(self):
        self.last_induction = timezone.now()
        return self.save()

    def is_signed_into_site(self):
        sessions = SiteSession.objects.filter(user=self.user, signout_date=None)

        return True if len(sessions) else False

    def get_basic_profile(self):
        """
        Returns a user's profile with a basic amount of info.
        :return: {}
        """
        return {
            "id": self.user.id,
            "admin": self.user.is_staff,
            "superuser": self.user.is_admin,
            "email": self.user.email,
            "excludeFromEmailExport": self.exclude_from_email_export,
            "registrationDate": self.created.strftime("%m/%d/%Y, %H:%M:%S"),
            "lastUpdatedProfile": self.modified.strftime("%m/%d/%Y, %H:%M:%S"),
            "screenName": self.screen_name,
            "name": {
                "first": self.first_name,
                "last": self.last_name,
                "full": self.get_full_name(),
            },
            "phone": self.phone,
            "state": self.get_state_display(),
            "vehicleRegistrationPlate": self.vehicle_registration_plate,
            "rfid": self.rfid,
            "memberBucks": {
                "balance": self.memberbucks_balance,
                "lastPurchase": self.last_memberbucks_purchase.strftime(
                    "%m/%d/%Y, %H:%M:%S"
                )
                if self.last_memberbucks_purchase
                else None,
            },
            "updateProfileRequired": self.must_update_profile,
            "lastSeen": self.last_seen.strftime("%m/%d/%Y, %H:%M:%S")
            if self.last_seen
            else None,
            "lastInduction": self.last_induction.strftime("%m/%d/%Y, %H:%M:%S")
            if self.last_induction
            else None,
            "stripe": {
                "cardExpiry": self.stripe_card_expiry,
                "last4": self.stripe_card_last_digits,
            },
            "subscriptionStatus": self.subscription_status,
        }

    def get_access_permissions(self):
        """
        returns a dictionary of the user's access permissions
        :return:
        """
        doors = []
        interlocks = []

        user_active = self.state == "active"

        from access.models import Doors, Interlock

        for door in Doors.objects.all():
            if door.hidden:
                continue

            if door in self.doors.all() and user_active:
                doors.append({"name": door.name, "access": True, "id": door.id})

            else:
                doors.append({"name": door.name, "access": False, "id": door.id})

        for interlock in Interlock.objects.all():
            if interlock.hidden:
                continue

            if interlock in self.interlocks.all() and user_active:
                interlocks.append(
                    {"name": interlock.name, "access": True, "id": interlock.id}
                )

            else:
                interlocks.append(
                    {"name": interlock.name, "access": False, "id": interlock.id}
                )

        return {"doors": doors, "interlocks": interlocks}

    def can_signup(self):
        """Checks if a member can signup. Returns {"success": True/False, "reasons": [String<list of reasons>]}"""
        required_steps = []

        # check if they were inducted recently enough
        last_inducted = self.last_induction
        furthest_previous_date = timezone.now() - timedelta(
            days=config.MAX_INDUCTION_DAYS
        )

        if config.MAX_INDUCTION_DAYS > 0 and (
            last_inducted is None or last_inducted < furthest_previous_date
        ):
            if (
                config.CANVAS_INDUCTION_ENABLED is True
                or config.MOODLE_INDUCTION_ENABLED is True
            ):
                required_steps.append("induction")

        # check if they have an RFID card assigned
        if not self.rfid:
            required_steps.append("accessCard")

        if len(required_steps):
            return {"success": False, "requiredSteps": required_steps}

        else:
            return {"success": True, "requiredSteps": []}

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Profile, self).save(*args, **kwargs)
