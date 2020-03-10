from django.http import HttpResponseForbidden, HttpResponse
import json


def login_required_401(function=None, redirect_field_name=None):
    """
    Just make sure the user is authenticated to access a certain ajax view

    Found here: https://stackoverflow.com/questions/10031001/login-required-decorator-on-ajax-views-to-return-401-instead-of-302

    Otherwise return a HttpResponse 401 - authentication required
    instead of the 302 redirect of the original Django decorator
    """
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(status=401)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


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
