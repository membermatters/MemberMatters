from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from membermatters.decorators import login_required_401


@require_POST
@login_required_401
def api_meeting(request):
    """
    This method parses the meeting creation form
    :param request:
    :return:
    """
    pass


@require_POST
@login_required_401
def api_proxy(request):
    """
    This method parses the proxy creation form
    :param request:
    :return:
    """
    pass
