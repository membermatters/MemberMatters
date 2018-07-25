from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest, HttpResponse, \
    HttpResponseServerError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import *
from .models import log_event, log_user_event
import stripe


def admin_required(view):
    def wrap(request, *args, **kwargs):
        # do some logic here
        if request.user.is_staff:
            return view(request, *args, **kwargs)
        else:
            # if the user isn't authorised let them know
            return HttpResponseForbidden("403 Access Forbidden")

    return wrap


def no_noobs(view):
    def wrap(request, *args, **kwargs):
        # do some logic here
        if request.user.profile.state == "noob":
            # if the user isn't authorised let them know
            return HttpResponseForbidden("403 Access Forbidden")
        else:
            return view(request, *args, **kwargs)

    return wrap


def reader_auth(view):
    def wrap(request, *args, **kwargs):
        # do some logic here
        if request.method == "GET" and request.GET.get('secret', "wrong") == "cookiemonster":
            return view(request, *args, **kwargs)
        else:
            # if the user isn't authorised let them know
            return HttpResponseForbidden("403 Access Forbidden")

    return wrap


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
            profile.email_link("HSBNE New Member Signup - Action Required",
                               "Next Step: Register for an Induction",
                               "Important. Please read this email for details on how to register for an induction.",
                               "{}, thanks for signing up! The next step to becoming a fully fledged member is to book "
                               "in for an induction. During this induction we will go over the basic safety and "
                               "operational aspects of HSBNE. To book in, click the link below.".format(
                                   new_user.first_name),
                               "https://www.eventbrite.com.au/e/hsbne-open-night-tickets-27140078706",
                               "Register for Induction")

            # for convenience, we should now log the user in
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/')

    else:
        # make a new instance for both forms and render the template
        user_form = SignUpForm()
        profile_form = AddProfileForm()

    return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def signin(request):
    """
    The sign in view.
    :param request:
    :return:
    """
    log_user_event(request.user, "User logged in.", "usage")
    return render(request, 'registration/login.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log_user_event(request.user, "User password changed.", "profile")
            return render(request, 'change_password.html', {'form': form, "message": "Password changed successfully."})

        else:
            return render(request, 'change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


def loggedout(request):
    """
    The view to show the logged out page.
    :param request:
    :return:
    """
    log_user_event(request.user, "User signed out.", "usage")
    return render(request, 'loggedout.html')


def home(request):
    """
    The home page view.
    :param request:
    :return:
    """
    return render(request, 'home.html')


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
@admin_required
def admin_edit_member(request, member_id):
    """
    Part of the process for our ajax requests for the member list.
    :param request:
    :param member_id:
    :return:
    """
    user = get_object_or_404(Profile, user=member_id)
    data = dict()

    form = AdminEditProfileForm(instance=user)
    # if it's not valid don't save or log it
    data['form_is_valid'] = False

    if request.method == 'POST':
        # if it's a form submission pass it to the form
        form = AdminEditProfileForm(request.POST, instance=user)

        if form.is_valid():
            # if it's a valid form submission then save and log it
            form.save()
            data['form_is_valid'] = True
            log_user_event(user, request.user.get_full_name() + " edited user profile.", "profile")

    # render the form and return it
    data['html_form'] = render_to_string('partial_admin_edit_member.html', {'form': form, 'member_id': member_id},
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
    data['html_form'] = render_to_string('partial_admin_member_logs.html', {'logs': member.profile.get_logs()},
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
        cause_form = EditCausesForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and cause_form.is_valid():
            # if it was a form submission save it
            user_form.save()
            cause_form.save()
            log_user_event(request.user, "User profile edited.", "profile")
            return HttpResponseRedirect('%s' % (reverse('profile')))

    else:
        # if it's not a form submission, return an empty form
        user_form = EditUserForm(instance=request.user)
        cause_form = EditCausesForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, "cause_form": cause_form})


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
def manage_causes(request):
    # if we want to add a cause
    if request.method == 'POST':
        form = CauseForm(request.POST)
        if form.is_valid():
            form.save()
            log_user_event(request.user, "Created {} cause.".format(form.cleaned_data.get('name')), "admin", form)
            return HttpResponseRedirect(reverse("manage_causes"))

    else:
        form = CauseForm()

    causes = Causes.objects.all()

    return render(request, 'manage_causes.html', {"form": form, "causes": causes})


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
        form = CauseForm(request.POST, instance=Causes.objects.get(pk=cause_id))
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            log_user_event(request.user, "Edited {} cause.".format(Causes.objects.get(pk=cause_id).name), "admin", form)
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
    log_user_event(request.user, "Deleted {} cause.".format(cause.name), "admin")

    return HttpResponse("Success")


@login_required
@no_noobs
def access_permissions(request):
    doors = Doors.objects.all()

    return render(request, 'access_permissions.html', {"doors": doors, "member_id": request.user.id})


@login_required
@admin_required
def manage_doors(request):
    doors = Doors.objects.all()
    return render(request, 'manage_doors.html', {"doors": doors})


@login_required
@admin_required
def add_door(request):
    if request.method == 'POST':
        form = DoorForm(request.POST)
        if form.is_valid():
            form.save()
            log_user_event(request.user, "Created {} door.".format(form.cleaned_data['name']), "admin", form)
            return HttpResponseRedirect(reverse("manage_doors"))

    else:
        form = DoorForm()

    return render(request, 'add_door.html', {"form": form})


@login_required
@admin_required
def edit_door(request, door_id):
    if request.method == 'POST':
        form = DoorForm(request.POST, instance=Doors.objects.get(pk=door_id))
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            log_user_event(request.user, "Edited {} door.".format(Doors.objects.get(pk=door_id).name), "admin", form)
            return HttpResponseRedirect('%s' % (reverse('manage_doors')))
        else:
            # otherwise return form with errors
            return render(request, 'edit_cause.html', {'form': form})

    else:
        # if it's not a form submission, return an empty form
        form = DoorForm(instance=Doors.objects.get(pk=door_id))
        return render(request, 'edit_door.html', {'form': form})


@login_required
@admin_required
def delete_door(request, door_id):
    door = Doors.objects.get(pk=door_id)
    log_user_event(request.user, "Deleted {} door.".format(door.name), "admin")
    door.delete()
    return HttpResponseRedirect('%s' % (reverse('manage_doors')))


@login_required
@admin_required
def admin_edit_access(request, member_id):
    member = get_object_or_404(User, pk=member_id)
    doors = Doors.objects.all()
    data = dict()

    # render the form and return it
    data['html_form'] = render_to_string('partial_admin_edit_access.html',
                                         {'member': member, 'member_id': member_id, 'doors': doors}, request=request)
    return JsonResponse(data)


@login_required
@no_noobs
def edit_theme_song(request):
    return render(request, 'edit_theme_song.html')


@login_required
@admin_required
def admin_grant_door(request, door_id, member_id):
    try:
        user = User.objects.get(pk=member_id)
        door = Doors.objects.get(pk=door_id)
        user.profile.doors.add(door)
        user.profile.save()
        log_user_event(user, "Access to {} granted.".format(door.name), "profile")
        log_user_event(request.user, "Access to {} granted for {}.".format(door.name, user.get_full_name()), "admin")

        return JsonResponse({"success": True})

    except Exception:
        return JsonResponse({"success": False, "reason": "Bad Request. Error AhSv"})


@login_required
@admin_required
def admin_revoke_door(request, door_id, member_id):
    try:
        user = User.objects.get(pk=member_id)
        door = Doors.objects.get(pk=door_id)
        user.profile.doors.remove(door)
        user.profile.save()
        log_user_event(user, "Access to {} revoked.".format(door.name), "profile")
        log_user_event(request.user, "Access to {} revoked for {}.".format(door.name, user.get_full_name()), "admin")

        return JsonResponse({"success": True})

    except ObjectDoesNotExist:
        return JsonResponse({"success": False, "reason": "No access permission was found."})


@login_required
@no_noobs
def request_access(request, door_id):
    return JsonResponse({"success": False, "reason": "Not implemented yet."})


@reader_auth
def check_access(request, rfid_code, door_id=None):
    door = None

    try:
        user = Profile.objects.get(rfid=rfid_code).user

    except ObjectDoesNotExist:
        # send back some random error code you can search for here - this means the RFID tag doesn't exist.
        log_event("Tried to check access for non existant user (or rfid not set).", "error", request)
        return HttpResponseBadRequest("Bad Request. Error AhDA")

    if user.profile.state == "active":
        if door_id is not None:
            try:
                door = Doors.objects.get(pk=door_id)
                door.checkin()

            except ObjectDoesNotExist:
                # send back some random error code you can search for here - this means the door ID doesn't exist.
                log_event("Tried to check access for non existant door.", "error", request)
                return HttpResponseBadRequest("Bad Request. Error AJld")

        else:
            try:
                door_ip = request.META.get('REMOTE_ADDR')
                door = Doors.objects.get(ip_address=door_ip)
                door.checkin()

            except ObjectDoesNotExist:
                # send back some random error code you can search for here - this means the door doesn't exist.
                log_event("Tried to check access for door {} but none found.".format(door_ip), "error", request)
                return HttpResponseBadRequest("Bad Request. Error AJlc")

        allowed_doors = user.profile.doors.all()

        if allowed_doors:
            if door in allowed_doors:
                # user has access
                door.log_access(user.id)
                return JsonResponse({"access": True, "name": user.first_name, "door": door.name})

    # if the are inactive or don't have access
    return JsonResponse({"access": False, "name": user.first_name, "door": door.name})


@login_required
@no_noobs
def list_causes(request):
    causes = Causes.objects.all()
    members = Profile.objects.all()

    return render(request, 'list_causes.html', {"causes": causes, "members": members})


def webcams(request):
    return render(request, 'webcams.html')


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
def open_door(request, door_id):
    door = Doors.objects.get(pk=door_id)
    if door in request.user.profile.doors.all():
        log_user_event(request.user, "Opened {} door via API.".format(door.name), "door")
        return JsonResponse({"success": door.unlock()})

    return HttpResponseForbidden("You are not authorised to access that door.")


@reader_auth
def authorised_tags(request, door_id=None):
    door = None

    if door_id is not None:
        try:
            door = Doors.objects.get(pk=door_id)
            door.checkin()

        except ObjectDoesNotExist:
            # send back some random error code you can search for here - this means the door ID doesn't exist.
            log_event("Tried to get authorised tags for non existant door.", "error", request)
            return HttpResponseBadRequest("Bad Request. Error AJld")

    else:
        try:
            door_ip = request.META.get('REMOTE_ADDR')
            door = Doors.objects.get(ip_address=door_ip)
            door.checkin()

        except ObjectDoesNotExist:
            # send back some random error code you can search for here - this means the door doesn't exist.
            log_event("Tried to get authorised tags for non existant door (or IP set incorrectly).", "error", request)
            return HttpResponseBadRequest("Bad Request. Error AJlc")

    authorised_tags = list()

    for profile in Profile.objects.all():
        if door in profile.doors.all():
            authorised_tags.append(profile.rfid)

    log_event("Got authorised tags for {} door.".format(door.name), "door")
    return JsonResponse({"authorised_tags": authorised_tags, "door": door.name})


@login_required
@no_noobs
def manage_spacebucks(request):
    spacebucks_transactions = SpaceBucks.objects.filter(user=request.user)

    return render(request, 'manage_spacebucks.html', {"spacebucks_transactions": spacebucks_transactions})


@login_required
@no_noobs
def add_spacebucks(request, amount=None):
    if request.method == "POST":
        if "STRIPE_SECRET_KEY" in os.environ:
            stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
            stripe.default_http_client = stripe.http_client.RequestsClient()
        else:
            return HttpResponseServerError("No stripe API details found.")

        if amount is not None:
            # lets restrict this to something reasonable
            if amount <= 50:
                log_user_event(request.user,
                               "Attempting to charge {} for ${}.".format(request.user.get_full_name(), amount),
                               "stripe")
                charge = stripe.Charge.create(
                    amount=amount * 100,  # convert to cents,
                    currency='aud',
                    description='HSBNE Spacebucks ({})'.format(request.user.get_full_name()),
                    customer=request.user.profile.stripe_customer_id,
                    metadata={'Payment By': request.user.get_full_name(), "For": "Spacebucks Top Up"},
                )

                if charge.paid:
                    transaction = SpaceBucks()
                    transaction.amount = amount
                    transaction.user = request.user
                    transaction.description = "Added spacebucks via Stripe"
                    transaction.transaction_type = "stripe"
                    transaction.logging_info = charge
                    transaction.save()
                    log_user_event(request.user,
                                   "Successfully charged {} for ${}.".format(request.user.get_full_name(), amount),
                                   "stripe")

                    return render(request, 'add_spacebucks.html',
                                  {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": True,
                                   "message": "Successfully charged ${} to your card ending in {}. Please check your spacebucks balance.".format(
                                       amount, request.user.profile.stripe_card_last_digits)})
                else:
                    log_user_event(request.user,
                                   "Problem charging {}.".format(request.user.get_full_name()),
                                   "stripe")
                    return render(request, 'add_spacebucks.html',
                                  {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                                   "message": "There was a problem collecting the funds off your card."})
            else:
                log_user_event(request.user, "Tried to add more than $50 to spacebucks via stripe.", "stripe")

        return render(request, 'add_spacebucks.html',
                      {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                       "message": "Invalid amount."})

    else:
        if "STRIPE_PUBLIC_KEY" in os.environ:
            return render(request, 'add_spacebucks.html', {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"]})

        else:
            return HttpResponseServerError("Error unable to find stripe details in environment variables.")


@csrf_exempt
def save_spacebucks_payment_info(request):
    if request.method == 'POST':
        if "STRIPE_SECRET_KEY" in os.environ:
            stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
            stripe.default_http_client = stripe.http_client.RequestsClient()
        else:
            return HttpResponseServerError("Can't find stripe API details.")

        try:
            log_user_event(request.user,
                           "Attempting to create stripe customer.", "stripe")
            customer = stripe.Customer.create(
                source=request.POST.get("stripeToken"),
                email=request.POST.get("stripeEmail"),
            )

            profile = request.user.profile
            profile.stripe_customer_id = customer.id
            profile.stripe_card_expiry = str(customer.sources.data[0]['exp_month']) + '/' + str(
                customer.sources.data[0]['exp_year'])
            profile.stripe_card_last_digits = customer.sources.data[0]['last4']
            profile.save()
            log_user_event(request.user, "Created stripe customer.".format(request.user.get_full_name()), "stripe")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            log_user_event(request.user, "Card declined while saving payment details.", "stripe")

            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": err})

        except stripe.error.RateLimitError as e:
            log_user_event(request.user, "Rate limtied while saving payment details.", "stripe")
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server is talking to stripe too quickly, try again later."})

        except stripe.error.InvalidRequestError as e:
            log_user_event(request.user, "Invalid request while saving payment details.", "stripe", request)
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "There was an error with the request details."})

        except stripe.error.AuthenticationError as e:
            log_user_event(request.user, "Can't authenticate with stripe while saving payment details.", "stripe")
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to authenticate with the Stripe server."})

        except stripe.error.APIConnectionError as e:
            log_user_event(request.user, "Stripe API connection error while saving payment details.", "stripe")
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to communicate with the Stripe server."})

        except stripe.error.StripeError as e:
            log_user_event(request.user, "Unkown stripe while saving payment details.", "stripe", request)
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": e})

        except Exception as e:
            log_user_event(request.user, "Unkown other error while saving payment details.", "stripe", request)
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Unkown error (unrelated to stripe)."})

        log_user_event(request.user, "Successfully save payment details.", "stripe")
        return render(request, 'add_spacebucks.html',
                      {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": True,
                       "message": "Your payment details were successfully saved."})

    else:
        return redirect(reverse('add_spacebucks'))


@login_required
@admin_required
def resend_welcome_email(request, member_id):
    success = User.objects.get(pk=member_id).profile.email_welcome()
    log_user_event(request.user, "Resent welcome email.", "profile")

    if success:
        return JsonResponse({"success": True})

    else:
        return JsonResponse({"success": False, "reason": "Unknown error. Error AlfSo"})
