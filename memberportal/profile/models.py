from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
import pytz
import os
import sendgrid
from sendgrid.helpers.mail import *
import uuid
from django.template.loader import render_to_string

utc = pytz.UTC

FROM_EMAIL = '"HSBNE Member Portal" <contact@hsbne.org>'

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
)


class UserEventLog(models.Model):
    user = models.ForeignKey(User, "User affected by action")
    logtype = models.CharField(
        "Type of action/event", choices=LOG_TYPES, max_length=30)
    description = models.CharField(
        "Description of action/event", max_length=500)
    data = models.TextField("Extra data for debugging action/event")
    date = models.DateTimeField(auto_now_add=True)


class EventLog(models.Model):
    logtype = models.CharField(
        "Type of action/event", choices=LOG_TYPES, max_length=30)
    description = models.CharField(
        "Description of action/event", max_length=500)
    data = models.TextField("Extra data for debugging action/event")
    date = models.DateTimeField(auto_now_add=True)


class MemberTypes(models.Model):
    name = models.CharField("Member Type Name", max_length=20)
    conditions = models.CharField("Membership Conditions", max_length=100)
    cost = models.IntegerField("Monthly Cost")

    def __str__(self):
        return self.name + " - ${} per mth. {}".format(
            self.cost, self.conditions)


from memberportal.helpers import log_user_event


class Profile(models.Model):
    STATES = (
        ('noob', 'New Member'),
        ('active', 'Active Member'),
        ('inactive', 'Inactive Member'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    password_reset_key = models.UUIDField(default=None, blank=True, null=True)
    password_reset_expire = models.DateTimeField(
        default=None, blank=True, null=True)
    state = models.CharField(max_length=8, default='noob', choices=STATES)
    member_type = models.ForeignKey(
        MemberTypes, on_delete=models.PROTECT, related_name='member_type')
    causes = models.ManyToManyField('causes.Causes')
    rfid = models.CharField(
        "RFID Tag", max_length=20, unique=True, null=True, blank=True)
    doors = models.ManyToManyField('access.Doors', blank=True)
    spacebucks_balance = models.FloatField(default=0.0)
    stripe_customer_id = models.CharField(
        max_length=100, blank=True, null=True, default="")
    stripe_card_expiry = models.CharField(
        max_length=10, blank=True, null=True, default="")
    stripe_card_last_digits = models.CharField(
        max_length=4, blank=True, null=True, default="")

    def deactivate(self):
        log_user_event(self.user, "Deactivated member", "profile")
        self.email_disable_member()
        self.state = "inactive"
        self.save()

    def activate(self):
        log_user_event(self.user, "Activated member", "profile")
        if self.state == "noob":
            self.email_welcome()

        else:
            self.email_enable_member()

        self.state = "active"
        self.save()

    def get_logs(self):
        return UserEventLog.objects.filter(user=self.user)

    def __str__(self):
        return str(self.user)

    def __send_email(self, subject, body):
        if "SENDGRID_API_KEY" in os.environ:
            sg = sendgrid.SendGridAPIClient(
                apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = sendgrid.Email(FROM_EMAIL)
            to_email = sendgrid.Email(self.user.email)
            subject = subject
            content = Content("text/html", body)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())

            if response.status_code == 202:
                log_user_event(
                    self.user, "Sent email with subject: " + subject, "email",
                    "Email content: " + body)
                return True

        log_user_event(
            self.user, "Failed to send email with subject: " + subject,
            "email", "Email content: " + body)
        return False

    def email_notification(self, subject, title, preheader, message):
        email_vars = {"preheader": preheader,
                      "title": title, "message": message}
        email_string = render_to_string(
            'email_without_button.html', {'email': email_vars})

        if self.__send_email(subject, email_string):
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

    def email_welcome(self):
        name = self.user.first_name
        email_vars = {"name": name}
        email_string = render_to_string(
            'email_welcome.html', {'email': email_vars})

        if self.__send_email("Welcome to HSBNE " + name, email_string):
            return True

        return False

    def email_disable_member(self):
        if self.email_notification(
                "Your HSBNE site access has been disabled.",
                "Your access has been disabled.",
                "Your HSBNE site access has been disabled.",
                "Unfortunately, your access to HSBNE has been disabled. This "
                "could be due to overdue membership fees, a ban being issued "
                "or your membership ending."):
            return True

        return False

    def email_enable_member(self):
        if self.email_notification(
                "Your HSBNE site access has been enabled.",
                "Your access has been enabled.",
                "Your HSBNE site access has been eabled.",
                "Great news! Your access to HSBNE has been enabled."):
            return True

        return False

    def reset_password(self):
        log_user_event(self.user, "Password reset requested", "profile")
        self.password_reset_key = uuid.uuid4()
        self.password_reset_expire = datetime.now() + timedelta(hours=24)
        self.save()
        self.email_link(
            "Password reset request for you HSBNE account",
            "HSBNE Password Reset",
            "Password reset request for you HSBNE account",
            "Someone has issued a password reset for your HSBNE account. "
            "The link below will expire in 24 hours. If this wasn't you, "
            "just ignore this email and nothing will happen.",
            "https://portal.hsbne.org" + reverse(
                'reset_password',
                kwargs={'reset_token': self.password_reset_key}),
            "Reset Password")

        return True
