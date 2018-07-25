from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest, HttpResponse, \
    HttpResponseServerError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import *
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


def log_admin_action(admin_user, member_id, action="unknown", description="none"):
    """
    Called to log admin action to the DB.
    :param admin_user: user object of logged in admin performing the request.
    :param member_id: id number of member action is being performed on.
    :param action: brief description of the action being taken.
    :param description: either a brief description of why or the raw request params.
    :return:
    """

    if "csrfmiddlewaretoken" in description:
        import re
        description = re.sub(r"csrfmiddlewaretoken=[a-zA-Z0-9]*&", '', description)

    member = User.objects.get(pk=member_id)
    AdminLog(log_user=admin_user, action=action, log_member=member, description=description).save()


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
                               "operational aspects of HSBNE. To book in, click the link below.".format(new_user.first_name),
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
    return render(request, 'registration/login.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
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
            log_admin_action(request.user, member_id, "edited member profile", str(request.body))

    # render the form and return it
    data['html_form'] = render_to_string('partial_admin_edit_member.html', {'form': form, 'member_id': member_id},
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
            return HttpResponseRedirect('%s' % (reverse('profile')))

    else:
        # if it's not a form submission, return an empty form
        user_form = EditUserForm(instance=request.user)
        cause_form = EditCausesForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, "cause_form": cause_form})


@login_required
def edit_causes(request):
    """
    The edit causes view.
    :param request:
    :return:
    """
    if request.method == 'POST':
        user = Profile.objects.get(user=request.user)
        form = EditCausesForm(request.POST, instance=user)
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            return HttpResponseRedirect('%s' % (reverse('profile')))
        else:
            # otherwise return form with errors
            return render(request, 'edit_causes.html', {'form': form})

    else:
        # if it's not a form submission, return an empty form
        user = Profile.objects.get(user=request.user)
        form = EditCausesForm(instance=user)
        return render(request, 'edit_causes.html', {'form': form})


@login_required
def spacebug(request):
    form_class = SpacebugForm

    return render(request, 'spacebug.html', {
        'form': form_class,
    })

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

    # grab the user object and save the state
    user = User.objects.get(id=member_id)

    # if user state changes to active - give default access
    if state == 'active':
        if user.profile.state == "noob":
            for door in Doors.objects.filter(all_members=True):
                user.profile.doors.add(door)
            user.profile.email_new_member()

        else:
            user.profile.email_enable_member()

    else:
        user.profile.email_disable_member()


    user.profile.state = state
    user.profile.save()

    return JsonResponse({"success": True})


@login_required
@admin_required
def manage_causes(request):
    if request.method == 'POST':
        form = CauseForm(request.POST)
        if form.is_valid():
            form.save()
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
    Causes.objects.get(pk=cause_id).delete()
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
    Doors.objects.get(pk=door_id).delete()
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
    if request.method == 'POST':
        form = DoorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("manage_doors"))

    else:
        form = DoorForm()

    return render(request, 'edit_theme_song.html', {"form": form})


@login_required
@admin_required
def admin_grant_door(request, door_id, member_id):
    try:
        user = User.objects.get(pk=member_id)
        user.profile.doors.add(Doors.objects.get(pk=door_id))
        user.profile.save()
        return JsonResponse({"success": True})

    except Exception:
        return JsonResponse({"success": False, "reason": "Bad Request. Error AhSv"})


@login_required
@admin_required
def admin_revoke_door(request, door_id, member_id):
    try:
        user = User.objects.get(pk=member_id)
        user.profile.doors.remove(Doors.objects.get(pk=door_id))
        user.profile.save()
        return JsonResponse({"success": True})

    except ObjectDoesNotExist:
        return JsonResponse({"success": False, "reason": "No access permission was found."})


@login_required
@no_noobs
def request_access(request, door_id):
    return JsonResponse({"success": False, "reason": "Not implemented yet."})


def log_door_access(user, door):
    """
    Logs a door as being accessed.
    :param user:
    :param door_id:
    :return:
    """
    return DoorLog(user=user, door=door).save()


@reader_auth
def check_access(request, rfid_code, door_id=None):
    door = None

    try:
        user = Profile.objects.get(rfid=rfid_code).user
    except ObjectDoesNotExist:
        # send back some random error code you can search for here - this means the RFID tag doesn't exist.
        return HttpResponseBadRequest("Bad Request. Error AhDA")

    if user.profile.state == "active":
        if door_id is not None:
            try:
                door = Doors.objects.get(pk=door_id)
                door.checkin()

            except ObjectDoesNotExist:
                # send back some random error code you can search for here - this means the door ID doesn't exist.
                return HttpResponseBadRequest("Bad Request. Error AJld")

        else:
            try:
                door_ip = request.META.get('REMOTE_ADDR')
                door = Doors.objects.get(ip_address=door_ip)
                door.checkin()

            except ObjectDoesNotExist:
                # send back some random error code you can search for here - this means the door doesn't exist.
                return HttpResponseBadRequest("Bad Request. Error AJlc")

        allowed_doors = user.profile.doors.all()

        if allowed_doors:
            if door in allowed_doors:
                # user has access
                log_door_access(user, door)
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
    if door in request.user.doors.all():
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
            return HttpResponseBadRequest("Bad Request. Error AJld")

    else:
        try:
            door_ip = request.META.get('REMOTE_ADDR')
            door = Doors.objects.get(ip_address=door_ip)
            door.checkin()

        except ObjectDoesNotExist:
            # send back some random error code you can search for here - this means the door doesn't exist.
            return HttpResponseBadRequest("Bad Request. Error AJlc")

    authorised_tags = list()

    for profile in Profile.objects.all():
        if door in profile.doors.all():
            authorised_tags.append(profile.rfid)

    # if the are inactive or don't have access
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
            return HttpResponseServerError("Unkown error.")

        if amount is not None:
            # lets restrict this to something reasonable
            if amount <= 50:
                charge = stripe.Charge.create(
                    amount=amount * 100,  # convert to cents,
                    currency='aud',
                    description='HSBNE Spacebucks ({})'.format(request.user.get_full_name()),
                    customer=request.user.profile.stripe_customer_id,
                    metadata={'Payment By': request.user.get_full_name(), "For": "Spacebucks Top Up"},
                )
                print(charge.paid)
                print(charge)
                if charge.paid:
                    transaction = SpaceBucks()
                    transaction.amount = amount
                    transaction.user = request.user
                    transaction.description = "Added spacebucks via Stripe"
                    transaction.transaction_type = "stripe"
                    transaction.logging_info = charge
                    transaction.save()

                    return render(request, 'add_spacebucks.html', {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": True,
                                   "message": "Successfully charged ${} to your card ending in {}. Please check your spacebucks balance.".format(amount, request.user.profile.stripe_card_last_digits)})
                else:
                    return render(request, 'add_spacebucks.html',
                                  {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                                   "message": "There was a problem collecting the funds off your card."})

        return render(request, 'add_spacebucks.html', {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
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
            return HttpResponseServerError("Unkown error.")

        try:
            customer = stripe.Customer.create(
                source=request.POST.get("stripeToken"),
                email=request.POST.get("stripeEmail"),
            )
            print(customer.id)
            profile = request.user.profile
            profile.stripe_customer_id = customer.id
            profile.stripe_card_expiry = str(customer.sources.data[0]['exp_month']) + '/' + str(customer.sources.data[0]['exp_year'])
            profile.stripe_card_last_digits = customer.sources.data[0]['last4']
            profile.save()

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": err})

        except stripe.error.RateLimitError as e:
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server is talking to stripe too quickly, try again later."})

        except stripe.error.InvalidRequestError as e:
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "There was an error with the request details."})

        except stripe.error.AuthenticationError as e:
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to authenticate with the Stripe server."})

        except stripe.error.APIConnectionError as e:
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": "Our server was unable to communicate with the Stripe server."})

        except stripe.error.StripeError as e:
            return render(request, 'add_spacebucks.html',
                          {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False,
                           "message": e})

        except Exception as e:
            return render(request, 'add_spacebucks.html', {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": False, "message": "Unkown error (unrelated to stripe)."})

        return render(request, 'add_spacebucks.html', {"STRIPE_PUBLIC_KEY": os.environ["STRIPE_PUBLIC_KEY"], "success": True, "message": "Your payment details were successfully saved."})

    else:
        return redirect(reverse('add_spacebucks'))


@login_required
@admin_required
def resend_welcome_email(request, member_id):
    success = User.objects.get(pk=member_id).profile.email_welcome()

    if success:
        return JsonResponse({"success": True})

    else:
        return JsonResponse({"success": False, "reason": "Unknown error. Error AlfSo"})