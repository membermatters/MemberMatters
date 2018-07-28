from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from memberportal.helpers import log_user_event
from .forms import SpacebugForm
import pytz
import os
import sendgrid
from sendgrid.helpers.mail import *


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
            subject = request.POST.get('issue', '')
            body = request.POST.get('details', '')
            if "SENDGRID_API_KEY" in os.environ:
                sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
                from_email = Email("portal@hsbne.org")
                to_email = Email("issues@hsbne.org")
                content = Content("text/html", body)
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                if response.status_code == 202:
                    log_user_event(request.user, "Sent issue with subject: " + subject, "email",
                                   "Email content: " + body)
                    messages.success(request, 'Issue submitted successfully. Thanks.')
                    return redirect(reverse('report_spacebug'))
        log_user_event(request.user, "Failed to send issue with subject: " + subject, "email", "Email content: " + body)
        messages.error(request, 'Issue failed to submit, sorry.')
        return redirect(reverse('report_spacebug'))

    # render template normally
    return render(request, 'spacebug.html', {
        'form': form_class,
    })


def webcams(request):
    return render(request, 'webcams.html')
