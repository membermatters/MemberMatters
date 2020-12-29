from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


class ForceCsrfCookieMiddleware(MiddlewareMixin):
    """
    This makes the CSRF cookie included in every page.
    """

    def process_request(self, request):
        get_token(request)
