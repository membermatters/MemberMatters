from django.contrib.auth import login, update_session_auth_hash
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db.utils import IntegrityError
from django.urls import reverse
from memberportal.decorators import no_noobs, admin_required, api_auth
from memberportal.helpers import log_user_event
from .models import Profile, User, MemberTypes
from access.models import Doors, Interlock, DoorLog, InterlockLog
from spacebucks.models import SpaceBucks
from .emailhelpers import send_single_email, send_group_email
from django.conf import settings
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import pytz

utc = pytz.UTC

permission_message = "You are not authorised to do that."


@csrf_exempt
@api_auth
def create_account_api(request):
    if request.method == 'POST':
        try:
            details = json.loads(request.body)
        except:
            return JsonResponse({"success": False, "message": "Invalid json input."})

        # Create a new instance of the user model and fill it with data
        user = User()
        user.email = details["email"]
        user.save()

        # Create a new instance of the profile model and fill it with data
        profile = Profile()
        created_date = datetime.strptime(details["created"], '%Y-%m-%d %H:%M:%S')
        profile.screen_name = details["screen_name"]
        profile.first_name = details["first_name"]
        profile.last_name = details["last_name"]
        profile.phone = details["phone"]
        profile.rfid = details["rfid_code"]
        profile.created = created_date
        profile.state = details["state"]
        profile.member_type = MemberTypes.objects.get(id=4)
        profile.user = user
        profile.must_update_profile = True
        profile.save()

        # give default access
        for door in Doors.objects.filter(all_members=True):
            profile.doors.add(door)

        profile.save()

        return JsonResponse({"success": True})

    return HttpResponseBadRequest("Bad request method")


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

            profile.email_profile_to("contact@hsbne.org")

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
                "https://hsbnemembership.eventbrite.com.au",
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
            return redirect('profile')
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
            return render(request, 'reset_password_form.html', {"error": "Invalid link."})

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
                         "message": "Password changed successfully. Please use the login link in the menu."})

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
def profile(request, extra_context=None):
    """
    The profile view.
    :param request:
    :return:
    """
    return render(request, 'profile.html', context=extra_context)


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
    interlocks = Interlock.objects.all()

    return render(
        request, 'access_permissions.html',
        {"doors": doors, "interlocks": interlocks, "member_id": request.user.id})


@login_required
@admin_required
def admin_spacebucks_transactions(request, member_id):
    if not request.user.profile.can_see_members_spacebucks:
        return HttpResponseForbidden(permission_message)

    user = User.objects.get(pk=member_id)
    transactions = SpaceBucks.objects.filter(user_id=member_id)
    context = {
        "transactions": transactions,
        "balance": user.profile.spacebucks_balance,
        "member": user
    }
    rendered = render_to_string('partial_admin_member_spacebucks.html', context)

    return JsonResponse({"body": rendered})


@login_required
@admin_required
def admin_add_spacebucks(request, member_id, amount):
    if not request.user.profile.can_see_members_spacebucks:
        return HttpResponseForbidden(permission_message)

    if request.method == 'GET':
        user = User.objects.get(pk=member_id)

        # Convert from cents
        amount = round(amount / 100, 2)

        if amount > 50:
            return HttpResponseBadRequest("Invalid amount.")

        transaction = SpaceBucks()
        transaction.amount = amount
        transaction.user = user
        transaction.description = "Manually added by administrator."
        transaction.transaction_type = "bank"
        transaction.logging_info = ""
        transaction.save()
        log_user_event(request.user, "Manually added ${} to {}.".format(amount, user.profile.get_full_name()),
                       "spacebucks")
        log_user_event(user, "{} manually added ${} to {}.".format(request.user.profile.get_full_name(), amount,
                                                                   user.profile.get_full_name()), "stripe")

        return JsonResponse({"success": True})

    else:
        return HttpResponseBadRequest("Invalid request method.")


@login_required
@admin_required
def admin_edit_member(request, member_id):
    """
    Part of the process for our ajax requests for the member list.
    :param request:
    :param member_id:
    :return:
    """
    if not request.user.profile.can_see_members_personal_details:
        return HttpResponseForbidden(permission_message)
    profile = get_object_or_404(Profile, user=member_id)
    data = dict()

    profile_form = AdminEditProfileForm(instance=profile)
    user_form = AdminEditUserForm(instance=profile.user)
    form_valid = False

    if request.method == 'POST':
        # if it's a form submission pass it to the form
        profile_form = AdminEditProfileForm(request.POST, instance=profile)
        user_form = AdminEditUserForm(request.POST, instance=profile.user)

        if profile_form.is_valid() and user_form.is_valid():
            # if it's a valid form submission then save and log it
            try:
                profile_form.save()
                user_form.save()
                form_valid = True
                log_user_event(profile.user, request.user.profile.get_full_name() + " edited user profile.", "profile")

            except IntegrityError:
                form_valid = False

    # render the form and return it
    data["form_is_valid"] = form_valid
    data['html_form'] = render_to_string(
        'partial_admin_edit_member.html',
        {'profile_form': profile_form, 'user_form': user_form,
         'member_id': member_id, "profile": profile}, request=request)
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
    if not request.user.profile.can_see_members_logs:
        return HttpResponseForbidden(permission_message)

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
        profile_form = EditProfileForm(
            request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            # if it was a form submission save it
            user_form.save()
            profile_form.save()
            if request.user.profile.must_update_profile:
                request.user.profile.must_update_profile = False
                request.user.profile.save()
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
def digital_id(request):
    """
    The digital ID view.
    :param request:
    :return:
    """

    return render(request, 'digital_id.html')


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
    if not request.user.profile.can_disable_members:
        return JsonResponse({"message": permission_message})

    user = User.objects.get(id=member_id)

    if state == 'active':
        if user.profile.state == "noob":
            # give default door access
            for door in Doors.objects.filter(all_members=True):
                user.profile.doors.add(door)

            # give default interlock access
            for interlock in Interlock.objects.filter(all_members=True):
                user.profile.interlocks.add(interlock)

            email = user.email_welcome()
            xero = user.profile.add_to_xero()
            invoice = user.profile.create_membership_invoice()
            user.profile.state = "inactive"  # an admin should activate them when they pay their invoice
            user.profile.save()

            if "Error" not in xero and "Error" not in invoice and email:
                return JsonResponse({"success": True, "message": "Successfully added to Xero and sent welcome email."})

            elif "Error" in xero:
                return JsonResponse({"success": False, "message": xero})

            elif "Error" in invoice:
                return JsonResponse({"success": False, "message": invoice})

            elif email is False:
                return JsonResponse({"success": False, "message": "Error, couldn't send welcome email."})

            else:
                return JsonResponse({"success": False, "message": "Unknown error while making into member."})

        else:
            user.profile.activate()
            return JsonResponse({"success": True, "message": "Successfully enabled user. ✅"})

    else:
        user.profile.deactivate()
        return JsonResponse(
            {"success": True, "message": "Successfully disabled user. ⛔"})


@login_required
@admin_required
def admin_edit_access(request, member_id):
    if not request.user.profile.can_manage_access:
        return HttpResponseForbidden(permission_message)

    member = get_object_or_404(User, pk=member_id)
    doors = Doors.objects.all()
    interlocks = Interlock.objects.all()
    data = dict()

    # render the form and return it
    data['html_form'] = render_to_string(
        'partial_admin_edit_access.html',
        {'member': member, 'member_id': member_id, 'doors': doors,
         'interlocks': interlocks}, request=request)
    return JsonResponse(data)


@login_required
@no_noobs
def recent_swipes(request):
    doors = DoorLog.objects.all().order_by('date')[::-1][:50]
    interlocks = InterlockLog.objects.all().order_by(
        'last_heartbeat')[::-1][:50]

    return render(
        request, 'recent_swipes.html',
        {"doors": doors, "interlocks": interlocks})


@login_required
@no_noobs
def last_seen(request):
    last_seens = list()
    members = User.objects.all()

    for member in members:
        if member.profile.last_seen is not None:
            last_seens.append(
                {"user": member, "never": False,
                 "date": member.profile.last_seen})

        else:
            last_seens.append({"user": member, "never": True})

    return render(request, 'last_seen.html', {"last_seens": last_seens})


@login_required
@no_noobs
def edit_theme_song(request):
    if request.method == 'POST':
        theme_form = ThemeForm(request.POST, request.FILES,
                               instance=request.user.profile)

        if theme_form.is_valid():
            # todo: pass the uploaded file (or removal request) to asterisk
            # handle_uploaded_file(request.FILES['theme'])
            theme_form.save()
            log_user_event(request.user, "User theme updated.", "profile")
            return HttpResponseRedirect('%s' % (reverse('edit_theme_song')))

    else:
        # if it's not a form submission, return an empty form
        theme_form = ThemeForm(instance=request.user.profile)

    return render(
        request, 'edit_theme_song.html',
        {"theme_form": theme_form}, )


@login_required
@admin_required
def resend_welcome_email(request, member_id):
    success = User.objects.get(pk=member_id).email_welcome()
    log_user_event(request.user, "Resent welcome email.", "profile")

    if success:
        return JsonResponse({"message": success})

    else:
        return JsonResponse(
            {"message": "Couldn't email member, unknown error."})


@login_required
@admin_required
def sync_xero_accounts(request):
    from .xerohelpers import sync_xero_accounts
    success = sync_xero_accounts(User.objects.all().prefetch_related())
    log_user_event(request.user, "Resynced xero accounts.", "profile")

    if success:
        return JsonResponse({"message": success})

    else:
        return JsonResponse(
            {"message": "Couldn't sync xero accounts, unknown error."})


@login_required
@admin_required
def add_to_xero(request, member_id):
    return JsonResponse({"message": User.objects.get(pk=member_id).profile.add_to_xero()})


@login_required
def create_invoice(request, member_id, option=False):
    email_invoice = False

    if "email" == option:
        email_invoice = True

    if request.user.profile.can_generate_invoice:
        response = User.objects.get(pk=member_id).profile.create_membership_invoice(email_invoice=email_invoice)

        return JsonResponse({"message": response})

    else:
        return JsonResponse({"message": permission_message})


@login_required
def starving_hacker_form(request):
    if request.method == 'POST':
        starving_form = StarvingHackerForm(request.POST, instance=request.user.profile)

        if starving_form.is_valid():
            # if it was a form submission save it
            profile = starving_form.save()
            profile.updated_starving_details = datetime.now()
            profile.save()

            log_user_event(request.user, "User edited starving hacker details.", "profile")

            message = None
            error = None

            if profile.is_starving_eligible():
                message = "Your application for the starving hacker discount was " \
                          "successful. Your next invoice " \
                          "should reflect the discount. If it doesn't, email our treasurer at treasurer@hsbne.org."
                email = send_single_email(request.user,
                                          settings.EXEC_EMAIL,
                                          "New Starving Hacker Approved",
                                          "New Starving Hacker Approved",
                                          "Hi there, a new starving hacker application has been approved for {}. Please " \
                                          "update their membership level in the portal and change their repeating invoice in " \
                                          "Xero to reflect the discount.".format(profile.get_full_name()))

            else:
                if profile.special_consideration:
                    error = " Unfortunately, you aren't eligible for the discount based on the information you " \
                            "provided. As you requested special consideration, the executive will review your " \
                            "application and get back to you within a few days with the outcome."
                    email = send_single_email(request.user,
                                              settings.EXEC_EMAIL,
                                              "New Special Consideration Application for Starving Hacker",
                                              "New Special Consideration Application for Starving Hacker",
                                              "Hi there, a new starving hacker application has been rejected for {}. However," \
                                              "they have requested special consideration. Login to the portal if you'd like " \
                                              "to check their application details. ~br~~br~ Special Consideration Reason: {}".format(
                                                  request.user.profile.get_full_name(),
                                                  profile.special_consideration_note))

                else:
                    error = " Unfortunately, you aren't eligible for the discount based on the information you " \
                            "provided. Your attempt has been logged and any additional applications may require proof" \
                            " of your circumstances."
                    email = send_single_email(request.user,
                                              settings.EXEC_EMAIL,
                                              "New Starving Hacker Rejected",
                                              "New Starving Hacker Rejected",
                                              "Hi there, a new starving hacker application has been rejected for {}. Login to the" \
                                              " portal if you'd like to check their application details.".format(
                                                  request.user.profile.get_full_name()))

            if not email:
                return render(request, 'starving_hacker_form.html',
                              {"message": message, "error": "Unable to send email to the executive.",
                               "form": starving_form})

            return render(request, 'starving_hacker_form.html',
                          {"message": message, "error": error, "form": starving_form})

        return render(request, 'starving_hacker_form.html', {"error": "Error validating form.", "form": starving_form})

    else:
        # if it's not a form submission, return an empty form
        starving_form = StarvingHackerForm(instance=request.user.profile)

    return render(request, 'starving_hacker_form.html', {"form": starving_form})
