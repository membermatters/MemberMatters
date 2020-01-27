from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from membermatters.helpers import log_user_event
import pytz
import os
import requests
from membermatters.decorators import no_noobs, admin_required, api_auth
from xero import Xero
from xero.auth import PrivateCredentials
import datetime
from sendgrid.helpers.mail import To

import sendgrid
from multiprocessing.dummy import Pool as ThreadPool
from django.contrib.auth import get_user_model

User = get_user_model()
from profile.models import Profile
from profile.emailhelpers import send_single_email

utc = pytz.UTC
xero_rsa = os.environ.get("PORTAL_XERO_RSA_FILE", "/usr/src/data/xerkey.pem")

from constance import config


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


def webcams(request):
    return render(request, 'webcams.html')


@login_required
def issue(request):
    # Handle submission.
    if request.method == 'POST':
        print(request.POST.get("title"))
        if request.POST.get("title") and request.POST.get("description"):
            if "PORTAL_TRELLO_API_KEY" in os.environ and "PORTAL_TRELLO_API_TOKEN" in os.environ:
                issue = request.POST.get('title', '')
                details = request.POST.get('description', '')
                url = "https://api.trello.com/1/cards"
                trelloKey = os.environ.get('PORTAL_TRELLO_API_KEY')
                trelloToken = os.environ.get('PORTAL_TRELLO_API_TOKEN')

                querystring = {"name": issue, "desc": details, "pos": "top", "idList": "5529dd886d658fdace75c830",
                               "keepFromSource": "all", "key": trelloKey, "token": trelloToken}

                response = requests.request("POST", url, params=querystring)

                if response.status_code == 200:
                    log_user_event(request.user, "Submitted issue: " + issue + " Content: " + details, "generic")

                    return render(request, 'issue.html', {'message': "Submission Successful!"})
                else:
                    return render(request, 'issue.html',
                                  {'error': "Sorry but there was a server side error."})

            else:
                return render(request, 'issue.html',
                              {'error': "Sorry but there was a server side error: Trello API is not configured."})

        return render(request, 'issue.html', {'error': "Invalid form submission..."})

    # render template normally
    return render(request, 'issue.html')


@login_required
def proxy(request):
    groups = request.user.profile.groups.all()

    context = {"groups": groups}

    # Handle submission.
    if request.method == 'POST':
        params = {}
        required_aprams = ["proxy-memberaddress", "proxy-proxyname", "proxy-proxyaddress", "proxy-type",
                           "proxy-meetingdate"]

        for param in request.POST:
            params[param] = request.POST[param]

        for param in required_aprams:
            if param not in params:
                context["error"] = "Sorry, invalid form submission."

        full_name = request.user.profile.get_full_name()
        member_address = params["proxy-memberaddress"]
        proxy_name = params["proxy-proxyname"]
        proxy_address = params["proxy-proxyaddress"]
        proxy_type = params["proxy-type"]
        proxy_date = params["proxy-meetingdate"]
        submit_date = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M")

        subject = "{} submitted a proxy for {} Meeting".format(full_name, params["proxy-type"])
        message = "I, {}, of {}, being a member of the association, appoint {} of {} as my proxy to vote for me on my "\
                  "behalf at the {} Meeting of the association, to be held on the day of {} and at any adjournment of "\
                  "the meeting. ~br~ ~br~ Signed by {} on this day of {}.".format(full_name, member_address, proxy_name,
                                                                                  proxy_address, proxy_type, proxy_date,
                                                                                  full_name, submit_date)

        send_single_email(request.user, request.user.email, subject, subject, message)
        send_single_email(request.user, config.EMAIL_ADMIN, subject, subject, message)
        context["message"] = "Successfully submitted proxy. A copy has been emailed to you for your records."

    # render template normally
    return render(request, 'proxy.html', context)
