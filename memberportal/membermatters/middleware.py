from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token
from sentry_sdk import set_user


class ForceCsrfCookieMiddleware(MiddlewareMixin):
    """
    This makes the CSRF cookie included in every page.
    """

    def process_request(self, request):
        get_token(request)


class Sentry(MiddlewareMixin):
    """
    Adds current user to sentry context.
    """

    def process_request(self, request):
        if request.user and request.user.is_authenticated:
            set_user(
                {
                    "email": request.user.email,
                    "Screen Name": request.user.profile.screen_name,
                }
            )
