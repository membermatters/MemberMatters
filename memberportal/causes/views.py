from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from memberportal.helpers import log_user_event
from .forms import CauseForm
from .models import Causes
from memberportal.decorators import admin_required, no_noobs
from profile.models import Profile
import pytz

utc = pytz.UTC


@login_required
@admin_required
def manage_causes(request):
    # if we want to add a cause
    if request.method == 'POST':
        form = CauseForm(request.POST)
        if form.is_valid():
            form.save()
            log_user_event(
                request.user,
                "Created {} cause.".format(form.cleaned_data.get('name')),
                "admin", form)
            return HttpResponseRedirect(reverse("manage_causes"))

    else:
        form = CauseForm()

    causes = Causes.objects.all()

    return render(
        request, 'manage_causes.html', {"form": form, "causes": causes})


@login_required
@no_noobs
def list_causes(request):
    causes = Causes.objects.all()
    members = Profile.objects.all()

    return render(
        request,
        'list_causes.html', {"causes": causes, "members": members})


@login_required
@admin_required
def edit_cause(request, cause_id):
    """
    The edit cause (admin) view.
    :param request:
    :param cause_id: cause id to edit
    :return:
    """
    if request.method == 'POST':
        form = CauseForm(
            request.POST, instance=Causes.objects.get(pk=cause_id))
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            log_user_event(
                request.user,
                "Edited {} cause.".format(
                    Causes.objects.get(pk=cause_id).name),
                "admin", form)
            return HttpResponseRedirect('%s' % (reverse('manage_causes')))
        else:
            # otherwise return form with errors
            return render(request, 'edit_cause.html', {'form': form})

    else:
        # if it's not a form submission, return an empty form
        form = CauseForm(instance=Causes.objects.get(pk=cause_id))
        return render(request, 'edit_cause.html', {'form': form})


@login_required
@admin_required
def delete_cause(request, cause_id):
    cause = Causes.objects.get(pk=cause_id)
    cause.delete()
    log_user_event(
        request.user, "Deleted {} cause.".format(cause.name), "admin")

    return HttpResponse("Success")
