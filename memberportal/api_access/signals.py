import logging

logger = logging.getLogger("app")

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import auth
from access.models import AccessControlledDevice, Doors, Interlock, MemberbucksDevice
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = auth.get_user_model()


@receiver(post_save, sender=AccessControlledDevice)
def save_or_create_access_controlled_device(sender, instance, created, **kwargs):
    # disable the handler during fixture loading
    if kwargs["raw"]:
        return

    all_members_changed = False
    maintenance_lockout_changed = False
    device = None
    if instance.type == "door":
        device = Doors.objects.get(pk=instance.id)
    elif instance.type == "interlock":
        device = Interlock.objects.get(pk=instance.id)
    elif instance.type == "memberbucks":
        device = MemberbucksDevice.objects.get(pk=instance.id)

    # if we didn't just create the device check if it's properties have changed
    if not created:
        all_members_changed = instance.all_members != device.all_members
        maintenance_lockout_changed = instance.locked_out != device.locked_out

    # if the device has all_members set, and it is new or all_members has changed, reset permissions for it
    if instance.all_members is True and (created or all_members_changed):
        # update access
        members = User.objects.all()

        for member in members:
            if device.type == "door":
                member.profile.doors.add(device)
            elif device.type == "interlock":
                member.profile.interlocks.add(device)
            member.profile.save()

        # once we're done, sync changes to the device
        device.sync()

    # if the device has all_members unset, and all_members has changed, unset permissions for it
    elif instance.all_members is False and all_members_changed:
        # update access
        members = User.objects.all()

        for member in members:
            if device.type == "door":
                member.profile.doors.remove(device)
            elif device.type == "interlock":
                member.profile.interlocks.remove(device)
            member.profile.save()

        # once we're done, sync changes to the device
        device.sync()

    if maintenance_lockout_changed:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            device.serial_number, {"type": "update_device_locked_out"}
        )

    # update the door object on the websocket consumer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        device.serial_number, {"type": "update_device_object"}
    )
