from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse
from memberportal.helpers import log_user_event
from memberportal.decorators import no_noobs, admin_required, api_auth
from profile.models import User
from .forms import *
from .models import *
from profile.models import Profile
import pytz
import time
import requests
import os
from datetime import timedelta
from django.utils import timezone
import humanize
import hashlib
import urllib

utc = pytz.UTC
request_timeout = settings.REQUEST_TIMEOUT

@login_required
@admin_required
def manage_doors(request):
    if not request.user.profile.can_manage_doors:
        return HttpResponseForbidden("You do not have permission to access that.")

    doors = Doors.objects.all()
    return render(request, 'manage_doors.html', {"doors": doors})


@login_required
@admin_required
def add_door(request):
    if not request.user.profile.can_manage_doors:
        return HttpResponseForbidden("You do not have permission to access that.")

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
    if not request.user.profile.can_manage_doors:
        return HttpResponseForbidden("You do not have permission to access that.")

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
    if not request.user.profile.can_manage_doors:
        return HttpResponseForbidden("You do not have permission to access that.")

    door = Doors.objects.get(pk=door_id)
    log_user_event(request.user, "Deleted {} door.".format(door.name), "admin")
    door.delete()
    return HttpResponseRedirect('%s' % (reverse('manage_doors')))


@login_required
@admin_required
def admin_grant_door(request, door_id, member_id):
    if not request.user.profile.can_manage_access:
        return HttpResponseForbidden("You do not have permission to access that.")

    try:
        user = User.objects.get(pk=member_id)
        door = Doors.objects.get(pk=door_id)
        user.profile.doors.add(door)
        user.profile.save()
        log_user_event(user, "Access to {} granted.".format(door.name), "profile")
        log_user_event(request.user, "Access to {} granted for {}.".format(door.name, user.profile.get_full_name()),
                       "admin")

        return JsonResponse({"success": True})

    except Exception:
        return JsonResponse({"success": False, "reason": "Bad Request. User or door not found."})


@login_required
@admin_required
def admin_revoke_door(request, door_id, member_id):
    if not request.user.profile.can_manage_access:
        return HttpResponseForbidden("You do not have permission to access that.")

    try:
        user = User.objects.get(pk=member_id)
        door = Doors.objects.get(pk=door_id)
        user.profile.doors.remove(door)
        user.profile.save()
        log_user_event(user, "Access to {} revoked.".format(door.name), "profile")
        log_user_event(request.user, "Access to {} revoked for {}.".format(door.name, user.profile.get_full_name()),
                       "admin")

        return JsonResponse({"success": True})

    except ObjectDoesNotExist:
        return JsonResponse({"success": False, "reason": "No access permission was found."})


def play_theme_song(user):
    url = "http://10.0.1.50/playmp3.php?nickname="
    url = url + urllib.parse.quote_plus(user.profile.screen_name)

    try:
        requests.get(url, timeout=request_timeout)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        return True

    return False


def post_door_swipe_to_discord(name, door, successful):
    if "DISCORD_DOOR_WEBHOOK" in os.environ:
        url = os.environ.get('DISCORD_DOOR_WEBHOOK')

        json_message = {
            "description": "",
            "embeds": []
        }

        if successful:
            json_message['embeds'].append({
                "description": ":unlock: {} just **successfully** swiped at {} door.".format(name, door),
                "color": 5025616
            })

        else:
            json_message['embeds'].append({
                "description": "{} just swiped at {} door but was **rejected**. You can check your access [here](https://portal.hsbne.org/profile/access/view/).".format(
                    name, door),
                "color": 16007990
            })

        try:
            requests.post(url, json=json_message, timeout=request_timeout)
        except requests.exceptions.ReadTimeout:
            return True

    return False


def post_interlock_swipe_to_discord(name, interlock, type, time=None):
    if "DISCORD_INTERLOCK_WEBHOOK" in os.environ:
        url = os.environ.get('DISCORD_INTERLOCK_WEBHOOK')

        json_message = {
            "description": "",
            "embeds": []
        }

        if type == "activated":
            json_message['embeds'].append({
                "description": ":unlock: {} just **activated** the {}.".format(name, interlock),
                "color": 5025616
            })

        elif type == "rejected":
            json_message['embeds'].append({
                "description": "{} tried to activate the {} but was **rejected**. You can check your access [here](https://portal.hsbne.org/profile/access/view/).".format(
                    name, interlock),
                "color": 16007990
            })

        elif type == "left_on":
            json_message['embeds'].append({
                "description": ":lock: The {} was just turned off by the access system because it timed out (last used by {}). It was on for {}.".format(interlock, name, time),
                "color": 16750592
            })

        elif type == "deactivated":
            json_message['embeds'].append({
                "description": ":lock: {} just **deactivated** the {}. It was on for {}.".format(name, interlock, time),
                "color": 5025616
            })

        elif type == "maintenance_lock_out":
            json_message['embeds'].append({
                "description": "{} tried to access the {} but it is currently under a maintenance lockout".format(name, interlock),
                "color": 16007990
            })

        try:
            requests.post(url, json=json_message, timeout=request_timeout)
        except requests.exceptions.ReadTimeout:
            return True

    return False


@api_auth
def check_door_access(request, rfid_code, door_id=None):
    try:
        user = Profile.objects.get(rfid=rfid_code).user

    except ObjectDoesNotExist:
        log_event("Tried to check access for non existent user (or rfid not set).", "error", request)
        return JsonResponse({"access": False,
                             "error": "Tried to check access for non existent user (or rfid not set).",
                             "timestamp": round(time.time())})

    if door_id is not None:
        try:
            door = Doors.objects.get(pk=door_id)
            door.checkin()

        except ObjectDoesNotExist:
            log_event("Tried to check access for non existent door.", "error", request)
            return JsonResponse({"access": False,
                                 "error": "Tried to check access for non existent door",
                                 "timestamp": round(time.time())})

    else:
        door_ip = request.META.get('REMOTE_ADDR')

        try:
            door = Doors.objects.get(ip_address=door_ip)
            door.checkin()

        except ObjectDoesNotExist:
            log_event("Tried to check access for door {} but none found. (or IP not set)".format(door_ip), "error",
                      request)
            return JsonResponse({"access": False,
                                 "error": "Tried to check access for door {} but none found. (or IP not set)".format(door_ip),
                                 "timestamp": round(time.time())})

    if user.profile.state == "active":
        allowed_doors = user.profile.doors.all()

        if door.locked_out:
            post_interlock_swipe_to_discord(user.profile.get_full_name(), door.name, "maintenance_lock_out")
            return JsonResponse({"access": False, "error": "Maintenance lockout enabled.", "timestamp": round(time.time())})

        if allowed_doors:
            if door in allowed_doors:
                # user has access
                door.log_access(user.id)
                user.profile.update_last_seen()
                post_door_swipe_to_discord(user.profile.get_full_name(), door.name, True)
                if door.play_theme:
                    play_theme_song(user)

                return JsonResponse({"access": True, "name": user.profile.first_name})

    # if the are inactive or don't have access
    user.profile.update_last_seen()
    post_door_swipe_to_discord(user.profile.get_full_name(), door.name, False)
    return JsonResponse({"access": False, "name": user.profile.first_name})


@login_required
@admin_required
def bump_door(request, door_id):
    if not request.user.profile.can_manage_doors:
        return HttpResponseForbidden("You do not have permission to access that.")

    door = Doors.objects.get(pk=door_id)
    if door in request.user.profile.doors.all():
        log_user_event(request.user, "Bumped {} door via API.".format(door.name), "door")
        return JsonResponse({"success": door.bump()})

    return JsonResponse({"success": False, "message": "You are not authorised to access that door."})


@login_required
@admin_required
def lock_interlock(request, interlock_id):
    if not request.user.profile.can_manage_interlocks:
        return HttpResponseForbidden("You do not have permission to access that.")
        interlock = Interlock.objects.get(pk=interlock_id)
        log_user_event(request.user, "Locked {} interlock via API.".format(interlock.name), "interlock")
        return JsonResponse({"success": interlock.lock()})


def get_door_tags(door, return_hash=False):
    try:
        door = Doors.objects.get(pk=door)

    except (ObjectDoesNotExist, ValueError):
        try:
            door = Doors.objects.get(ip_address=door)

        except ObjectDoesNotExist:
            return False

        except TypeError:
            return False

    door.checkin()
    authorised_tags = list()

    for profile in Profile.objects.all():
        if door in profile.doors.all() and profile.state == "active":
            if profile.rfid:
                authorised_tags.append(profile.rfid)

    if return_hash:
        return hashlib.md5(str(authorised_tags).encode('utf-8')).hexdigest()

    else:
        return authorised_tags


def get_interlock_tags(interlock, return_hash=False):
    try:
        interlock = Interlock.objects.get(pk=interlock)

    except (ObjectDoesNotExist, ValueError):
        try:
            interlock = Interlock.objects.get(ip_address=interlock)

        except ObjectDoesNotExist:
            return False

        except TypeError:
            return False

    interlock.checkin()
    authorised_tags = list()

    for profile in Profile.objects.all():
        if interlock in profile.interlocks.all() and profile.state == "active":
            if profile.rfid:
                authorised_tags.append(profile.rfid)

    if return_hash:
        return hashlib.md5(str(authorised_tags).encode('utf-8')).hexdigest()

    else:
        return authorised_tags


@api_auth
def interlock_checkin(request, interlock=None):
    if interlock is not None:
        authorised_tags = get_interlock_tags(interlock, True)

        if authorised_tags:
            return JsonResponse({"success": True, "hashOfTags": authorised_tags, "timestamp": round(time.time())})

        else:
            log_event("Tried to check access for non existent interlock.", "error", request)
            return JsonResponse({"success": False, "error": "Error interlock does not exist.", "timestamp": round(time.time())})

    else:
        ip = request.META.get('REMOTE_ADDR')
        authorised_tags = get_interlock_tags(ip, True)

        if authorised_tags:
            return JsonResponse({"success": True, "hashOfTags": authorised_tags, "timestamp": round(time.time())})

        else:
            log_event("Tried to check access for non existent interlock.", "error", request)
            return JsonResponse({"success": False, "error": "Error interlock does not exist.", "timestamp": round(time.time())})


@api_auth
def door_checkin(request, door=None):
    if door is not None:
        authorised_tags = get_door_tags(door, True)

        if authorised_tags:
            return JsonResponse({"success": True, "hashOfTags": authorised_tags, "timestamp": round(time.time())})

        else:
            log_event("Tried to check access for non existent door.", "error", request)
            return JsonResponse({"success": False, "error": "Error door does not exist.", "timestamp": round(time.time())})

    else:
        ip = request.META.get('REMOTE_ADDR')
        authorised_tags = get_door_tags(ip, True)

        if authorised_tags:
            return JsonResponse({"success": True, "hashOfTags": authorised_tags, "timestamp": round(time.time())})

        else:
            log_event("Tried to check access for non existent door.", "error", request)
            return JsonResponse({"success": False, "error": "Error door does not exist.", "timestamp": round(time.time())})


@api_auth
def authorised_door_tags(request, door=None):
    if door is not None:
        tags = get_door_tags(door)

        if tags:
            tags_hash = hashlib.md5(str(tags).encode('utf-8')).hexdigest()

            return JsonResponse({"authorised_tags": tags, "authorised_tags_hash": tags_hash})

        else:
            log_event("Tried to get authorised tags for non existent interlock.", "error", request)
            return JsonResponse({"access": False,
                                 "error": "Tried to get authorised tags for non existent interlock.",
                                 "timestamp": round(time.time())})

    else:
        ip = request.META.get('REMOTE_ADDR')
        tags = get_door_tags(ip)

        if tags:
            tags_hash = hashlib.md5(str(tags).encode('utf-8')).hexdigest()

            return JsonResponse({"authorised_tags": tags, "authorised_tags_hash": tags_hash})

        else:
            log_event("Tried to get tags for non existent door {} (or IP set incorrectly).".format(ip), "error", request)
            return JsonResponse({"access": False,
                                 "error": "Tried to get tags for non existent door {} (or IP set incorrectly).".format(ip),
                                 "timestamp": round(time.time())})


@api_auth
def authorised_interlock_tags(request, interlock=None):
    if interlock is not None:
        tags = get_interlock_tags(interlock)
        if tags:
            tags_hash = hashlib.md5(str(tags).encode('utf-8')).hexdigest()

            return JsonResponse({"authorised_tags": tags, "authorised_tags_hash": tags_hash})

        else:
            log_event("Tried to get authorised tags for non existent interlock.", "error", request)
            return JsonResponse({"access": False,
                                 "error": "Tried to get authorised tags for non existent interlock.",
                                 "timestamp": round(time.time())})

    else:
        ip = request.META.get('REMOTE_ADDR')
        tags = get_interlock_tags(ip)

        if tags:
            tags_hash = hashlib.md5(str(tags).encode('utf-8')).hexdigest()
            return JsonResponse({"authorised_tags": tags, "authorised_tags_hash": tags_hash})

        else:
            log_event("Tried to get tags for non existent interlock {} (or IP set incorrectly).".format(ip), "error", request)
            return JsonResponse({"access": False,
                                 "error": "Tried to get tags for non existent interlock {} (or IP set incorrectly).".format(ip),
                                 "timestamp": round(time.time())})


@login_required
@admin_required
def manage_interlocks(request):
    if not request.user.profile.can_manage_interlocks:
        return HttpResponseForbidden("You do not have permission to access that.")

    interlocks = Interlock.objects.all()
    return render(request, 'manage_interlocks.html', {"interlocks": interlocks})


@login_required
@admin_required
def view_interlock_sessions(request):
    if not request.user.profile.can_manage_interlocks:
        return HttpResponseForbidden("You do not have permission to access that.")

    raw_sessions = InterlockLog.objects.all()
    interlock_sessions = []

    for session in raw_sessions:
        user_off = "IN USE"
        if session.user_off:
            user_off = session.user_off.profile.get_full_name()
        session = {
            "id": session.id,
            "interlock_name": session.interlock.name,
            "time_on": timezone.make_naive(session.first_heartbeat).strftime("%Y-%m-%d %H:%M:%S"),
            "time_off": timezone.make_naive(session.last_heartbeat).strftime("%Y-%m-%d %H:%M:%S"),
            "user_on": session.user.profile.get_full_name(),
            "user_off": user_off,
            "on_for": humanize.naturaldelta(session.last_heartbeat - session.first_heartbeat),
            "completed": session.session_complete
        }
        interlock_sessions.append(session)

    return render(request, 'view_interlock_sessions.html', {"sessions": interlock_sessions})


@login_required
@admin_required
def add_interlock(request):
    if not request.user.profile.can_manage_interlocks:
        return HttpResponseForbidden("You do not have permission to access that.")

    if request.method == 'POST':
        form = InterlockForm(request.POST)
        if form.is_valid():
            form.save()
            log_user_event(
                request.user,
                "Created {} interlock.".format(form.cleaned_data['name']),
                "admin", form)
            return HttpResponseRedirect(reverse("manage_interlocks"))

    else:
        form = InterlockForm()

    return render(request, 'add_interlock.html', {"form": form})


@login_required
@admin_required
def edit_interlock(request, interlock_id):
    if not request.user.profile.can_manage_interlocks:
        return HttpResponseForbidden("You do not have permission to access that.")

    if request.method == 'POST':
        form = InterlockForm(request.POST, instance=Interlock.objects.get(pk=interlock_id))
        if form.is_valid():
            # if it was a form submission save it
            form.save()
            log_user_event(
                request.user,
                "Edited {} interlock.".format(Interlock.objects.get(pk=interlock_id).name),
                "admin", form)
            return HttpResponseRedirect('%s' % (reverse('manage_interlocks')))
        else:
            # otherwise return form with errors
            return render(request, 'edit_interlock.html', {'form': form})

    else:
        # if it's not a form submission, return an empty form
        form = InterlockForm(instance=Interlock.objects.get(pk=interlock_id))
        return render(request, 'edit_interlock.html', {'form': form})


@login_required
@admin_required
def delete_interlock(request, interlock_id):
    if not request.user.profile.can_manage_interlocks:
        return HttpResponseForbidden("You do not have permission to access that.")

    interlock = Interlock.objects.get(pk=interlock_id)
    log_user_event(request.user, "Deleted {} interlock.".format(interlock.name), "admin")
    interlock.delete()
    return HttpResponseRedirect('%s' % (reverse('manage_interlocks')))


@login_required
@admin_required
def admin_grant_interlock(request, interlock_id, member_id):
    if not request.user.profile.can_manage_access:
        return HttpResponseForbidden("You do not have permission to access that.")

    try:
        user = User.objects.get(pk=member_id)
        interlock = Interlock.objects.get(pk=interlock_id)
        user.profile.interlocks.add(interlock)
        user.profile.save()
        log_user_event(user, "Access to {} granted.".format(interlock.name), "profile")
        log_user_event(request.user,
                       "Access to {} granted for {}.".format(interlock.name, user.profile.get_full_name()), "admin")

        return JsonResponse({"success": True})

    except Exception:
        return JsonResponse({"success": False, "reason": "Bad Request. User or interlock not found."})


@login_required
@admin_required
def admin_revoke_interlock(request, interlock_id, member_id):
    if not request.user.profile.can_manage_access:
        return HttpResponseForbidden("You do not have permission to access that.")

    try:
        user = User.objects.get(pk=member_id)
        interlock = Interlock.objects.get(pk=interlock_id)
        user.profile.interlocks.remove(interlock)
        user.profile.save()
        log_user_event(user, "Access to {} revoked.".format(interlock.name), "profile")
        log_user_event(request.user,
                       "Access to {} revoked for {}.".format(interlock.name, user.profile.get_full_name()), "admin")

        return JsonResponse({"success": True})

    except ObjectDoesNotExist:
        return JsonResponse({"success": False, "reason": "No access permission was found."})


@api_auth
def check_interlock_access(request, rfid_code=None, interlock_id=None, session_id=None):
    interlock_ip = None

    if session_id is not None:
        session = InterlockLog.objects.get(pk=session_id)
        if not session.session_complete:
            session.heartbeat()
            return JsonResponse({"access": True, "timestamp": round(time.time())})

        else:
            return JsonResponse({"access": False, "error": "Session already ended.", "timestamp": round(time.time())})

    try:
        user = Profile.objects.get(rfid=rfid_code).user

    except ObjectDoesNotExist:
        log_event("Tried to check access for non existent user (or rfid not set).", "error", request)
        return JsonResponse(
            {"access": False, "error": "Tried to check access for non existent user (or rfid not set).",
             "timestamp": round(time.time())})

    if interlock_id is not None:
        try:
            interlock = Interlock.objects.get(pk=interlock_id)
            interlock.checkin()

        except ObjectDoesNotExist:
            log_event("Tried to check access for non existent interlock.", "error", request)
            return JsonResponse({"access": False, "error": "Tried to check access for non existent interlock.",
                                 "timestamp": round(time.time())})

    else:
        interlock_ip = request.META.get('REMOTE_ADDR')

        try:
            interlock = Interlock.objects.get(ip_address=interlock_ip)
            interlock.checkin()

        except ObjectDoesNotExist:
            log_event("Tried to check access for {} interlock but none found.".format(interlock_ip), "error", request)
            return JsonResponse({"access": False,
                                 "error": "Tried to check access for {} interlock but none found.".format(interlock_ip),
                                 "timestamp": round(time.time())})

    if user.profile.state == "active":
        if interlock.locked_out:
            post_interlock_swipe_to_discord(user.profile.get_full_name(), interlock.name, "maintenance_lock_out")
            return JsonResponse({"access": False, "error": "Maintenance lockout enabled.", "timestamp": round(time.time())})

        allowed_interlocks = user.profile.interlocks.all()

        if allowed_interlocks:
            if interlock in allowed_interlocks:
                # user has access
                session = interlock.create_session(user)
                user.profile.update_last_seen()
                post_interlock_swipe_to_discord(user.profile.get_full_name(), interlock.name, "activated")
                if interlock.play_theme:
                    play_theme_song(user)

                return JsonResponse({"access": True, "session_id": session.id, "timestamp": round(time.time()),
                                     "name": user.profile.first_name})

    # if they are inactive or don't have access
    user.profile.update_last_seen()
    post_interlock_swipe_to_discord(user.profile.get_full_name(), interlock.name, "rejected")
    return JsonResponse({"access": False, "name": user.profile.first_name})


@api_auth
def spacebucks_device_checkin(request, device_id=None):
    device_ip = None

    if device_id is not None:
        try:
            device = SpacebucksDevice.objects.get(pk=device_id)
            device.checkin()
            return JsonResponse({"success": True, "timestamp": round(time.time())})

        except ObjectDoesNotExist:
            log_event("Tried to check access for non existent spacebucks device.", "error", request)
            return JsonResponse(
                {"success": False, "error": "Error spacebucks device does not exist.", "timestamp": round(time.time())})

    else:
        try:
            device_ip = request.META.get('REMOTE_ADDR')
            device = SpacebucksDevice.objects.get(ip_address=device_ip)
            device.checkin()
            return JsonResponse({"success": True, "timestamp": round(time.time())})

        except ObjectDoesNotExist:
            log_event("Tried to check access for {} spacebucks device but none found.".format(device_ip), "error", request)
            return JsonResponse({"success": False, "error": "spacebucks device does not exist..",
                                 "timestamp": round(time.time())})


@api_auth
def interlock_cron(request):
    timedout_interlocks = InterlockLog.objects.filter(last_heartbeat__lt=timezone.now() - timedelta(minutes=2),
                                                      session_complete=False)

    if timedout_interlocks:
        for session in timedout_interlocks:
            session.session_complete = True
            session.save()
            session.interlock.checkin()
            on_time = humanize.naturaldelta(session.last_heartbeat - session.first_heartbeat)
            post_interlock_swipe_to_discord(session.user.profile.get_full_name(), session.interlock.name,
                                            "left_on", on_time)

    return HttpResponseRedirect("/")


@api_auth
def end_interlock_session(request, session_id, rfid=None):
    session = InterlockLog.objects.get(pk=session_id)
    if not session.session_complete:
        user = None
        if rfid is not None:
            user = Profile.objects.get(rfid=rfid).user
        else:
            user = session.user

        session.session_complete = True
        session.last_heartbeat = timezone.now()
        session.user_off = user
        session.save()
        session.interlock.checkin()
        on_time = humanize.naturaldelta(session.last_heartbeat - session.first_heartbeat)
        post_interlock_swipe_to_discord(session.user_off.profile.get_full_name(), session.interlock.name,
                                        "deactivated", on_time)

        return JsonResponse({"access": True})

    return JsonResponse({"access": False, "error": "Session already ended.", "timestamp": round(time.time())})


@api_auth
def reset_default_door_access(request):
    users = User.objects.all()
    doors = Doors.objects.filter(all_members=True)

    try:
        for user in users:
            for door in doors:
                user.profile.doors.add(door)

        return JsonResponse({"success": True})
    
    except:
        return JsonResponse({"success": False, "message": "Failed to reset access permissions for unknown reason."})

@api_auth
def reset_default_interlock_access(request):
    users = User.objects.all()
    interlocks = Interlock.objects.filter(all_members=True)

    try:
        for user in users:
            for interlock in interlocks:
                user.profile.interlocks.add(interlock)

        return JsonResponse({"success": True})

    except:
        return JsonResponse({"success": False, "message": "Failed to reset access permissions for unknown reason."})
