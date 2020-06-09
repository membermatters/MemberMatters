from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.html import escape
from django.urls import reverse
from membermatters.helpers import log_user_event
from .forms import CauseForm
from .models import Group
from membermatters.decorators import staff_required, no_noobs
from profile.emailhelpers import send_group_email
from constance import config
import pytz

utc = pytz.UTC


@login_required
@staff_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if (
        not request.user.profile.can_manage_groups
        or group not in request.user.profile.can_manage_group.all()
    ):
        return HttpResponseForbidden("You do not have permission to access that.")

    group.delete()
    log_user_event(request.user, "Deleted {} group.".format(group.name), "admin")

    return HttpResponseRedirect(reverse("manage_groups"))
