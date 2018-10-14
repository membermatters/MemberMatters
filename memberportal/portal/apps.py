from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "portal"
    label = "portal"
    verbose_name = "Portal"

    def ready(self):
        # importing signal handlers
        import portal.signals
