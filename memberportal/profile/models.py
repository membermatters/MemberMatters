from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
import os
import sendgrid
from sendgrid.helpers.mail import *
from django.utils.timezone import make_aware
import uuid
from django.template.loader import render_to_string
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.conf import settings
from profile.xerohelpers import get_xero_contact, create_membership_invoice
from profile.xerohelpers import add_to_xero
from constance import config
from api_general.models import SiteSession
from api_admin_tools.models import MemberTier, PaymentPlan
import json
import uuid

utc = pytz.UTC

LOG_TYPES = (
    ("generic", "Generic log entry"),
    ("usage", "Generic usage access"),
    ("stripe", "Stripe related event"),
    ("memberbucks", "Memberbucks related event"),
    ("spacebucks", "Spacebucks related event"),
    ("profile", "Member profile edited"),
    ("interlock", "Interlock related event"),
    ("door", "Door related event"),
    ("email", "Email send event"),
    ("admin", "Generic admin event"),
    ("error", "Some event that causes an error"),
    ("xero", "Generic xero log entry"),
)


class Log(models.Model):
    logtype = models.CharField("Type of action/event", choices=LOG_TYPES, max_length=30)
    description = models.CharField("Description of action/event", max_length=500)
    data = models.TextField("Extra data for debugging action/event")
    date = models.DateTimeField(auto_now_add=True)


class UserEventLog(Log):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class EventLog(Log):
    pass


# this needs to be here because it relies on the models defined above
from membermatters.helpers import log_user_event


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

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def __send_email(self, subject, body):
        sg = sendgrid.SendGridAPIClient(config.SENDGRID_API_KEY)
        from_email = From(config.EMAIL_DEFAULT_FROM)
        to_email = To(self.email)
        subject = subject
        content = Content("text/html", body)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.send(mail)

        if response.status_code == 202:
            log_user_event(
                self,
                "Sent email with subject: " + subject,
                "email",
                "Email content: " + body,
            )
            return True

    def email_notification(self, subject, title, preheader, message):
        email_vars = {"preheader": preheader, "title": title, "message": message}
        email_string = render_to_string(
            "email_without_button.html", {"email": email_vars, "config": config}
        )

        if self.__send_email(subject, email_string):
            return True

    def email_password_reset(self, link):
        email_vars = {"link": link}
        email_string = render_to_string(
            "email_password_reset.html", {"email": email_vars, "config": config}
        )

        if self.__send_email(f"Reset your {config.SITE_OWNER} password", email_string):
            return True

    def email_link(self, subject, title, preheader, message, link, btn_text):
        email_vars = {
            "preheader": preheader,
            "title": title,
            "message": message,
            "link": link,
            "btn_text": btn_text,
        }
        email_string = render_to_string(
            "email_with_button.html",
            {"email": email_vars, "config": config, "config": config},
        )

        if self.__send_email(subject, email_string):
            return True

        return False

    def email_invoice(self, name, amount, number, due_date, reference, url):
        invoice = {
            "name": name,
            "amount": amount,
            "number": number,
            "due_date": due_date,
            "reference": reference,
            "url": url,
        }
        email_string = render_to_string(
            "email_invoice.html", {"invoice": invoice, "config": config}
        )

        if self.__send_email(
            f"You have a new invoice from {config.SITE_OWNER} ({number})", email_string
        ):
            return True

        return False

    def email_welcome(self):
        cards = (
            config.WELCOME_EMAIL_CARDS
            if config.WELCOME_EMAIL_CARDS
            else config.HOME_PAGE_CARDS
        )
        cards = json.loads(cards)

        email_string = render_to_string(
            "email_welcome.html", {"config": config, "cards": cards}
        )

        if self.__send_email(f"Welcome to {config.SITE_OWNER}", email_string):
            return "Successfully sent welcome email to user. ✉"

        return False

    def email_disable_member(self):
        if self.email_notification(
            f"{self.profile.first_name}, your {config.SITE_OWNER} site access has been disabled.",
            "Your access has been disabled.",
            f"Your {config.SITE_OWNER} site access has been disabled.",
            f"Your access to {config.SITE_OWNER} has been disabled. This could be due to overdue membership fees, a"
            " ban being issued or your membership ending. If this is because of a ban, you are not allowed back on "
            "site until your ban has ended and your membership has been reactivated.",
        ):
            return True

        return False

    def email_enable_member(self):
        if self.email_notification(
            f"{self.profile.first_name}, your {config.SITE_OWNER} site access has been enabled.",
            "Your access has been enabled.",
            f"Your {config.SITE_OWNER} site access has been enabled.",
            f"Great news! Your access to {config.SITE_OWNER} has been enabled.",
        ):
            return True

        return False

    def reset_password(self):
        log_user_event(self, "Password reset requested", "profile")
        self.password_reset_key = uuid.uuid4()
        self.password_reset_expire = timezone.now() + timedelta(hours=24)
        self.save()
        self.email_password_reset(
            f"{config.SITE_URL}/profile/password/reset/{self.password_reset_key}"
        )

        return True


class MemberTypes(models.Model):
    # TODO: remove this when the stripe billing is fully implemented
    name = models.CharField("Member Type Name", max_length=20)
    conditions = models.CharField("Membership Conditions", max_length=100)
    cost = models.IntegerField("Monthly Cost (cents)")

    def get_object(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "conditions": self.conditions,
            "cost": self.cost,
        }

    def __str__(self):
        return self.name + " - ${} per mth. {}".format(self.cost, self.conditions)


from access.models import Doors, Interlock


class Profile(models.Model):
    def path_and_rename(self, filename):
        ext = filename.split(".")[-1]
        # set filename as random string
        filename = f"profile_pics/{str(uuid.uuid4())}.{ext}"
        # return the new path to the file
        return os.path.join(filename)

    STATES = (
        ("noob", "New"),
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    class Meta:
        permissions = [
            ("change_staff", "Can change if the user is a staff member or not"),
            ("manage_access", "Can manage a user's access permissions"),
            ("deactivate_member", "Can deactivate or activate a member"),
            ("see_personal_details", "Can see and update a member's personal details"),
            ("manage_memberbucks_balance", "Can see and modify memberbucks balance"),
            ("member_logs", "Can see a members log"),
            ("generate_invoice", "Can generate a member invoice"),
        ]

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
    state = models.CharField(max_length=8, default="noob", choices=STATES)

    picture = models.ImageField(upload_to=path_and_rename, null=True, blank=True)

    member_type = models.ForeignKey(
        MemberTypes, on_delete=models.PROTECT, related_name="member_type"
    )
    groups = models.ManyToManyField("group.Group")
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
    xero_account_id = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )
    xero_account_number = models.CharField(
        max_length=6, blank=True, null=True, default=""
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

    def deactivate(self, request):
        log_user_event(
            self.user,
            request.user.profile.get_full_name() + " deactivated member",
            "profile",
        )
        self.user.email_disable_member()
        self.state = "inactive"
        self.save()
        return True

    def activate(self, request):
        log_user_event(
            self.user,
            request.user.profile.get_full_name() + " activated member",
            "profile",
        )
        if self.state != "noob":
            self.user.email_enable_member()

        self.state = "active"
        self.save()
        return True

    def email_profile_to(self, to_email):
        groups = self.groups.all()
        groups_string = "none :("

        if groups.count() == 3:
            groups_string = "{}, {} and {}".format(groups[0], groups[1], groups[2])
        elif groups.count() == 2:
            groups_string = "{} and {}".format(groups[0], groups[1])
        elif groups.count() == 1:
            groups_string = groups[0]

        message = (
            f"{self.get_full_name()} has just signed up. Their membership level is {self.member_type} and their selected {config.GROUP_NAME} are {groups_string}. "
            f"Their email is {self.user.email}."
        )
        email_vars = {"preheader": "", "title": "New member signup", "message": message}
        email_string = render_to_string(
            "email_without_button.html", {"email": email_vars, "config": config}
        )
        subject = "A new member signed up! ({})".format(self.get_full_name())

        sg = sendgrid.SendGridAPIClient(config.SENDGRID_API_KEY)

        from_email = From(config.EMAIL_DEFAULT_FROM)
        to_email = To(to_email)
        content = Content("text/html", email_string)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.send(mail)

        if response.status_code == 202:
            log_user_event(
                self.user,
                "Sent email with subject: " + subject,
                "email",
                "Email content: " + email_string,
            )
            return True

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
        self.last_seen = timezone.now()
        return self.save()

    def get_xero_contact(self):
        return get_xero_contact(self)

    def add_to_xero(self):
        return add_to_xero(self)

    def create_membership_invoice(self, email_invoice=True):
        return create_membership_invoice(self.user, email_invoice)

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
            # "picture": picture,
            "memberType": {
                "name": self.member_type.name,
                "id": self.member_type_id,
            },
            "groups": self.groups.all().values(),
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
            "xero": {
                "accountId": self.xero_account_id,
                "accountNumber": self.xero_account_number,
            },
        }

    def get_access_permissions(self):
        """
        returns a dictionary of the user's access permissions
        :return:
        """
        doors = []
        interlocks = []

        user_active = not (self.state == "inactive" or self.state == "noob")

        # if the method got doors, use them, otherwise query them
        for door in Doors.objects.all():
            if door in self.doors.all() and user_active:
                doors.append({"name": door.name, "access": True, "id": door.id})

            else:
                doors.append({"name": door.name, "access": False, "id": door.id})

        # if the method got interlocks, use them, otherwise query them
        for interlock in Interlock.objects.all():
            if interlock in self.interlocks.all() and user_active:
                interlocks.append(
                    {"name": interlock.name, "access": True, "id": interlock.id}
                )

            else:
                interlocks.append(
                    {"name": interlock.name, "access": False, "id": interlock.id}
                )

        return {"doors": doors, "interlocks": interlocks}

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Profile, self).save(*args, **kwargs)
