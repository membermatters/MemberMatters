from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.html import escape
from django.urls import reverse
from membermatters.helpers import log_user_event
from .forms import CauseForm, CauseFundForm
from .models import Group, CauseFund
from membermatters.decorators import admin_required, no_noobs
from profile.emailhelpers import send_group_email
from constance import config
import pytz

utc = pytz.UTC


@login_required
@admin_required
def manage_groups(request):
    if not request.user.profile.can_manage_groups:
        return HttpResponseForbidden("You do not have permission to access that.")

    # if we want to add a group
    if request.method == 'POST':
        form = CauseForm(request.POST)
        if form.is_valid():
            form.save()
            log_user_event(
                request.user,
                f"Created {form.cleaned_data.get('name')} {config.GROUP_NAME}.",
                "admin", form)
            return HttpResponseRedirect(reverse("manage_groups"))

    else:
        form = CauseForm()

    groups = Group.objects.all()

    return render(request, 'manage_groups.html', {"form": form, "groups": groups})


@login_required
@no_noobs
def list_groups(request):
    groups = Group.objects.all()

    return render(
        request,
        'list_groups.html', {"groups": groups, })


@login_required
@admin_required
def email_group_members(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if not request.user.profile.can_manage_groups or group not in request.user.profile.can_manage_group.all():
        return HttpResponseForbidden("You do not have permission to access that.")

    if request.method == 'POST':
        # check all our params exist
        for x in ("email_content", "subject", "group"):
            if x not in request.POST:
                return HttpResponseBadRequest("Invalid Request.")

        # get the group, email message and subject
        message = request.POST.get("email_content", "no message")
        title = request.POST.get("subject", "no subject")

        # handle no message/subject specified
        if not len(title):
            return render(request, 'email_group_members.html', {"group": group, "error": "No subject specified."})

        if not len(message):
            return render(request, 'email_group_members.html', {"group": group, "error": "No message specified."})

        subject = escape(f"{config.SITE_OWNER} {group.name} - {title}")  # format our subject

        # make the list of our recipients
        emails = list()
        for member in group.get_active_set():
            emails.append(member.user.email)

        if request.user.email not in emails:
            emails.append(request.user.email)

        response = send_group_email(request.user, emails, subject, title, message)
        return render(request, 'email_group_members.html', {"group": group, "success": response})

    else:
        group = Group.objects.get(pk=group_id)
        return render(request, 'email_group_members.html', {"group": group})


@login_required
@admin_required
def edit_group(request, group_id):
    """
    The edit group (admin) view.
    :param request:
    :param group_id: group id to edit
    :return:
    """
    group = get_object_or_404(Group, pk=group_id)

    if not request.user.profile.can_manage_groups or group not in request.user.profile.can_manage_group.all():
        return HttpResponseForbidden("You do not have permission to access that.")

    if request.method == 'POST':
        form = CauseForm(request.POST, instance=group)
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            log_user_event(
                request.user,
                f"Edited {group.name} {config.GROUP_NAME}.",
                "admin", form)
            return HttpResponseRedirect('%s' % (reverse('manage_groups')))
        else:
            # otherwise return form with errors
            return render(request, 'edit_group.html', {'form': form})

    else:
        # if it's not a form submission, return an empty form
        form = CauseForm(instance=Group.objects.get(pk=group_id))
        return render(request, 'edit_group.html', {'form': form})


@login_required
@admin_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if not request.user.profile.can_manage_groups or group not in request.user.profile.can_manage_group.all():
        return HttpResponseForbidden("You do not have permission to access that.")

    group.delete()
    log_user_event(request.user, "Deleted {} group.".format(group.name), "admin")

    return HttpResponseRedirect(reverse("manage_groups"))
