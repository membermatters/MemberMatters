from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.html import escape
from django.urls import reverse
from memberportal.helpers import log_user_event
from .forms import CauseForm, CauseFundForm
from .models import Causes, CauseFund
from memberportal.decorators import admin_required, no_noobs
from profile.emailhelpers import send_group_email
import pytz

utc = pytz.UTC


@login_required
@admin_required
def manage_causes(request):
    if not request.user.profile.can_manage_causes:
        return HttpResponseForbidden("You do not have permission to access that.")

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

    return render(request, 'manage_causes.html', {"form": form, "causes": causes})


@login_required
@no_noobs
def list_causes(request):
    causes = Causes.objects.all()

    return render(
        request,
        'list_causes.html', {"causes": causes, })


@login_required
@admin_required
def email_cause_members(request, cause_id):
    cause = get_object_or_404(Causes, pk=cause_id)

    if not request.user.profile.can_manage_causes or cause not in request.user.profile.can_manage_cause.all():
        return HttpResponseForbidden("You do not have permission to access that.")

    if request.method == 'POST':
        # check all our params exist
        for x in ("email_content", "subject", "cause"):
            if x not in request.POST:
                return HttpResponseBadRequest("Invalid Request.")

        # get the cause, email message and subject
        message = request.POST.get("email_content", "no message")
        title = request.POST.get("subject", "no subject")

        # handle no message/subject specified
        if not len(title):
            return render(request, 'email_cause_members.html', {"cause": cause, "error": "No subject specified."})

        if not len(message):
            return render(request, 'email_cause_members.html', {"cause": cause, "error": "No message specified."})

        subject = escape("HSBNE {} - {}".format(cause.name, title))  # format our subject

        # make the list of our recipients
        emails = list()
        for member in cause.get_active_set():
            emails.append(member.user.email)

        if request.user.email not in emails:
            emails.append(request.user.email)

        response = send_group_email(request.user, emails, subject, title, message)
        return render(request, 'email_cause_members.html', {"cause": cause, "success": response})

    else:
        cause = Causes.objects.get(pk=cause_id)
        return render(request, 'email_cause_members.html', {"cause": cause})


@login_required
@admin_required
def edit_cause(request, cause_id):
    """
    The edit cause (admin) view.
    :param request:
    :param cause_id: cause id to edit
    :return:
    """
    cause = get_object_or_404(Causes, pk=cause_id)

    if not request.user.profile.can_manage_causes or cause not in request.user.profile.can_manage_cause.all():
        return HttpResponseForbidden("You do not have permission to access that.")

    if request.method == 'POST':
        form = CauseForm(request.POST, instance=cause)
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            log_user_event(
                request.user,
                "Edited {} cause.".format(cause.name),
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
    cause = get_object_or_404(Causes, pk=cause_id)

    if not request.user.profile.can_manage_causes or cause not in request.user.profile.can_manage_cause.all():
        return HttpResponseForbidden("You do not have permission to access that.")

    cause.delete()
    log_user_event(request.user, "Deleted {} cause.".format(cause.name), "admin")

    return HttpResponseRedirect(reverse("manage_causes"))


@login_required
@admin_required
def manage_cause_funds(request, cause_id):
    cause = get_object_or_404(Causes, pk=cause_id)

    if not request.user.profile.can_manage_causes or cause not in request.user.profile.can_manage_cause.all():
        return HttpResponseForbidden("You do not have permission to access that.")

    # if we want to add a cause
    if request.method == 'POST':
        form = CauseFundForm(request.POST)
        if form.is_valid():
            fund = form.save(commit=False)
            fund.cause = cause
            fund.save()
            log_user_event(
                request.user,
                "Created {} cause.".format(form.cleaned_data.get('name')),
                "admin", form)
            return HttpResponseRedirect(
                reverse("manage_cause_funds", kwargs={'cause_id': cause.pk, }))

    else:
        form = CauseFundForm()

    funds = CauseFund.objects.filter(cause=cause)

    return render(
        request, 'manage_cause_funds.html',
        {"form": form, "cause": cause, "funds": funds})


@login_required
@no_noobs
def list_cause_funds(request):
    if not request.user.profile.can_manage_causes:
        return HttpResponseForbidden("You do not have permission to access that.")

    causes = Causes.objects.all()

    return render(
        request,
        'list_causes.html', {"causes": causes, })


@login_required
@admin_required
def edit_cause_fund(request, fund_id):
    """
    The edit cause (admin) view.
    :param request:
    :param cause_id: cause id to edit
    :return:
    """
    if not request.user.profile.can_manage_causes:
        return HttpResponseForbidden("You do not have permission to access that.")

    fund = get_object_or_404(CauseFund, pk=fund_id)
    if request.method == 'POST':
        form = CauseFundForm(request.POST, instance=fund)
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            log_user_event(
                request.user,
                "Edited {} cause fund".format(fund.name),
                "admin", form)
            return HttpResponseRedirect(
                reverse('manage_cause_funds',
                        kwargs={'cause_id': fund.cause.pk, }))
        else:
            # otherwise return form with errors
            return render(request, 'edit_cause_fund.html', {'form': form})

    else:
        # if it's not a form submission, return an empty form
        form = CauseFundForm(instance=CauseFund.objects.get(pk=fund_id))
        return render(request, 'edit_cause_fund.html', {'form': form})


@login_required
@admin_required
def delete_cause_fund(request, fund_id):
    if not request.user.profile.can_manage_causes:
        return HttpResponseForbidden("You do not have permission to access that.")

    fund = get_object_or_404(CauseFund, pk=fund_id)
    fund.delete()
    log_user_event(
        request.user, "Deleted {} cause fund.".format(fund.name), "admin")

    return HttpResponse("Success")
