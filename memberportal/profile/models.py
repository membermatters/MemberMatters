from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import pytz
import os
import sendgrid
from sendgrid.helpers.mail import *
import uuid
from django.template.loader import render_to_string
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.validators import RegexValidator
from django.conf import settings
from profile.xerohelpers import get_xero_contact, create_membership_invoice
from profile.xerohelpers import add_to_xero

utc = pytz.UTC

LOG_TYPES = (
    ('generic', 'Generic log entry'),
    ('usage', 'Generic usage access'),
    ('stripe', 'Stripe related event'),
    ('spacebucks', 'Spacebucks related event'),
    ('profile', 'Member profile edited'),
    ('interlock', 'Interlock related event'),
    ('door', 'Door related event'),
    ('email', 'Email send event'),
    ('admin', 'Generic admin event'),
    ('error', 'Some event that causes an error'),
    ('xero', 'Generic xero log entry'),
)


class Log(models.Model):
    logtype = models.CharField(
        "Type of action/event", choices=LOG_TYPES, max_length=30)
    description = models.CharField(
        "Description of action/event", max_length=500)
    data = models.TextField("Extra data for debugging action/event")
    date = models.DateTimeField(auto_now_add=True)


class UserEventLog(Log):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, "User affected by action")


class EventLog(Log):
    pass


# this needs to be here because it relies on the models defined above
from memberportal.helpers import log_user_event


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_superuser=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

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
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    password_reset_key = models.UUIDField(default=None, blank=True, null=True)
    password_reset_expire = models.DateTimeField(default=None, blank=True, null=True)
    staff = models.BooleanField(default=False)  # an admin user for the portal
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = 'email'
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

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            "Sorry, that email has already been used.",
            code='duplicate_username',
        )

    def __send_email(self, subject, body):
        if "SENDGRID_API_KEY" in os.environ:
            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = sendgrid.Email(settings.FROM_EMAIL)
            to_email = sendgrid.Email(self.email)
            subject = subject
            content = Content("text/html", body)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())

            if response.status_code == 202:
                log_user_event(self, "Sent email with subject: " + subject, "email", "Email content: " + body)
                return True

        log_user_event(self, "Failed to send email with subject: " + subject, "email", "Email content: " + body)
        raise RuntimeError("No SendGrid API key found in environment variables.")

    def email_notification(self, subject, title, preheader, message):
        email_vars = {"preheader": preheader,
                      "title": title, "message": message}
        email_string = render_to_string(
            'email_without_button.html', {'email': email_vars})

        if self.__send_email(subject, email_string):
            return True

    def email_password_reset(self, link):
        email_vars = {"link": link}
        email_string = render_to_string('email_password_reset.html', {'email': email_vars})

        if self.__send_email("Reset your HSBNE password", email_string):
            return True

    def email_link(self, subject, title, preheader, message, link, btn_text):
        email_vars = {"preheader": preheader,
                      "title": title,
                      "message": message,
                      "link": link,
                      "btn_text": btn_text}
        email_string = render_to_string(
            'email_with_button.html', {'email': email_vars})

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
            'email_invoice.html', {'invoice': invoice})

        if self.__send_email("You have a new invoice from HSBNE ({})".format(number), email_string):
            return True

        return False

    def email_welcome(self):
        email_string = render_to_string('email_welcome.html')

        if self.__send_email("Welcome to HSBNE", email_string):
            return "Successfully sent welcome email to user. ✉"

        return False

    def email_disable_member(self):
        if self.email_notification(
                "Your HSBNE site access has been disabled.",
                "Your access has been disabled.",
                "Your HSBNE site access has been disabled.",
                "Your access to HSBNE has been disabled. This could be due to overdue membership fees, a ban being "
                "issued or your membership ending. If this is because of a ban, you are not allowed back on site until "
                "your ban has ended and your membership has been reactivated."):
            return True

        return False

    def email_enable_member(self):
        if self.email_notification(
                "Your HSBNE site access has been enabled.",
                "Your access has been enabled.",
                "Your HSBNE site access has been enabled.",
                "Great news! Your access to HSBNE has been enabled."):
            return True

        return False

    def reset_password(self):
        log_user_event(self, "Password reset requested", "profile")
        self.password_reset_key = uuid.uuid4()
        self.password_reset_expire = timezone.now() + timedelta(hours=24)
        self.save()
        self.email_password_reset("https://portal.hsbne.org" + reverse('reset_password', kwargs={'reset_token': self.password_reset_key}))

        return True


class MemberTypes(models.Model):
    name = models.CharField("Member Type Name", max_length=20)
    conditions = models.CharField("Membership Conditions", max_length=100)
    cost = models.IntegerField("Monthly Cost")

    def __str__(self):
        return self.name + " - ${} per mth. {}".format(
            self.cost, self.conditions)


class Profile(models.Model):
    STATES = (
        ('noob', 'New Member'),
        ('active', 'Active Member'),
        ('inactive', 'Inactive Member'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    screen_name = models.CharField("Screen Name", max_length=30)
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '0417123456'. "
                "Up to 12 characters allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=12, blank=True)
    state = models.CharField(max_length=8, default='noob', choices=STATES)

    member_type = models.ForeignKey(MemberTypes, on_delete=models.PROTECT, related_name='member_type')
    causes = models.ManyToManyField('causes.Causes')

    rfid = models.CharField("RFID Tag", max_length=20, unique=True, null=True, blank=True)
    doors = models.ManyToManyField('access.Doors', blank=True)
    interlocks = models.ManyToManyField('access.Interlock', blank=True)
    spacebucks_balance = models.FloatField(default=0.0)
    last_spacebucks_purchase = models.DateTimeField(default=timezone.now)
    must_update_profile = models.BooleanField(default=False)

    last_seen = models.DateTimeField(default=None, blank=True, null=True)
    last_invoice = models.DateTimeField(default=None, blank=True, null=True)

    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True, default="")
    stripe_card_expiry = models.CharField(max_length=10, blank=True, null=True, default="")
    stripe_card_last_digits = models.CharField(max_length=4, blank=True, null=True, default="")
    xero_account_id = models.CharField(max_length=100, blank=True, null=True, default="")
    xero_account_number = models.CharField(max_length=6, blank=True, null=True, default="")

    # for now our permissions are stored here
    can_manage_access = models.BooleanField("Can manage access", default=False)
    can_disable_members = models.BooleanField("Can disable members", default=False)
    can_see_members_personal_details = models.BooleanField("Can see member personal details", default=False)
    can_see_members_spacebucks = models.BooleanField("Can see member spacebucks details", default=False)
    can_see_members_logs = models.BooleanField("Can see member logs", default=False)
    can_manage_doors = models.BooleanField("Can manage doors", default=False)
    can_manage_interlocks = models.BooleanField("Can manage interlocks", default=False)
    can_manage_causes = models.BooleanField("Can manage causes", default=False)
    can_add_cause = models.BooleanField("Can add a cause", default=False)
    can_manage_cause = models.ManyToManyField("causes.Causes", blank=True, related_name="can_manage_cause")
    can_generate_invoice = models.BooleanField("Can generate & email invoice", default=False)

    BRACKETS = (
        ('low', '$0/wk to $550/wk'),
        ('medium', '$550/wk to $950/wk'),
        ('high', '$950/wk or more'),
    )

    updated_starving_details = models.DateTimeField(null=True)
    studying_fulltime = models.BooleanField(default=False)
    centrelink = models.BooleanField(default=False)
    healthcare_card = models.BooleanField(default=False)
    income_bracket = models.CharField(max_length=10, default="high", choices=BRACKETS)
    special_consideration = models.BooleanField(default=False)
    special_consideration_note = models.TextField(max_length=500, null=True, blank=True)
    starving_override = models.BooleanField(default=False)  # override requirements and grant them starving status

    def is_starving_eligible(self):
        if self.starving_override:
            return True

        eligible = False
        criteria_met = 0

        if self.studying_fulltime:
            criteria_met += 1

        if self.centrelink:
            criteria_met += 1

        if self.healthcare_card:
            criteria_met += 1

        if criteria_met > 0:
            eligible = True

        if self.income_bracket != "low":
            eligible = False

        return eligible

    def deactivate(self):
        log_user_event(self.user, "Deactivated member", "profile")
        self.user.email_disable_member()
        self.state = "inactive"
        self.save()
        return True

    def activate(self):
        log_user_event(self.user, "Activated member", "profile")
        if self.state is not "noob":
            self.user.email_enable_member()

        self.state = "active"
        self.save()
        return True

    def email_profile_to(self, to_email):
        causes = self.causes.all()
        causes_string = "none :("

        if causes.count() == 3:
            causes_string = "{}, {} and {}".format(causes[0], causes[1], causes[2])
        elif causes.count() == 2:
            causes_string = "{} and {}".format(causes[0], causes[1])
        elif causes.count() == 1:
            causes_string = causes[0]

        message = "{} has just signed up. Their membership level is {} and their selected causes are {}. " \
                  "Their email is {}.".format(self.get_full_name(), self.member_type, causes_string, self.user.email)
        email_vars = {"preheader": "", "title": "New member signup", "message": message}
        email_string = render_to_string('email_without_button.html', {'email': email_vars})
        subject = "A new member signed up! ({})".format(self.get_full_name())

        if "SENDGRID_API_KEY" in os.environ:
            sg = sendgrid.SendGridAPIClient(
                apikey=os.environ.get('SENDGRID_API_KEY'))

            from_email = sendgrid.Email(settings.FROM_EMAIL)
            to_email = sendgrid.Email(to_email)
            content = Content("text/html", email_string)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())

            if response.status_code == 202:
                log_user_event(self.user, "Sent email with subject: " + subject, "email", "Email content: " + email_string)
                return True

        log_user_event(self.user, "Failed to send email with subject: " + subject, "email", "Email content: " + email_string)
        return False

    def get_logs(self):
        return UserEventLog.objects.filter(user=self.user)

    def __str__(self):
        return str(self.user)

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def update_last_seen(self):
        self.last_seen = timezone.now()
        return self.save()

    def get_xero_contact(self):
        return get_xero_contact(self)

    def add_to_xero(self):
        return add_to_xero(self)

    def create_membership_invoice(self, email_invoice=True):
        return create_membership_invoice(self.user, email_invoice)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Profile, self).save(*args, **kwargs)
