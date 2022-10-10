from access.models import Doors, Interlock
from profile.models import User

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from constance import config


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

        return Response()


class AuthoriseInterlock(APIView):
    """
    post: This method authorises a member to access an interlock.
    """

    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, interlock_id, user_id):
        member = User.objects.get(pk=user_id)
        door = Interlock.objects.get(pk=interlock_id)

        member.profile.interlocks.add(door)
        member.profile.save()

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
