from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from memberportal.helpers import log_user_event
from .forms import SpacebugForm
import pytz

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

    return render(request, 'spacebug.html', {
        'form': form_class,
    })


def webcams(request):
    return render(request, 'webcams.html')
