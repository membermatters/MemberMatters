from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from memberportal.helpers import log_user_event
from .forms import SpacebugForm
import pytz
import os
import requests
from memberportal.decorators import no_noobs, admin_required, api_auth
from xero import Xero
from xero.auth import PrivateCredentials

import sendgrid
from multiprocessing.dummy import Pool as ThreadPool
from django.contrib.auth import get_user_model

User = get_user_model()
from profile.models import Profile

utc = pytz.UTC


def signin(request):
    """
    The sign in view.
    :param request:
    :return:
    """
    log_user_event(request.user, "User logged in.", "usage")
    return render(request, 'registration/login.html')


def loggedout(request):
    """
    The view to show the logged out page.
    :param request:
    :return:
    """
    return render(request, 'loggedout.html')


def home(request):
    """
    The home page view.
    :param request:
    :return:
    """
    return render(request, 'home.html')


@login_required
def spacebug(request):
    form_class = SpacebugForm
    # if this is a submission, handle it and render a thankyou.
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            if "TRELLO_API_KEY" in os.environ and "TRELLO_API_TOKEN" in os.environ:
                issue = request.POST.get('issue', '')
                details = request.POST.get('details', '')
                url = "https://api.trello.com/1/cards"
                trelloKey = os.environ.get('TRELLO_API_KEY')
                trelloToken = os.environ.get('TRELLO_API_TOKEN')

                querystring = {"name": issue, "desc": details, "pos": "top", "idList": "5529dd886d658fdace75c830",
                               "keepFromSource": "all", "key": trelloKey, "token": trelloToken}

                response = requests.request("POST", url, params=querystring)

                if response.status_code == 200:
                    log_user_event(request.user, "Submitted issue: " + issue + " Content: " + details, "generic")
                    messages.success(request, 'Issue submitted successfully. Thanks.')
                    return redirect(reverse('report_spacebug'))

            else:
                return HttpResponseBadRequest("No trello API details found in environment.")

        log_user_event(request.user, "Issue Submit Failed:: " + issue + " content: " + details, "error")
        messages.error(request, 'Issue failed to submit, sorry.')
        return redirect(reverse('report_spacebug'))

    # render template normally
    return render(request, 'spacebug.html', {
        'form': form_class,
    })


def webcams(request):
    return render(request, 'webcams.html')


@login_required
def spacebug(request):
    form_class = SpacebugForm
    # if this is a submission, handle it and render a thankyou.
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            if "TRELLO_API_KEY" in os.environ and "TRELLO_API_TOKEN" in os.environ:
                issue = request.POST.get('issue', '')
                details = request.POST.get('details', '')
                url = "https://api.trello.com/1/cards"
                trelloKey = os.environ.get('TRELLO_API_KEY')
                trelloToken = os.environ.get('TRELLO_API_TOKEN')

                querystring = {"name": issue, "desc": details, "pos": "top", "idList": "5529dd886d658fdace75c830",
                               "keepFromSource": "all", "key": trelloKey, "token": trelloToken}

                response = requests.request("POST", url, params=querystring)

                if response.status_code == 200:
                    log_user_event(request.user, "Submitted issue: " + issue + " Content: " + details, "generic")
                    messages.success(request, 'Issue submitted successfully. Thanks.')
                    return redirect(reverse('report_spacebug'))

            else:
                return HttpResponseBadRequest("No trello API details found in environment.")

        log_user_event(request.user, "Issue Submit Failed:: " + issue + " content: " + details, "error")
        messages.error(request, 'Issue failed to submit, sorry.')
        return redirect(reverse('report_spacebug'))

    # render template normally
    return render(request, 'spacebug.html', {
        'form': form_class,
    })


@api_auth
def invoice_cron(request):
    if "SENDGRID_API_KEY" in os.environ:
        pool = ThreadPool(100)

        def create_invoice(member):
            if member.profile.state == "active":
                if member.profile.last_invoice is not None:
                    if member.profile.last_invoice.month == timezone.now().month:
                        print("already invoiced this month")
                        return {"name": member.profile.get_full_name(), "email": member.email,
                                "success": False, "message": "User already invoiced this month."}

                    elif member.profile.xero_account_id:
                        return {"name": member.profile.get_full_name(), "email": member.email,
                                "success": member.profile.create_membership_invoice(), "message": ""}

                elif member.profile.xero_account_id:
                    return {"name": member.profile.get_full_name(), "email": member.email,
                            "success": member.profile.create_membership_invoice(), "message": ""}

                return {"name": member.profile.get_full_name(), "email": member.email, "success": False,
                        "message": "No contact in xero."}

        results = pool.map(create_invoice, User.objects.all())

        successful = list()
        failed = list()
        successful_string, failed_string = "", ""

        for result in results:
            if result is not None:
                if result['success']:
                    successful.append("{} - {}<br>".format(result['name'], result['email']))
                    successful_string += "{} - {} - {}<br>".format(result['name'], result['email'], result['message'])

                else:
                    failed.append("{} - {} - {}<br>".format(result['name'], result['email'], result['message']))
                    failed_string += "{} - {} - {}<br>".format(result['name'], result['email'], result['message'])

        body = "HSBNE invoice generation ran with {} successful and {} failed.<br>".format(len(successful),
                                                                                           len(failed)) + \
               "Invoice creation for the following members failed: <br>{}<br><br>".format(failed_string) + \
               "Invoice creation for the following members succeeded:<br>{}".format(successful_string)

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = sendgrid.Email(settings.FROM_EMAIL_TREASURER)
        to_email = sendgrid.Email(settings.SYSADMIN_EMAIL)
        subject = "HSBNE invoice generation ran with {} successful and {} failed.".format(len(successful), len(failed))
        content = sendgrid.helpers.mail.Content("text/html", body)
        mail = sendgrid.helpers.mail.Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())

        return HttpResponse(response.status_code)


@api_auth
def overdue_cron(request):
    if "XERO_CONSUMER_KEY" in os.environ and "XERO_RSA_FILE" in os.environ:
        with open(os.environ.get('XERO_RSA_FILE')) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(os.environ.get('XERO_CONSUMER_KEY'), rsa_key)
        xero = Xero(credentials)

        # Monkey patch the library to support pagination.
        def get_contacts(page):
            uri = '/'.join([xero.contacts.base_url, xero.contacts.name, "?page=" + str(page)])
            params = {'summarizeErrors': False}
            return uri, params, 'get', None, None, False

        xero.contacts.get_contacts = xero.contacts._get_data(get_contacts)

        contacts = list()
        page = 0

        while True:
            page += 1
            result = xero.contacts.get_contacts(page)
            contacts += result

            if not result:
                break

        profiles = Profile.objects.all()
        deactivated_members = list()
        activated_members = list()

        for contact in contacts:
            if contact.get('IsCustomer', False) and contact.get('ContactStatus', False) == "ACTIVE":
                contact_id = contact['ContactID']
                try:
                    profile = profiles.get(xero_account_id=contact_id)
                    if contact.get("Balances", False):
                        print(contact["Balances"]["AccountsReceivable"]["Outstanding"])
                        if contact["Balances"]["AccountsReceivable"]["Outstanding"] > 0:
                            if profile.state == "active":
                                profile.deactivate()
                                deactivated_members.append(profile.get_full_name())
                        else:
                            if profile.state == "inactive":
                                profile.activate()
                                activated_members.append(profile.get_full_name())
                                
                    else:
                        if profile.state == "inactive":
                            profile.activate()
                            activated_members.append(profile.get_full_name())

                except ObjectDoesNotExist:
                    pass

        if "SENDGRID_API_KEY" in os.environ and len(deactivated_members) or len(activated_members):
            body = "HSBNE overdue fees check ran with {} overdue. These people have been deactivated:<br>{}<br><br>" \
                   "These people have been reactivated:<br>{}".format(len(deactivated_members), deactivated_members, activated_members)
            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = sendgrid.Email(settings.FROM_EMAIL_TREASURER)
            to_email = sendgrid.Email(settings.SYSADMIN_EMAIL)
            subject = "HSBNE overdue fees check ran with {} overdue and {} reactivated.".format(len(deactivated_members), len(activated_members))
            content = sendgrid.helpers.mail.Content("text/html", body)
            mail = sendgrid.helpers.mail.Mail(from_email, subject, to_email, content)
            sg.client.mail.send.post(request_body=mail.get())

        return HttpResponse(str(page) + "," + str(len(contacts)))

    else:
        return "Error checking overdue fees in Xero. No Xero API details."
