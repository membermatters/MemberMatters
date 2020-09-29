from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from membermatters.helpers import log_user_event
from membermatters.decorators import staff_required, api_auth
from profile.models import User
from .models import *
from profile.models import Profile
from django.db.models import *
from constance import config
import pytz
import time
import requests
from datetime import timedelta
from django.utils import timezone
import humanize
import hashlib
import urllib

from services.discord import post_interlock_swipe_to_discord, post_door_swipe_to_discord

utc = pytz.UTC
request_timeout = settings.REQUEST_TIMEOUT


def play_theme_song(user):
    if config.ENABLE_THEME_SWIPE:
        url = config.THEME_SWIPE_URL.format(
            urllib.parse.quote_plus(user.profile.screen_name)
        )

        try:
            requests.get(url, timeout=request_timeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return True

        return False

    return True


@api_auth
def check_door_access(request, rfid_code, door_id=None):
    try:
        user = Profile.objects.get(rfid=rfid_code).user

    except ObjectDoesNotExist:
        log_event(
            "Tried to check access for non existent user (or rfid not set).",
            "error",
            request,
        )
        print(
            "Tried to check access on ({}) for non existent user ({}) or rfid not set.".format(
                door_id, rfid_code
            )
        )
        return JsonResponse(
            {
                "access": False,
                "error": "Tried to check access for non existent user (or rfid not set).",
                "timestamp": round(time.time()),
            }
        )

    if door_id is not None:
        try:
            door = Doors.objects.get(pk=door_id)
            door.checkin()

        except ObjectDoesNotExist:
            log_event("Tried to check access for non existent door.", "error", request)
            print("Tried to check access for non existent door ({}).".format(door_id))
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to check access for non existent door",
                    "timestamp": round(time.time()),
                }
            )

    else:
        door_ip = request.META.get("HTTP_X_REAL_IP")

        try:
            door = Doors.objects.get(ip_address=door_ip)
            door.checkin()

        except ObjectDoesNotExist:
            log_event(
                "Tried to check access for door {} but none found. (or IP not set)".format(
                    door_ip
                ),
                "error",
                request,
            )
            print(
                "Tried to check access for non existent door ({}) ip ({}).".format(
                    door_id, door_ip
                )
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to check access for door {} but none found. (or IP not set)".format(
                        door_ip
                    ),
                    "timestamp": round(time.time()),
                }
            )

    if user.profile.state == "active":
        allowed_doors = user.profile.doors.all()

        if door.locked_out:
            post_interlock_swipe_to_discord(
                user.profile.get_full_name(), door.name, "maintenance_lock_out"
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Maintenance lockout enabled.",
                    "timestamp": round(time.time()),
                }
            )

        if allowed_doors:
            if door in allowed_doors:
                # user has access

                # if the user isn't signed into site and the door isn't exempt from this
                if (
                    not user.profile.is_signed_into_site()
                    and door.exempt_signin is False
                ):
                    user.profile.update_last_seen()
                    post_door_swipe_to_discord(
                        user.profile.get_full_name(), door.name, "not_signed_in"
                    )
                    return JsonResponse(
                        {"access": False, "name": user.profile.first_name}
                    )

                door.log_access(user.id)
                user.profile.update_last_seen()
                post_door_swipe_to_discord(
                    user.profile.get_full_name(), door.name, True
                )
                if door.play_theme:
                    play_theme_song(user)

                return JsonResponse({"access": True, "name": user.profile.first_name})

    # if the are inactive or don't have access
    user.profile.update_last_seen()
    post_door_swipe_to_discord(user.profile.get_full_name(), door.name, False)
    return JsonResponse({"access": False, "name": user.profile.first_name})


@login_required
@staff_required
def bump_door(request, door_id):
    if not request.user.profile.can_manage_doors:
        return HttpResponseForbidden("You do not have permission to access that.")

    door = Doors.objects.get(pk=door_id)
    if door in request.user.profile.doors.all():
        log_user_event(
            request.user, "Bumped {} door via API.".format(door.name), "door"
        )
        return JsonResponse({"success": door.unlock()})

    return JsonResponse(
        {"success": False, "message": "You are not authorised to access that door."}
    )


@login_required
@staff_required
def reboot_door(request, door_id):
    if not request.user.profile.can_manage_doors:
        return HttpResponseForbidden("You do not have permission to access that.")

    door = Doors.objects.get(pk=door_id)
    log_user_event(
        request.user, "Rebooted {} door via API.".format(door.name), "interlock"
    )
    return JsonResponse({"success": door.reboot()})


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
            if profile.rfid and (
                profile.is_signed_into_site() or door.exempt_signin is True
            ):
                authorised_tags.append(profile.rfid)

    if return_hash:
        return hashlib.md5(str(authorised_tags).encode("utf-8")).hexdigest()

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
            if profile.rfid and (
                profile.is_signed_into_site() or interlock.exempt_signin is True
            ):
                authorised_tags.append(profile.rfid)

    if return_hash:
        return hashlib.md5(str(authorised_tags).encode("utf-8")).hexdigest()

    else:
        return authorised_tags


@api_auth
def interlock_checkin(request, interlock=None):
    if interlock is not None:
        authorised_tags = get_interlock_tags(interlock, True)

        if authorised_tags:
            return JsonResponse(
                {
                    "success": True,
                    "hashOfTags": authorised_tags,
                    "timestamp": round(time.time()),
                }
            )

        else:
            log_event(
                "Tried to check access for non existent interlock.", "error", request
            )
            return JsonResponse(
                {
                    "success": False,
                    "error": "Error interlock does not exist.",
                    "timestamp": round(time.time()),
                }
            )

    else:
        ip = request.META.get("HTTP_X_REAL_IP")
        authorised_tags = get_interlock_tags(ip, True)

        if authorised_tags:
            return JsonResponse(
                {
                    "success": True,
                    "hashOfTags": authorised_tags,
                    "timestamp": round(time.time()),
                }
            )

        else:
            log_event(
                "Tried to check access for non existent interlock.", "error", request
            )
            return JsonResponse(
                {
                    "success": False,
                    "error": "Error interlock does not exist.",
                    "timestamp": round(time.time()),
                }
            )


@api_auth
def door_checkin(request, door=None):
    if door is not None:
        authorised_tags = get_door_tags(door, True)

        if authorised_tags:
            return JsonResponse(
                {
                    "success": True,
                    "hashOfTags": authorised_tags,
                    "timestamp": round(time.time()),
                }
            )

        else:
            log_event("Tried to check access for non existent door.", "error", request)
            return JsonResponse(
                {
                    "success": False,
                    "error": "Error door does not exist.",
                    "timestamp": round(time.time()),
                }
            )

    else:
        ip = request.META.get("HTTP_X_REAL_IP")
        authorised_tags = get_door_tags(ip, True)

        if authorised_tags:
            return JsonResponse(
                {
                    "success": True,
                    "hashOfTags": authorised_tags,
                    "timestamp": round(time.time()),
                }
            )

        else:
            log_event("Tried to check access for non existent door.", "error", request)
            return JsonResponse(
                {
                    "success": False,
                    "error": "Error door does not exist.",
                    "timestamp": round(time.time()),
                }
            )


@api_auth
def authorised_door_tags(request, door=None):
    if door is not None:
        tags = get_door_tags(door)

        if tags:
            tags_hash = hashlib.md5(str(tags).encode("utf-8")).hexdigest()

            return JsonResponse(
                {"authorised_tags": tags, "authorised_tags_hash": tags_hash}
            )

        else:
            log_event(
                "Tried to get authorised tags for non existent interlock.",
                "error",
                request,
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to get authorised tags for non existent interlock.",
                    "timestamp": round(time.time()),
                }
            )

    else:
        ip = request.META.get("HTTP_X_REAL_IP")
        tags = get_door_tags(ip)

        if tags:
            tags_hash = hashlib.md5(str(tags).encode("utf-8")).hexdigest()

            return JsonResponse(
                {"authorised_tags": tags, "authorised_tags_hash": tags_hash}
            )

        else:
            log_event(
                "Tried to get tags for non existent door {} (or IP set incorrectly).".format(
                    ip
                ),
                "error",
                request,
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to get tags for non existent door {} (or IP set incorrectly).".format(
                        ip
                    ),
                    "timestamp": round(time.time()),
                }
            )


@api_auth
def authorised_interlock_tags(request, interlock=None):
    if interlock is not None:
        tags = get_interlock_tags(interlock)
        if tags:
            tags_hash = hashlib.md5(str(tags).encode("utf-8")).hexdigest()

            return JsonResponse(
                {"authorised_tags": tags, "authorised_tags_hash": tags_hash}
            )

        else:
            log_event(
                "Tried to get authorised tags for non existent interlock.",
                "error",
                request,
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to get authorised tags for non existent interlock.",
                    "timestamp": round(time.time()),
                }
            )

    else:
        ip = request.META.get("HTTP_X_REAL_IP")
        tags = get_interlock_tags(ip)

        if tags:
            tags_hash = hashlib.md5(str(tags).encode("utf-8")).hexdigest()
            return JsonResponse(
                {"authorised_tags": tags, "authorised_tags_hash": tags_hash}
            )

        else:
            log_event(
                "Tried to get tags for non existent interlock {} (or IP set incorrectly).".format(
                    ip
                ),
                "error",
                request,
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to get tags for non existent interlock {} (or IP set incorrectly).".format(
                        ip
                    ),
                    "timestamp": round(time.time()),
                }
            )


@api_auth
def check_interlock_access(request, rfid_code=None, interlock_id=None, session_id=None):
    interlock_ip = None

    if session_id is not None:
        session = InterlockLog.objects.get(pk=session_id)
        if not session.session_complete:
            session.heartbeat()
            return JsonResponse({"access": True, "timestamp": round(time.time())})

        else:
            return JsonResponse(
                {
                    "access": False,
                    "error": "Session already ended.",
                    "timestamp": round(time.time()),
                }
            )

    try:
        user = Profile.objects.get(rfid=rfid_code).user

    except ObjectDoesNotExist:
        log_event(
            "Tried to check access for non existent user (or rfid not set).",
            "error",
            request,
        )
        print(
            "Tried to check access on ({}) for non existent user ({}) or rfid not set.".format(
                interlock_id, rfid_code
            )
        )
        return JsonResponse(
            {
                "access": False,
                "error": "Tried to check access for non existent user (or rfid not set).",
                "timestamp": round(time.time()),
            }
        )

    if interlock_id is not None:
        try:
            interlock = Interlock.objects.get(pk=interlock_id)
            interlock.checkin()

        except ObjectDoesNotExist:
            log_event(
                "Tried to check access for non existent interlock.", "error", request
            )
            print(
                "Tried to check access for non existent interlock ({}) user ({}).".format(
                    interlock_id, rfid_code
                )
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to check access for non existent interlock.",
                    "timestamp": round(time.time()),
                }
            )

    else:
        interlock_ip = request.META.get("HTTP_X_REAL_IP")

        try:
            interlock = Interlock.objects.get(ip_address=interlock_ip)
            interlock.checkin()

        except ObjectDoesNotExist:
            log_event(
                "Tried to check access for {} interlock but none found.".format(
                    interlock_ip
                ),
                "error",
                request,
            )
            print(
                "Tried to check access for non existent interlock ({}) ip ({}).".format(
                    interlock_id, interlock_ip
                )
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Tried to check access for {} interlock but none found.".format(
                        interlock_ip
                    ),
                    "timestamp": round(time.time()),
                }
            )

    if user.profile.state == "active":
        if interlock.locked_out:
            post_interlock_swipe_to_discord(
                user.profile.get_full_name(), interlock.name, "maintenance_lock_out"
            )
            return JsonResponse(
                {
                    "access": False,
                    "error": "Maintenance lockout enabled.",
                    "timestamp": round(time.time()),
                }
            )

        allowed_interlocks = user.profile.interlocks.all()

        if allowed_interlocks:
            if interlock in allowed_interlocks:
                # user has access

                # if the user isn't signed into site and the interlock isn't exempt
                if (
                    not user.profile.is_signed_into_site()
                    and interlock.exempt_signin is False
                ):
                    user.profile.update_last_seen()
                    post_door_swipe_to_discord(
                        user.profile.get_full_name(), interlock.name, "not_signed_in"
                    )
                    return JsonResponse(
                        {"access": False, "name": user.profile.first_name}
                    )

                session = interlock.create_session(user)
                user.profile.update_last_seen()
                post_interlock_swipe_to_discord(
                    user.profile.get_full_name(), interlock.name, "activated"
                )
                if interlock.play_theme:
                    play_theme_song(user)

                return JsonResponse(
                    {
                        "access": True,
                        "session_id": session.id,
                        "timestamp": round(time.time()),
                        "name": user.profile.first_name,
                    }
                )

    # if they are inactive or don't have access
    user.profile.update_last_seen()
    post_interlock_swipe_to_discord(
        user.profile.get_full_name(), interlock.name, "rejected"
    )
    return JsonResponse({"access": False, "name": user.profile.first_name})


@api_auth
def memberbucks_device_checkin(request, device_id=None):
    device_ip = None

    if device_id is not None:
        try:
            device = MemberbucksDevice.objects.get(pk=device_id)
            device.checkin()
            return JsonResponse({"success": True, "timestamp": round(time.time())})

        except ObjectDoesNotExist:
            log_event(
                f"Tried to check access for non existent {config.MEMBERBUCKS_NAME} device.",
                "error",
                request,
            )
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Error {config.MEMBERBUCKS_NAME} device does not exist.",
                    "timestamp": round(time.time()),
                }
            )

    else:
        try:
            device_ip = request.META.get("HTTP_X_REAL_IP")
            device = MemberbucksDevice.objects.get(ip_address=device_ip)
            device.checkin()
            return JsonResponse({"success": True, "timestamp": round(time.time())})

        except ObjectDoesNotExist:
            log_event(
                f"Tried to check access for {device_ip} {config.MEMBERBUCKS_NAME} device but none found.",
                "error",
                request,
            )
            return JsonResponse(
                {
                    "success": False,
                    "error": f"{config.MEMBERBUCKS_NAME} device does not exist..",
                    "timestamp": round(time.time()),
                }
            )


@api_auth
def interlock_cron(request):
    timedout_interlocks = InterlockLog.objects.filter(
        last_heartbeat__lt=timezone.now() - timedelta(minutes=2), session_complete=False
    )

    if timedout_interlocks:
        for session in timedout_interlocks:
            session.session_complete = True
            session.save()
            session.interlock.checkin()
            on_time = humanize.naturaldelta(
                session.last_heartbeat - session.first_heartbeat
            )
            post_interlock_swipe_to_discord(
                session.user.profile.get_full_name(),
                session.interlock.name,
                "left_on",
                on_time,
            )

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
        on_time = humanize.naturaldelta(
            session.last_heartbeat - session.first_heartbeat
        )
        post_interlock_swipe_to_discord(
            session.user_off.profile.get_full_name(),
            session.interlock.name,
            "deactivated",
            on_time,
        )

        return JsonResponse({"access": True})

    return JsonResponse(
        {
            "access": False,
            "error": "Session already ended.",
            "timestamp": round(time.time()),
        }
    )


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
        return JsonResponse(
            {
                "success": False,
                "message": "Failed to reset access permissions for unknown reason.",
            }
        )


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
        return JsonResponse(
            {
                "success": False,
                "message": "Failed to reset access permissions for unknown reason.",
            }
        )
