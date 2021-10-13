from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroBadRequest
from constance import config
import datetime
import os

xero_rsa = os.environ.get("PORTAL_XERO_RSA_FILE", "/usr/src/data/xerkey.pem")


def get_xero_contact(user):
    """
    Returns an object with the xero contact details or None if it
     doesn't exist.
    :return:
    """

    if "PORTAL_XERO_CONSUMER_KEY" in os.environ:
        with open(xero_rsa) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(
            os.environ.get("PORTAL_XERO_CONSUMER_KEY"), rsa_key
        )
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
    if "PORTAL_XERO_CONSUMER_KEY" in os.environ:
        with open(xero_rsa) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(
            os.environ.get("PORTAL_XERO_CONSUMER_KEY", "/usr/src/data/xerkey.pem"),
            rsa_key,
        )
        xero = Xero(credentials)
        contacts = xero.contacts.filter(includeArchived=True)

        for x in range(100, 999):
            account_number = profile.first_name[0] + profile.last_name[:2] + str(x)
            account_number = account_number.upper()

            if not any(
                d.get("AccountNumber", None) == account_number for d in contacts
            ):
                profile.xero_account_number = account_number
                profile.save()
                print("Generated Xero Account: " + account_number)

                return profile.xero_account_number

    else:
        return False


def sync_xero_accounts(users):
    if "PORTAL_XERO_CONSUMER_KEY" in os.environ:
        with open(xero_rsa) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(
            os.environ.get("PORTAL_XERO_CONSUMER_KEY", "/usr/src/data/xerkey.pem"),
            rsa_key,
        )
        xero = Xero(credentials)
        contacts = xero.contacts.filter(includeArchived=True)
        matches = []
        non_matches = []

        for user in users:
            profile = user.profile
            if profile.state == "noob":
                print(
                    "Not syncing new member ({} {}).".format(
                        user.profile.get_full_name(), user.email
                    )
                )
                continue
            if profile.xero_account_id or profile.xero_account_number:
                print(
                    "{} already has xero details ({} {})".format(
                        user.profile.get_full_name(),
                        profile.xero_account_number,
                        profile.xero_account_id,
                    )
                )
                continue
            else:
                contact = next(
                    (
                        item
                        for item in contacts
                        if str(item["EmailAddress"]).lower() == str(user.email).lower()
                    ),
                    None,
                )
                if contact:
                    print(
                        "Found match for {} ({})".format(
                            profile.get_full_name(), user.email
                        )
                        + str(contact)
                    )
                    if "AccountNumber" not in contact:
                        if contact["ContactStatus"] == "ARCHIVED":
                            continue
                        else:
                            raise FileNotFoundError(
                                "No account number exists for "
                                + user.profile.get_full_name()
                            )
                    user.profile.xero_account_number = contact["AccountNumber"]
                    user.profile.xero_account_id = contact["ContactID"]
                    user.profile.save()
                    matches.append(user)
                else:
                    print(
                        "No match found for {} ({})".format(
                            profile.get_full_name(), user.email
                        )
                    )
                    non_matches.append(user)

        message = "\nDone syncing {} users. Found {} matches and {} non-matches. {} users untouched.".format(
            len(users),
            len(matches),
            len(non_matches),
            str(len(users) - (len(matches) + len(non_matches))),
        )
        print(message)
        print("\nMatched Users:")
        for match in matches:
            print(match.profile.get_full_name())
        print("\nNon-matched Users:")
        for non_match in non_matches:
            print(non_match.profile.get_full_name() + " " + non_match.email)

        non_matches_string = ""
        for non_match in non_matches:
            non_matches_string += "{} ({}), ".format(
                non_match.profile.get_full_name(), non_match.email
            )

        return message + "Non matches: " + non_matches_string

    else:
        return False


def add_to_xero(profile):
    if "PORTAL_XERO_CONSUMER_KEY" in os.environ:
        with open(xero_rsa) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(
            os.environ.get("PORTAL_XERO_CONSUMER_KEY", "/usr/src/data/xerkey.pem"),
            rsa_key,
        )
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
                        "AttentionTo": "",
                    }
                ],
                "Phones": [
                    {
                        "PhoneType": "DEFAULT",
                        "PhoneNumber": profile.phone,
                        "PhoneAreaCode": "",
                        "PhoneCountryCode": "",
                    }
                ],
                "IsSupplier": False,
                "IsCustomer": True,
                "DefaultCurrency": "AU",
            }
        ]

        try:
            result = xero.contacts.put(contact)

        except XeroBadRequest as e:
            error = str(e)
            if "is already assigned to another contact" in error:
                error = "That contact name is already in Xero."

            return "Error: " + error

        if result:
            print(result)
            profile.xero_account_id = result[0]["ContactID"]
            profile.save()
            return "Successfully added to Xero."

        else:
            return "Error adding to Xero."

    else:
        return "Error adding to Xero. No Xero API details."


def _create_xero_invoice(payload):
    if "PORTAL_XERO_CONSUMER_KEY" in os.environ:
        with open(xero_rsa) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(
            os.environ.get("PORTAL_XERO_CONSUMER_KEY", "/usr/src/data/xerkey.pem"),
            rsa_key,
        )
        xero = Xero(credentials)

        # Monkey patch the library to support online invoices.
        def get_onlineinvoice(id, headers=None, summarize_errors=None):
            uri = "/".join(
                [xero.invoices.base_url, xero.invoices.name, id, "OnlineInvoice"]
            )
            params = {}
            if not summarize_errors:
                params["summarizeErrors"] = "false"
            return uri, params, "get", None, headers, False

        xero.invoices.get_onlineinvoice = xero.invoices._get_data(get_onlineinvoice)

        # try to create the invoice
        result = xero.invoices.put(payload)

        invoice_url = xero.invoices.get_onlineinvoice(result[0]["InvoiceID"])[
            "OnlineInvoices"
        ][0]["OnlineInvoiceUrl"]

        return {
            "invoice_id": result[0]["InvoiceID"],
            "invoice_number": result[0]["InvoiceNumber"],
            "invoice_reference": result[0]["Reference"],
            "invoice_link": invoice_url,
        }

    else:
        return None


def create_membership_invoice(user, email_invoice=False):
    next_month = datetime.date.today().month + 1
    this_year = datetime.date.today().year
    if next_month == 13:
        next_month = 1
        this_year += 1

    next_month_date = datetime.datetime(this_year, next_month, 1)

    line_items = [
        {
            "Description": f"{config.SITE_OWNER}: " + user.profile.member_type.name,
            "Quantity": "1",
            "ItemCode": user.profile.member_type.name,
            "UnitAmount": round(user.profile.member_type.cost * 0.7, 2),
            "TaxType": config.XERO_TAX_TYPE,
            "AccountCode": config.XERO_MEMBERSHIP_ACCOUNT_CODE,
        }
    ]

    payload = {
        "Type": "ACCREC",
        "Contact": {"ContactID": user.profile.xero_account_id},
        "DueDate": next_month_date,
        "LineAmountTypes": "Inclusive",
        "LineItems": line_items,
        "Status": "AUTHORISED",
        "Reference": user.profile.xero_account_number,
        "Url": config.SITE_URL,
    }

    try:
        invoice = _create_xero_invoice(payload)
    except:
        return "Error creating Xero Invoice"

    # if we're successful and email == True send it
    if email_invoice:
        user.email_invoice(
            user.profile.first_name,
            user.profile.member_type.cost,
            invoice["invoice_number"],
            next_month_date.strftime("%d-%m-%Y"),
            invoice["invoice_reference"],
            invoice["invoice_link"],
        )

    # TODO fix the import of this helper
    # log_user_event(
    #     user,
    #     "Created invoice for $"
    #     + str(user.profile.member_type.cost)
    #     + "("
    #     + invoice["invoice_id"]
    #     + ")",
    #     "xero",
    # )

    if invoice:
        return "Successfully created invoice {} in Xero.".format(
            invoice["invoice_number"]
        )

    else:
        return "Error creating invoice in Xero."


def create_stripe_membership_invoice(user, amount, fee_amount):
    line_items = [
        {
            "Description": f"{config.SITE_OWNER} ",
            "Quantity": "1",
            "ItemCode": config.XERO_MEMBERSHIP_ITEM_CODE,
            "UnitAmount": amount,
            "TaxType": config.XERO_TAX_TYPE,
            "AccountCode": config.XERO_MEMBERSHIP_ACCOUNT_CODE,
        },
        {
            "Description": f"Stripe fee",
            "Quantity": "1",
            "ItemCode": config.XERO_STRIPE_FEE_ITEM_CODE,
            "UnitAmount": fee_amount,
            "TaxType": config.XERO_TAX_TYPE,
            "AccountCode": config.XERO_STRIPE_FEE_ACCOUNT_CODE,
        },
    ]

    payload = {
        "Type": "ACCREC",
        "Contact": {"ContactID": user.profile.xero_account_id},
        "DueDate": datetime.datetime.now(),
        "LineAmountTypes": "Inclusive",
        "LineItems": line_items,
        "Status": "AUTHORISED",
        "Reference": user.profile.xero_account_number,
        "Url": config.SITE_URL,
    }

    invoice = _create_xero_invoice(payload)

    # TODO fix the import of this helper
    # log_user_event(
    #     user,
    #     "Created invoice for $" + str(amount) + "(" + invoice["invoice_id"] + ")",
    #     "xero",
    # )

    if invoice:
        return invoice

    else:
        return None


def create_stripe_memberbucks_invoice(user, amount, fee_amount):
    line_items = [
        {
            "Description": f"{config.SITE_OWNER} ",
            "Quantity": "1",
            "ItemCode": config.XERO_MEMBERBUCKS_ITEM_CODE,
            "UnitAmount": amount,
            "TaxType": config.XERO_TAX_TYPE,
            "AccountCode": config.XERO_MEMBERBUCKS_ACCOUNT_CODE,
        },
        {
            "Description": f"Stripe fee",
            "Quantity": "1",
            "ItemCode": config.XERO_STRIPE_FEE_ITEM_CODE,
            "UnitAmount": fee_amount,
            "TaxType": config.XERO_TAX_TYPE,
            "AccountCode": config.XERO_STRIPE_FEE_ACCOUNT_CODE,
        },
    ]

    payload = {
        "Type": "ACCREC",
        "Contact": {"ContactID": user.profile.xero_account_id},
        "DueDate": datetime.datetime.now(),
        "LineAmountTypes": "Inclusive",
        "LineItems": line_items,
        "Status": "AUTHORISED",
        "Reference": user.profile.xero_account_number,
        "Url": config.SITE_URL,
    }

    invoice = _create_xero_invoice(payload)

    # TODO fix the import of this helper
    # log_user_event(
    #     user,
    #     "Created invoice for $" + str(amount) + "(" + invoice["invoice_id"] + ")",
    #     "xero",
    # )

    if invoice:
        return invoice

    else:
        return None
