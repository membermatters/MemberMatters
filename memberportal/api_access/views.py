from django.utils import timezone
from access.models import Doors, Interlock
from profile.models import User

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from constance import config


class AccessSystemStatus(APIView):
    """
    get: This method returns the current status of the access system.
    """

    permission_classes = (permissions.AllowAny,)

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
            if offline:
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
            if offline:
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
    post: This method authorises a member to access an interlock.
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
    post: This method revokes a member's access to a door.
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


class RebootInterlock(APIView):
    """
    post: This method will reboot the specified interlock.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, interlock_id):
        interlock = Interlock.objects.get(pk=interlock_id)

        return Response({"success": interlock.reboot()})


class RebootDoor(APIView):
    """
    post: This method will reboot the specified door.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, door_id):
        door = Doors.objects.get(pk=door_id)

        return Response({"success": door.reboot()})


class UnlockDoor(APIView):
    """
    post: This method will unlock the specified door.
    """

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, door_id):
        door = Doors.objects.get(pk=door_id)

        return Response({"success": door.unlock()})


class BumpDoor(APIView):
    """
    post: This method will 'bump' the specified door.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, door_id):
        bump_api_key = config.DOOR_BUMP_API_KEY  # grab the key from the config
        bump_api_enabled = (
            config.ENABLE_DOOR_BUMP_API
        )  # grab the enabled status from the config

        # grab the key from the request
        provided_key = request.query_params.get("secret") or request.headers.get(
            "Authorization", ""
        )

        if not bump_api_enabled:
            return Response(
                {"success": False, "error": "This API is disabled in the config."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not len(bump_api_key):
            return Response(
                {
                    "success": False,
                    "message": "DOOR_BUMP_API_KEY not set on server.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if provided_key != bump_api_key:
            return Response(
                {
                    "success": False,
                    "message": "Invalid API key.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        else:
            door = Doors.objects.get(pk=door_id)
            return Response({"success": door.unlock()})
