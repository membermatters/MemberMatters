from django.apps import AppConfig


class ProfileConfig(AppConfig):
    name = "profile"

    def ready(self):
        import profile.signals
