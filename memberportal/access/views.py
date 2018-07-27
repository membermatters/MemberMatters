from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from memberportal.helpers import log_event, log_user_event
from memberportal.decorators import no_noobs, admin_required, api_auth
from .forms import DoorForm
from .models import Doors
from profile.models import Profile

import pytz

utc = pytz.UTC


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
            log_user_event(
                request.user,
                "Created {} door.".format(form.cleaned_data['name']),
                "admin", form)
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
            log_user_event(
                request.user,
                "Edited {} door.".format(Doors.objects.get(pk=door_id).name),
                "admin", form)
            return HttpResponseRedirect('%s' % (reverse('manage_doors')))
        else:
            # otherwise return form with errors
            return render(request, 'edit_door.html', {'form': form})

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


@api_auth
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
def open_door(request, door_id):
    door = Doors.objects.get(pk=door_id)
    if door in request.user.profile.doors.all():
        log_user_event(request.user, "Opened {} door via API.".format(door.name), "door")
        return JsonResponse({"success": door.unlock()})

    return HttpResponseForbidden("You are not authorised to access that door.")


@api_auth
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
