from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401
from access.models import Doors, Interlock
from profile.models import User, Profile

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class UserAccessPermissions(APIView):
    """
    get: This method returns the current user's access permissions.
    """

    def get(self, request):
        return JsonResponse(request.user.profile.get_access_permissions())


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
