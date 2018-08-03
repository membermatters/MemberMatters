from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from memberportal.helpers import log_user_event
from .forms import SpacebugForm
import pytz
import os
import requests


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
            issue = request.POST.get('issue', '')
            details = request.POST.get('details', '')
            url = "https://api.trello.com/1/cards"
            trelloKey = os.environ.get('TRELLO_API_KEY')
            trelloToken = os.environ.get('TRELLO_API_TOKEN')

            querystring = {"name":issue,"desc":details,"pos":"top","idList":"5529dd886d658fdace75c830","keepFromSource":"all","key":trelloKey,"token":trelloToken}

            response = requests.request("POST", url, params=querystring)

                
            if response.status_code == 200:
                log_user_event(request.user, "Submitted issue: " + issue + " Content: " + details, "generic")
                messages.success(request, 'Issue submitted successfully. Thanks.')
                return redirect(reverse('report_spacebug'))
        log_user_event(request.user, "Issue Submit Failed:: " + issue + " content: " + details, "error")
        messages.error(request, 'Issue failed to submit, sorry.')
        return redirect(reverse('report_spacebug'))

    # render template normally
    return render(request, 'spacebug.html', {
        'form': form_class,
    })


def webcams(request):
    return render(request, 'webcams.html')
