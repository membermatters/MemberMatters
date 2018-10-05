from django.utils import timezone
from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroBadRequest
import datetime
import os


def get_xero_contact(user):
    """
    Returns an object with the xero contact details or None if it
     doesn't exist.
    :return:
    """

    if "XERO_CONSUMER_KEY" in os.environ and "XERO_RSA_FILE" in os.environ:
        with open(os.environ.get('XERO_RSA_FILE')) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(
            os.environ.get('XERO_CONSUMER_KEY'), rsa_key)
        xero = Xero(credentials)
        email = xero.contacts.filter(EmailAddress=user.profile.email)
        name = xero.contacts.filter(Name=user.profile.get_full_name())

        if email:
            return email

        elif name:
            return name

        return None

    else:
        return "Invalid Xero API details."


def generate_account_number(profile):
    if "XERO_CONSUMER_KEY" in os.environ and "XERO_RSA_FILE" in os.environ:
        with open(os.environ.get('XERO_RSA_FILE')) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(
            os.environ.get('XERO_CONSUMER_KEY'), rsa_key)
        xero = Xero(credentials)
        contacts = xero.contacts.filter(includeArchived=True)

        for x in range(100, 999):
            account_number = profile.first_name[0] + profile.last_name[:2] + str(x)
            account_number = account_number.upper()

            if not any(d.get('AccountNumber', None) == account_number for d in contacts):
                profile.xero_account_number = account_number
                profile.save()
                print("Generated Xero Account: " + account_number)

                return profile.xero_account_number

    else:
        return False


def add_to_xero(profile):
    member_exists = profile.xero_account_id is not "" and profile.xero_account_number is not ""

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
                    "AccountNumber": generate_account_number(profile),
                    "ContactStatus": "ACTIVE",
                    "Name": profile.get_full_name(),
                    "FirstName": profile.first_name,
                    "LastName": profile.last_name,
                    "EmailAddress": profile.user.email,
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
                            "PhoneNumber": profile.phone,
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
                profile.xero_account_id = result[0]['ContactID']
                profile.save()
                return "Successfully added to Xero."

            else:
                return "Error adding to Xero."

        else:
            return "Error adding to Xero. No Xero API details."


def create_membership_invoice(user):
    next_month = datetime.date.today().month + 1
    this_year = datetime.date.today().year
    if next_month == 13:
        next_month = 1
        this_year += 1

    next_month_date = datetime.datetime(this_year, next_month, 1)

    payload = {
        "Type": "ACCREC",
        "Contact": {
            "ContactID": user.profile.xero_account_id
        },
        "DueDate": next_month_date,
        "LineAmountTypes": "Inclusive",
        "LineItems": [
            {
                "Description": "HSBNE Membership: " + user.profile.member_type.name,
                "Quantity": "1",
                "ItemCode": user.profile.member_type.name,
                "UnitAmount": user.profile.member_type.cost,
                "TaxType": "OUTPUT",
                "AccountCode": "200"
            }
        ],
        "Status": "AUTHORISED",
        "Reference": user.profile.xero_account_number,
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

            from memberportal.helpers import log_user_event

            # try to create the invoice
            result = xero.invoices.put(payload)

            invoice_id = result[0]['InvoiceID']
            invoice_number = result[0]['InvoiceNumber']
            invoice_reference = result[0]['Reference']
            invoice_link = xero.invoices.get_onlineinvoice(invoice_id)['OnlineInvoices'][0]['OnlineInvoiceUrl']

            # if we're successful send it to the member and log it
            user.email_invoice(user.profile.first_name, user.profile.member_type.cost, invoice_number, next_month_date.strftime("%d-%m-%Y"), invoice_reference, invoice_link)
            log_user_event(user.user, "Created invoice for $" + str(user.profile.member_type.cost) + "(" + invoice_id + ")", "xero")
            user.profile.last_invoice = timezone.now()
            user.profile.save()

        except XeroBadRequest as e:
            log_user_event(user, "Error creating invoice for $" + str(user.profile.member_type.cost), "xero")
            return "Error: " + str(e)

        if result:
            return "Successfully created invoice {} in Xero.".format(invoice_number)

        else:
            return "Error creating invoice in Xero."

    else:
        return "Error created invoice in Xero. No Xero API details."
