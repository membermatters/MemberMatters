import logging

logger = logging.getLogger("profile")

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import auth
from .models import Profile

User = auth.get_user_model()


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    # disable the handler during fixture loading
    if kwargs["raw"]:
        return

    door_access_changed = False
    interlock_access_changed = False
    profile = Profile.objects.get(pk=instance.id)

    # if we didn't just create the profile check if the doors or interlocks properties have changed
    if not created:
        # TODO: check every single door and interlock for changes
        door_access_changed = profile.doors != instance.doors
        interlock_access_changed = profile.interlocks != instance.interlocks

    if profile.state != instance.state:
        # If our profile state changed, then sync everything.
        door_access_changed = True
        interlock_access_changed = True

    if door_access_changed:
        for door in profile.doors:
            door.sync()

    if interlock_access_changed:
        for interlock in profile.interlocks:
            interlock.sync()
