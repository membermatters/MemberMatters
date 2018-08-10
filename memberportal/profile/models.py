from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import datetime
import pytz
import os
import sendgrid
from sendgrid.helpers.mail import *
import uuid
from django.template.loader import render_to_string
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.conf import settings
from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroBadRequest

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
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

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
    password_reset_expire = models.DateTimeField(
        default=None, blank=True, null=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
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
            sg = sendgrid.SendGridAPIClient(
                apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = sendgrid.Email(settings.FROM_EMAIL)
            to_email = sendgrid.Email(self.email)
            subject = subject
            content = Content("text/html", body)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())

            if response.status_code == 202:
                log_user_event(
                    self, "Sent email with subject: " + subject, "email",
                          "Email content: " + body)
                return True

        log_user_event(
            self, "Failed to send email with subject: " + subject,
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
            return "Successfully sent welcome email to user."

        return False

    def email_disable_member(self):
        if self.email_notification(
                "Your HSBNE site access has been disabled.",
                "Your access has been disabled.",
                "Your HSBNE site access has been disabled.",
                "Your access to HSBNE has been disabled. This could be due to overdue membership fees, a ban being "
                "issued or your membership ending. If this is temporary, you are not allowed back on site until your "
                "membership has been reactivated."):
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
        self.email_link(
            "Password reset request for your HSBNE account",
            "HSBNE Password Reset",
            "Password reset request for your HSBNE account",
            "Someone has issued a password reset for your HSBNE account. "
            "The link below will expire in 24 hours. If this wasn't you, "
            "just ignore this email and nothing will happen.",
            "https://portal.hsbne.org" + reverse(
                'reset_password',
                kwargs={'reset_token': self.password_reset_key}),
            "Reset Password")

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

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    screen_name = models.CharField("Screen Name", max_length=30)
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '0417123456'. Up to 12 characters allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=12, blank=True)  # validators should be a list
    state = models.CharField(max_length=8, default='noob', choices=STATES)
    member_type = models.ForeignKey(
        MemberTypes, on_delete=models.PROTECT, related_name='member_type')
    causes = models.ManyToManyField('causes.Causes')
    rfid = models.CharField(
        "RFID Tag", max_length=20, unique=True, null=True, blank=True)
    doors = models.ManyToManyField('access.Doors', blank=True)
    interlocks = models.ManyToManyField('access.Interlock', blank=True)
    spacebucks_balance = models.FloatField(default=0.0)
    last_seen = models.DateTimeField(default=None, null=True)
    last_invoice = models.DateTimeField(default=None, null=True)
    stripe_customer_id = models.CharField(
        max_length=100, blank=True, null=True, default="")
    stripe_card_expiry = models.CharField(
        max_length=10, blank=True, null=True, default="")
    stripe_card_last_digits = models.CharField(
        max_length=4, blank=True, null=True, default="")
    xero_account_id = models.CharField(max_length=100, blank=True, null=True, default="")
    xero_account_number = models.CharField(max_length=6, blank=True, null=True, default="")

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
        """
        Returns an object with the xero contact details or None if it doesn't exist.
        :return:
        """

        if "XERO_CONSUMER_KEY" in os.environ and "XERO_RSA_FILE" in os.environ:
            with open(os.environ.get('XERO_RSA_FILE')) as keyfile:
                rsa_key = keyfile.read()
            credentials = PrivateCredentials(os.environ.get('XERO_CONSUMER_KEY'), rsa_key)
            xero = Xero(credentials)
            email = xero.contacts.filter(EmailAddress=self.user.email)
            name = xero.contacts.filter(Name=self.get_full_name())

            if email:
                return email

            elif name:
                return name

            return None

        else:
            return "Invalid Xero API details."

    def __generate_account_number(self):
        if "XERO_CONSUMER_KEY" in os.environ and "XERO_RSA_FILE" in os.environ:
            with open(os.environ.get('XERO_RSA_FILE')) as keyfile:
                rsa_key = keyfile.read()
            credentials = PrivateCredentials(os.environ.get('XERO_CONSUMER_KEY'), rsa_key)
            xero = Xero(credentials)
            contacts = xero.contacts.filter(includeArchived=True)

            for x in range(100, 999):
                account_number = self.first_name[0] + self.last_name[:2] + str(x)
                account_number = account_number.upper()

                if not any(d.get('AccountNumber', None) == account_number for d in contacts):
                    self.xero_account_number = account_number
                    self.save()
                    print(account_number)

                    return self.xero_account_number

        else:
            return False

    def add_to_xero(self):
        member_exists = self.xero_account_id is not "" and self.xero_account_number is not ""
        print(member_exists)

        if member_exists:
            result = "Error adding to xero, that email or contact name already exists."
            print(result)
            return result

        else:
            if "XERO_CONSUMER_KEY" in os.environ and "XERO_RSA_FILE" in os.environ:
                with open(os.environ.get('XERO_RSA_FILE')) as keyfile:
                    rsa_key = keyfile.read()
                credentials = PrivateCredentials(os.environ.get('XERO_CONSUMER_KEY'), rsa_key)
                xero = Xero(credentials)

                contact = [
                    {
                        "AccountNumber": self.__generate_account_number(),
                        "ContactStatus": "ACTIVE",
                        "Name": self.get_full_name(),
                        "FirstName": self.first_name,
                        "LastName": self.last_name,
                        "EmailAddress": self.user.email,
                        "Addresses": [
                            {
                                "AddressType": "STREET",
                                "City": "",
                                "Region": "",
                                "PostalCode": "",
                                "Country": "",
                                "AttentionTo": ""
                            }
                        ],
                        "Phones": [
                            {
                                "PhoneType": "DEFAULT",
                                "PhoneNumber": self.phone,
                                "PhoneAreaCode": "",
                                "PhoneCountryCode": ""
                            }
                        ],
                        "IsSupplier": False,
                        "IsCustomer": True,
                        "DefaultCurrency": "AU"
                    }
                ]

                try:
                    result = xero.contacts.put(contact)

                except XeroBadRequest as e:
                    return "Error: " + str(e)

                if result:
                    print(result)
                    self.xero_account_id = result[0]['ContactID']
                    self.save()
                    return "Successfully added to Xero."

                else:
                    return "Error adding to Xero."

            else:
                return "Error adding to Xero. No Xero API details."

    def create_membership_invoice(self):
        next_month = datetime.date.today().month + 1
        this_year = datetime.date.today().year
        if next_month == 13:
            next_month = 1
            this_year += 1

        next_month_date = datetime.datetime(this_year, next_month, 1)

        payload = {
            "Type": "ACCREC",
            "Contact": {
                "ContactID": self.xero_account_id
            },
            "DueDate": next_month_date,
            "LineAmountTypes": "Inclusive",
            "LineItems": [
                {
                    "Description": "HSBNE Membership: " + self.member_type.name,
                    "Quantity": "1",
                    "ItemCode": self.member_type.name,
                    "UnitAmount": self.member_type.cost,
                    "TaxType": "OUTPUT",
                    "AccountCode": "200"
                }
            ],
            "Status": "AUTHORISED",
            "Reference": self.xero_account_number,
            "Url": "https://hsbne.org",
        }

        if "XERO_CONSUMER_KEY" in os.environ and "XERO_RSA_FILE" in os.environ:
            with open(os.environ.get('XERO_RSA_FILE')) as keyfile:
                rsa_key = keyfile.read()
            credentials = PrivateCredentials(os.environ.get('XERO_CONSUMER_KEY'), rsa_key)
            xero = Xero(credentials)

            # Monkey patch the library to support online invoices.
            def get_onlineinvoice(id, headers=None, summarize_errors=None):
                uri = '/'.join([xero.invoices.base_url, xero.invoices.name, id, 'OnlineInvoice'])
                params = {}
                if not summarize_errors:
                    params['summarizeErrors'] = 'false'
                return uri, params, 'get', None, headers, False

            xero.invoices.get_onlineinvoice = xero.invoices._get_data(get_onlineinvoice)

            try:
                # try to create the invoice
                result = xero.invoices.put(payload)

                invoice_id = result[0]['InvoiceID']
                invoice_number = result[0]['InvoiceNumber']
                invoice_reference = result[0]['Reference']
                invoice_link = xero.invoices.get_onlineinvoice(invoice_id)['OnlineInvoices'][0]['OnlineInvoiceUrl']

                # if we're successful send it to the member and log it
                self.user.email_invoice(self.first_name, self.member_type.cost, invoice_number, next_month_date.strftime("%d-%m-%Y"), invoice_reference, invoice_link)
                log_user_event(self.user, "Created invoice for $" + str(self.member_type.cost) + "(" + invoice_id + ")",
                               "xero")
                self.last_invoice = timezone.now()
                self.save()

            except XeroBadRequest as e:
                log_user_event(self.user, "Error creating invoice for $" + str(self.member_type.cost),
                               "xero")
                return "Error: " + str(e)

            if result:
                return "Successfully created invoice {} in Xero.".format(invoice_number)

            else:
                return "Error creating invoice in Xero."

        else:
            return "Error created invoice in Xero. No Xero API details."
