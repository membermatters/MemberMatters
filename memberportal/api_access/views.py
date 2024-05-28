from django.utils import timezone
from access.models import (
    Doors,
    Interlock,
    HasExternalAccessControlAPIKey,
)
from profile.models import User

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from constance import config


class AccessSystemStatus(APIView):
    """
    get: This method returns the current status of the access system.
    """

    permission_classes = (HasExternalAccessControlAPIKey | permissions.IsAdminUser,)

    def get(self, request):
        statusObject = {
            "doors": [],
            "interlocks": [],
        }

        error_if_offline = request.GET.get("errorIfOffline", False)
        a_device_is_offline = False

        for door in Doors.objects.all():
            offline = door.get_unavailable()
            statusObject["doors"].append(
                {
                    "id": door.id,
                    "name": door.name,
                    "lastSeen": door.last_seen,
                    "lockedOut": door.locked_out,
                    "offline": offline,
                }
            )
            if offline and door.report_online_status:
                a_device_is_offline = True

        for interlock in Interlock.objects.all():
            offline = interlock.get_unavailable()
            statusObject["interlocks"].append(
                {
                    "id": interlock.id,
                    "name": interlock.name,
                    "lastSeen": interlock.last_seen,
                    "lockedOut": interlock.locked_out,
                    "offline": offline,
                }
            )
            if offline and interlock.report_online_status:
                a_device_is_offline = True

        if error_if_offline and a_device_is_offline:
            return Response(statusObject, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(statusObject)


class UserAccessPermissions(APIView):
    """
    get: This method returns the current user's access permissions.
    """

    def get(self, request):
        return Response(request.user.profile.get_access_permissions())


class AuthoriseDoor(APIView):
    """
    post: This method authorises a member to access a door.
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, door_id, user_id):
        member = User.objects.get(pk=user_id)
        door = Doors.objects.get(pk=door_id)

        member.profile.doors.add(door)
        member.profile.save()
        door.sync()

        return Response()


class AuthoriseInterlock(APIView):
    """
    put: This method authorises a member to access an interlock.
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, interlock_id, user_id):
        member = User.objects.get(pk=user_id)
        interlock = Interlock.objects.get(pk=interlock_id)

        member.profile.interlocks.add(interlock)
        member.profile.save()
        interlock.sync()

        return Response()


class RevokeDoor(APIView):
    """
    put: This method revokes a member's access to a door.
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, door_id, user_id):
        member = User.objects.get(pk=user_id)
        door = Doors.objects.get(pk=door_id)

        member.profile.doors.remove(door)
        member.profile.save()
        door.sync()

        return Response()


class RevokeInterlock(APIView):
    """
    post: This method revokes a member's access to an interlock.
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, interlock_id, user_id):
        member = User.objects.get(pk=user_id)
        interlock = Interlock.objects.get(pk=interlock_id)

        member.profile.interlocks.remove(interlock)
        member.profile.save()
        interlock.sync()

        return Response()


class SyncInterlock(APIView):
    """
    post: This method will force sync the specified interlock.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, interlock_id):
        interlock = Interlock.objects.get(pk=interlock_id)
        interlock.log_force_sync()

        return Response({"success": interlock.sync()})


class RebootInterlock(APIView):
    """
    post: This method will reboot the specified interlock.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, interlock_id):
        interlock = Interlock.objects.get(pk=interlock_id)
        interlock.log_force_rebooted()

        return Response({"success": interlock.reboot()})


class SyncDoor(APIView):
    """
    post: This method will force sync the specified door.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, door_id):
        door = Doors.objects.get(pk=door_id)
        door.log_force_sync()

        return Response({"success": door.sync(request=request)})


class RebootDoor(APIView):
    """
    post: This method will reboot the specified door.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, door_id):
        door = Doors.objects.get(pk=door_id)
        door.log_force_rebooted()

        return Response({"success": door.reboot(request=request)})


class BumpDoor(APIView):
    """
    post: This method will 'bump' the specified door. Note this MAY be called externally with an API key.
    """

    permission_classes = (HasExternalAccessControlAPIKey | permissions.IsAdminUser,)

    def post(self, request, door_id):
        # at this point the credentials been authorised by the permissions classes above
        # BUT we still need to check if the API is enabled or it's a user making the request
        if config.ENABLE_DOOR_BUMP_API or request.user.is_authenticated:
            door = Doors.objects.get(pk=door_id)
            bumped = door.bump()
            door.log_force_bump()
            return Response({"success": bumped})
        else:
            return Response(
                {"success": False, "error": "This API is disabled in the config."},
                status=status.HTTP_403_FORBIDDEN,
            )


class LockDevice(APIView):
    """
    post: This method will 'lock' the specified device. Note this MAY be called externally with an API key.
    """

    permission_classes = (HasExternalAccessControlAPIKey | permissions.IsAdminUser,)

    def post(self, request, door_id=None, interlock_id=None):
        # at this point the credentials been authorised by the permissions classes above
        # BUT we still need to check if the API is enabled or it's a user making the request
        if config.ENABLE_DOOR_BUMP_API or request.user.is_authenticated:
            device = (
                Doors.objects.get(pk=door_id)
                if door_id
                else Interlock.objects.get(pk=interlock_id)
            )
            locked = device.lock(request)
            device.log_force_lock()
            return Response({"success": locked})
        else:
            return Response(
                {"success": False, "error": "This API is disabled in the config."},
                status=status.HTTP_403_FORBIDDEN,
            )


class UnlockDevice(APIView):
    """
    post: This method will 'unlock' the specified device. Note this MAY be called externally with an API key.
    """

    permission_classes = (HasExternalAccessControlAPIKey | permissions.IsAdminUser,)

    def post(self, request, door_id=None, interlock_id=None):
        # at this point the credentials been authorised by the permissions classes above
        # BUT we still need to check if the API is enabled or it's a user making the request
        if config.ENABLE_DOOR_BUMP_API or request.user.is_authenticated:
            device = (
                Doors.objects.get(pk=door_id)
                if door_id
                else Interlock.objects.get(pk=interlock_id)
            )
            unlocked = device.unlock(request)
            device.log_force_unlock()
            return Response({"success": unlocked})
        else:
            return Response(
                {"success": False, "error": "This API is disabled in the config."},
                status=status.HTTP_403_FORBIDDEN,
            )
