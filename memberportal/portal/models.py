from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
import pytz
import os
import sendgrid
from sendgrid.helpers.mail import *
from django.template.loader import render_to_string

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
    type = models.CharField("Type of action/event", choices=LOG_TYPES, max_length=30)
    description = models.CharField("Description of action/event", max_length=500)
    data = models.TextField("Extra data for debugging action/event")
    date = models.DateTimeField(auto_now_add=True)


def log_user_event(user, description, event_type, data=""):
    UserEventLog(description=description, type=event_type, user=user, data=data).save()


class EventLog(models.Model):
    type = models.CharField("Type of action/event", choices=LOG_TYPES, max_length=30)
    description = models.CharField("Description of action/event", max_length=500)
    data = models.TextField("Extra data for debugging action/event")
    date = models.DateTimeField(auto_now_add=True)


def log_event(description, event_type, data=""):
    EventLog(description=description, type=event_type, data=data).save()


class MemberTypes(models.Model):
    name = models.CharField("Member Type Name", max_length=20)
    conditions = models.CharField("Membership Conditions", max_length=100)
    cost = models.IntegerField("Monthly Cost")

    def __str__(self):
        return self.name + " - ${} per mth. {}".format(
            self.cost, self.conditions)


class Causes(models.Model):
    name = models.CharField("Cause Name", max_length=20, unique=True)
    description = models.CharField("Cause Description", max_length=100)

    def get_active_count(self):
        return str(self.profile_set.filter(state="active").count())

    def get_quorum(self):
        quorum = self.profile_set.filter(state="active").count() * 0.4
        if quorum < 3:
            quorum = 3
        return str(quorum)

    def get_active_set(self):
        return self.profile_set.filter(state="active")

    def __str__(self):
        return self.name


class Doors(models.Model):
    name = models.CharField("Door Name", max_length=20, unique=True)
    description = models.CharField("Door Description/Location", max_length=100)
    ip_address = models.GenericIPAddressField(
        "IP Address of Door", unique=True, null=True, blank=True)
    last_seen = models.DateTimeField(null=True)
    all_members = models.BooleanField(
        "Members have access by default", default=False)

    def checkin(self):
        log_event(self.name + " checked in with server.", "door")
        self.last_seen = datetime.now()
        self.save()

    def get_unavailable(self):
        utc = pytz.UTC
        if self.last_seen:
            if utc.localize(datetime.now()) - timedelta(minutes=5) > self.last_seen:
                return True

        return False

    def unlock(self):
        import requests
        r = requests.get('http://{}/open?key=key'.format(self.ip_address))
        if r.status_code == 200:
            log_event(self.name + " unlocked from admin interface.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return True
        else:
            log_event(self.name + " unlock from admin interface failed.", "door", "Status: {}. Content: {}".format(r.status_code, r.content))
            return False

    def log_access(self, member_id):
        DoorLog(user=User.objects.get(pk=member_id), door=self).save()

    def __str__(self):
        return self.name


class DoorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    door = models.ForeignKey(Doors, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)


class Profile(models.Model):
    STATES = (
        ('noob', 'New Member'),
        ('active', 'Active Member'),
        ('inactive', 'Inactive Member'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    state = models.CharField(max_length=8, default='noob', choices=STATES)
    member_type = models.ForeignKey(
        MemberTypes, on_delete=models.PROTECT, related_name='member_type')
    causes = models.ManyToManyField(Causes)
    rfid = models.CharField(
        "RFID Tag", max_length=20, unique=True, null=True, blank=True)
    doors = models.ManyToManyField(Doors, blank=True)
    spacebucks_balance = models.FloatField(default=0.0)
    stripe_customer_id = models.CharField(max_length=100, null=True, default=None)
    stripe_card_expiry = models.CharField(max_length=10, null=True, default=None)
    stripe_card_last_digits = models.CharField(max_length=4, null=True, default=None)


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
            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email(FROM_EMAIL)
            to_email = Email(self.user.email)
            subject = subject
            content = Content("text/html", body)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())

            if response.status_code == 202:
                log_user_event(self.user, "Sent email with subject: " + subject, "email", "Email content: " + body)
                return True

        log_user_event(self.user, "Failed to send email with subject: " + subject, "email", "Email content: " + body)
        return False

    def email_notification(self, subject, title, preheader, message):
        email_vars = {"preheader": preheader, "title": title, "message": message}
        email_string = render_to_string('email_without_button.html', {'email': email_vars})

        if self.__send_email(subject, email_string):
            return True

    def email_link(self, subject, title, preheader, message, link, btn_text):
        email_vars = {"preheader": preheader, "title": title, "message": message, "link": link, "btn_text": btn_text}
        email_string = render_to_string('email_with_button.html', {'email': email_vars})

        if self.__send_email(subject, email_string):
            return True

        return False

    def email_welcome(self):
        name = self.user.first_name
        email_vars = {"name": name}
        email_string = render_to_string('email_welcome.html', {'email': email_vars})

        if self.__send_email("Welcome to HSBNE " + name, email_string):
            return True

        return False

    def email_disable_member(self):
        if self.email_notification("Your HSBNE site access has been disabled.",
                                "Your access has been disabled.",
                                "Your HSBNE site access has been disabled.",
                                "Unfortunately, your access to HSBNE has been disabled. This could be due to overdue "
                                "membership fees, a ban being issued or your membership ending."):
            return True

        return False

    def email_enable_member(self):
        if self.email_notification("Your HSBNE site access has been enabled.",
                                "Your access has been enabled.",
                                "Your HSBNE site access has been eabled.",
                                "Great news! Your access to HSBNE has been enabled."):
            return True

        return False


class SpaceBucks(models.Model):
    TRANSACTION_TYPES = (
        ('stripe', 'Stripe Payment'),
        ('bank', 'Bank Transfer'),
        ('card', 'Membership Card')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField("Amount")
    transaction_type = models.CharField(
        "Transaction Type", max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(
        "Description of Transaction", max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    logging_info = models.TextField("Detailed logging info from stripe.", blank=True)

    def save(self, *args, **kwargs):
        super(SpaceBucks, self).save(*args, **kwargs)
        balance = SpaceBucks.objects.filter(user=self.user).aggregate(Sum('amount'))['amount__sum']
        print(balance)
        self.user.profile.spacebucks_balance = balance
        self.user.profile.save()
