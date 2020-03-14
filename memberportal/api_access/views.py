from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401
from access.models import Doors, Interlock


@require_GET
@login_required_401
def api_get_access_permissions(request):
    """
    This method returns the current user's access permissions.
    :param request:
    :return:
    """
    doors = []
    interlocks = []
    user = request.user
    status = user.profile.state

    user_active = not (user.profile.state == "inactive" or user.profile.state == "noob")

    for door in Doors.objects.all():
        if door in user.profile.doors.all() and user_active:
            doors.append({"name": door.name, "access": True})

        else:
            doors.append({"name": door.name, "access": False})

    for interlock in Interlock.objects.all():
        if interlock in user.profile.interlocks.all() and user_active:
            interlocks.append({"name": interlock.name, "access": True})

        else:
            interlocks.append({"name": interlock.name, "access": False})

    return JsonResponse({"doors": doors, "interlocks": interlocks, "memberStatus": status})
