from django.apps import AppConfig


class ApiAccessConfig(AppConfig):
    name = "api_access"

    def ready(self):
        import api_access.signals
