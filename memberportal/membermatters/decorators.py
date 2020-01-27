from django.http import HttpResponseForbidden
import json


def admin_required(view):
    def wrap(request, *args, **kwargs):
        # do some logic here
        if request.user.is_staff:
            return view(request, *args, **kwargs)
        else:
            # if the user isn't authorised let them know
            return HttpResponseForbidden("403 Access Forbidden")

    return wrap


def no_noobs(view):
    def wrap(request, *args, **kwargs):
        # do some logic here
        if request.user.profile.state == "noob":
            # if the user isn't authorised let them know
            return HttpResponseForbidden("403 Access Forbidden")
        else:
            return view(request, *args, **kwargs)

    return wrap


def api_auth(view):
    def wrap(request, *args, **kwargs):
        secret_key = "cookiemonster"

        if request.method == "GET" and request.GET.get("secret", "wrong") == secret_key:
            return view(request, *args, **kwargs)

        elif request.method == "POST":
            details = json.loads(request.body)
            if details.get("secret", "wrong") == secret_key:
                print(True)
                return view(request, *args, **kwargs)

        # if the user isn't authorised let them know
        return HttpResponseForbidden("403 Access Forbidden")

    return wrap
