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

    return JsonResponse(request.user.profile.get_access_permissions())
