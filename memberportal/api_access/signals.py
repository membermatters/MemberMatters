import logging

logger = logging.getLogger("app")

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import auth
from access.models import Doors
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = auth.get_user_model()


@receiver(pre_save, sender=Doors)
def save_or_create_door(sender, instance, **kwargs):
    # disable the handler during fixture loading
    if kwargs["raw"]:
        return

    created = instance.pk is None
    door_all_members_changed = False
    door_maintenance_lockout_changed = False
    door = None

    # if we didn't just create the door check if it's properties have changed
    if not created:
        door = Doors.objects.get(pk=instance.id)
        door_all_members_changed = instance.all_members != door.all_members
        door_maintenance_lockout_changed = instance.locked_out != door.locked_out

    # if the door has all_members set, and it is new or all_members has changed, reset permissions for it
    if instance.all_members and (created or door_all_members_changed):
        # update access
        members = User.objects.all()

        for member in members:
            member.profile.doors.add(door)
            member.profile.save()

        # once we're done, sync changes to the door
        door.sync()

    # if the door has all_members unset, and it is new or all_members has changed, unset permissions for it
    elif instance.all_members is False and door_all_members_changed:
        # update access
        members = User.objects.all()
        door = Doors.objects.get(pk=instance.id)

        for member in members:
            member.profile.doors.remove(door)
            member.profile.save()

        # once we're done, sync changes to the door
        door.sync()

    if door_maintenance_lockout_changed:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "door_" + door.serial_number, {"type": "update_door_locked_out"}
        )

    # update the door object on the websocket consumer
    if door is not None:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "door_" + door.serial_number, {"type": "update_door_device"}
        )
