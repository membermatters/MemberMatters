from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from memberportal.decorators import no_noobs, admin_required
from memberportal.helpers import log_user_event
from access.models import Doors, DoorLog
from .forms import *
from datetime import datetime
import pytz

utc = pytz.UTC


def signup(request):
    """
    The signup view.
    :param request:
    :return:
    """

    # if the user has submitted a form process it
    if request.method == 'POST':
        # make a new instance of both forms
        user_form = SignUpForm(request.POST)
        profile_form = AddProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # if both forms are valid save them
            new_user = user_form.save()
            profile = profile_form.save(commit=False)

            # this check is needed to make sure the profile has the user id
            if profile.user_id is None:
                profile.user_id = new_user.id
            profile.save()
            profile_form.save_m2m()
            new_user.email_link(
                "HSBNE New Member Signup - Action Required",
                "Next Step: Register for an Induction",
                "Important. Please read this email for details on how to "
                "register for an induction.",
                "Hi {}, thanks for signing up! The next step to becoming a fully "
                "fledged member is to book in for an induction. During this "
                "induction we will go over the basic safety and operational "
                "aspects of HSBNE. To book in, click the link below.".format(
                    profile.first_name),
                "https://www.eventbrite.com.au/e/hsbne-open-night-tickets-27140078706",
                "Register for Induction")

            # for convenience, we should now log the user in
            login(request, new_user)

            return redirect('/')

    else:
        # make a new instance for both forms and render the template
        user_form = SignUpForm()
        profile_form = AddProfileForm()

    return render(request, 'signup.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log_user_event(request.user, "User password changed.", "profile")
            return render(
                request, 'change_password.html',
                {'form': form, "message": "Password changed successfully."})

        else:
            return render(request, 'change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


def reset_password(request, reset_token=None):
    if reset_token:
        try:
            user = User.objects.get(password_reset_key=reset_token)

        except ObjectDoesNotExist:
            return render(request, 'reset_password_form.html',
                          {"error": "Invalid link."})

        if request.method == "POST":
            form = ResetPasswordForm(request.POST)

            if form.is_valid():
                if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                    user.password = make_password(form.cleaned_data['password1'])
                    user.password_reset_expire = None
                    user.password_reset_key = None
                    user.save()

                    user.email_notification(
                        "Your HSBNE password has changed.",
                        "Your password has changed.", "",
                        "Your HSBNE password has been successfully changed.")

                    return render(
                        request, 'reset_password_form.html',
                        {'form': ResetPasswordForm(),
                         "message": "Password changed successfully."})

                else:
                    return render(
                        request, 'reset_password_form.html',
                        {'form': ResetPasswordForm(),
                         "error": "Passwords don't match."})

        else:
            if utc.localize(datetime.now()) < user.password_reset_expire:
                return render(request, 'reset_password_form.html',
                              {'form': ResetPasswordForm()})

            else:
                return render(request, 'reset_password_form.html',
                              {'form': ResetPasswordForm(),
                               "error": "Error. Link expired."})

    elif request.method == "POST":
        form = ResetPasswordRequestForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                user.reset_password()
                return render(
                    request, 'reset_password.html',
                    {'form': ResetPasswordRequestForm(),
                     "message": "Check your email for a link."})

            except ObjectDoesNotExist:
                return render(
                    request, 'reset_password.html',
                    {'form': ResetPasswordRequestForm(),
                     "error": "No user with that email."})

        else:
            return render(
                request, 'reset_password.html',
                {'form': ResetPasswordRequestForm(),
                 "error": "invalid email"})

    else:

        return render(
            request, 'reset_password.html',
            {'form': ResetPasswordRequestForm()})


@login_required
def profile(request):
    """
    The profile view.
    :param request:
    :return:
    """
    return render(request, 'profile.html')


@login_required
@admin_required
def member_list(request):
    """
    The list all members view. Used to manage all members.
    :param request:
    :return:
    """
    # extract the values we need for each member
    # probably will need to add some server side pagination...
    members = User.objects.all()

    return render(request, 'memberlist.html', {'members': members})


@login_required
@no_noobs
def access_permissions(request):
    doors = Doors.objects.all()

    return render(
        request, 'access_permissions.html',
        {"doors": doors, "member_id": request.user.id})


@login_required
@admin_required
def admin_edit_member(request, member_id):
    """
    Part of the process for our ajax requests for the member list.
    :param request:
    :param member_id:
    :return:
    """
    profile = get_object_or_404(Profile, user=member_id)
    data = dict()

    form = AdminEditProfileForm(instance=profile)
    # if it's not valid don't save or log it
    data['form_is_valid'] = False

    if request.method == 'POST':
        # if it's a form submission pass it to the form
        form = AdminEditProfileForm(request.POST, instance=profile)

        if form.is_valid():
            # if it's a valid form submission then save and log it
            form.save()
            data['form_is_valid'] = True
            log_user_event(
                profile.user, request.user.get_full_name() + " edited user profile.",
                "profile")

    # render the form and return it
    data['html_form'] = render_to_string(
        'partial_admin_edit_member.html',
        {'form': form, 'member_id': member_id},
        request=request)
    return JsonResponse(data)


@login_required
@admin_required
def admin_member_logs(request, member_id):
    """
    Part of the process for our ajax requests for the member list.
    :param request:
    :param member_id:
    :return:
    """
    data = dict()
    member = User.objects.get(pk=member_id)

    # render the form and return it
    data['html_form'] = render_to_string(
        'partial_admin_member_logs.html', {'logs': member.profile.get_logs()},
        request=request)
    return JsonResponse(data)


@login_required
def edit_profile(request):
    """
    The edit user profile view.
    :param request:
    :return:
    """

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            # if it was a form submission save it
            user_form.save()
            profile_form.save()
            log_user_event(request.user, "User profile edited.", "profile")
            return HttpResponseRedirect('%s' % (reverse('profile')))

    else:
        # if it's not a form submission, return an empty form
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    return render(
        request, 'edit_profile.html',
        {'user_form': user_form, "profile_form": profile_form})


@login_required
@admin_required
def set_state(request, member_id, state):
    """
    Sets the active/inactive (access disabled/enabled) state for members.
    :param request:
    :param member_id:
    :param state:
    :return:
    """
    user = User.objects.get(id=member_id)

    if state == 'active':
        if user.profile.state == "noob":
            # give default access
            for door in Doors.objects.filter(all_members=True):
                user.profile.doors.add(door)

        user.profile.activate()

    else:
        user.profile.deactivate()

    return JsonResponse({"success": True})


@login_required
@admin_required
def admin_edit_access(request, member_id):
    member = get_object_or_404(User, pk=member_id)
    doors = Doors.objects.all()
    data = dict()

    # render the form and return it
    data['html_form'] = render_to_string(
        'partial_admin_edit_access.html',
        {'member': member, 'member_id': member_id,
         'doors': doors}, request=request)
    return JsonResponse(data)


@login_required
@no_noobs
def recent_swipes(request):
    swipes = DoorLog.objects.all().order_by('date')[::-1][:50]

    return render(request, 'recent_swipes.html', {"swipes": swipes})


@login_required
@no_noobs
def last_seen(request):
    last_seens = list()
    members = User.objects.all()

    for member in members:
        door_logs = DoorLog.objects.filter(user=member).order_by("date")
        if len(door_logs):
            date = door_logs[::-1][0].date
            last_seens.append({"user": member, "never": False, "date": date})
        else:
            last_seens.append({"user": member, "never": True})

    return render(request, 'last_seen.html', {"last_seens": last_seens})


@login_required
@no_noobs
def edit_theme_song(request):
    return render(request, 'edit_theme_song.html')


@login_required
@admin_required
def resend_welcome_email(request, member_id):
    success = User.objects.get(pk=member_id).email_welcome()
    log_user_event(request.user, "Resent welcome email.", "profile")

    if success:
        return JsonResponse({"success": True})

    else:
        return JsonResponse(
            {"success": False, "reason": "Unknown error. Error AlfSo"})
