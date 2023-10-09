import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import logging
import datetime
from access.models import (
    Doors,
    Interlock,
    MemberbucksDevice,
    AccessControlledDeviceAPIKey,
)
from profile.models import Profile

logger = logging.getLogger("app")


class AccessDeviceConsumer(JsonWebsocketConsumer):
    groups = ["broadcast"]

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.device = None
        self.DeviceClass = None
        self.device_group_name = None
        self.authorised = False
        self.ping_count = 0
        self.connected_at = None
        self.last_seen = None

    def connect(self):
        logger.info("Device connected!")
        kwargs = self.scope["url_route"]["kwargs"]
        device_id = None

        if kwargs.get("door_id"):
            device_id = kwargs.get("door_id")
            self.DeviceClass = Doors

        elif kwargs.get("interlock_id"):
            device_id = kwargs.get("interlock_id")
            self.DeviceClass = Interlock

        elif kwargs.get("memberbucks_id"):
            device_id = kwargs.get("memberbucks_id")
            self.DeviceClass = MemberbucksDevice

        else:
            logger.error("Unknown device type tried to connect")
            self.close()

        defaults = {
            "name": f"New Device ({device_id})",
            "description": "New device that is yet to be setup.",
            "serial_number": device_id,
            "hidden": True,
        }

        # Get or create the device object and check it in
        device_object, created = self.DeviceClass.objects.get_or_create(
            serial_number=device_id, defaults=defaults
        )
        self.device = device_object
        self.device.checkin()

        # Set the channels group name and add the device to the group
        self.device_group_name = self.device.serial_number
        async_to_sync(self.channel_layer.group_add)(
            self.device_group_name, self.channel_name
        )

        # Set the connected_at and last_seen times
        self.connected_at = datetime.datetime.now()
        self.last_seen = self.connected_at

        if created:
            logger.warning(
                f"Created new {self.device.type} object for {self.device_id}"
            )

        if self.device.authorised:
            tags, hash = self.device.get_tags()
            print(tags, hash)
            self.accept()

        else:
            logger.warning(
                f"Device ({self.device.serial_number}) is not authorised yet and has been disconnected."
            )
            self.close()

    def disconnect(self, close_code):
        logger.info("Device disconnected!")
        logger.info("Device was connected for %s", self.last_seen - self.connected_at)
        async_to_sync(self.channel_layer.group_discard)(
            self.device_group_name, self.channel_name
        )

    def receive_json(self, content=None, **kwargs):
        """
        Receive message from WebSocket.
        """
        try:
            logger.info(
                f"Got message from {self.device.type} ({self.device.serial_number}): {json.dumps(content)}",
            )
            self.last_seen = datetime.datetime.now()
            self.device.checkin()

            if content.get("api_secret_key"):
                logger.info(
                    "Received an authorisation packet from " + self.device.serial_number
                )

                raw_api_key = content.get("api_secret_key")
                api_key_is_valid = AccessControlledDeviceAPIKey.objects.is_valid(
                    raw_api_key
                )

                if api_key_is_valid:
                    logger.info(
                        "Authorisation successful from " + self.device.serial_number
                    )
                    self.authorised = True
                    self.send_json({"authorised": True})
                    self.sync_users({})  # sync the cards down
                    self.update_device_locked_out()
                else:
                    logger.debug(
                        "Authorisation failed from " + self.device.serial_number
                    )
                    self.authorised = False
                    self.send_json({"authorised": False})
                    self.close()
                return

            elif not self.authorised:
                logger.info("Device is not authorised!")
                self.send_json({"authorised": False})
                self.close()
                return

            if content.get("command") == "ping":
                self.ping_count += 1
                self.send_json({"command": "pong"})

            elif content.get("command") == "ip_address":
                self.device.ip_address = content.get("ip_address")
                self.device.save(update_fields=["ip_address"])

            elif content.get("command") == "sync":
                self.sync_users({})

            elif content.get("command") == "log_access":
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.device.log_access(profile.user.id, success=True)

            elif content.get("command") == "log_access_denied":
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.device.log_access(profile.user.id, success=False)

            elif content.get("command") == "log_access_locked_out":
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.device.log_access(profile.user.id, success="locked_out")

            else:
                logger.info(
                    "Received an unknown packet from " + self.device.serial_number
                )

        except Exception as e:
            logger.error("Error receiving message from device: %s", e)
            logger.error(e)
            self.send_json({"command": "error"})

    def door_bump(self, event=None):
        # Handles the "door_bump" event when it's sent to us.

        logger.info("Sending door bump for {}".format(self.device.serial_number))
        print("Sending door bump for {}".format(self.device.serial_number))
        self.send_json({"command": "bump"})

    def sync_users(self, event=None):
        # Handles the "sync_users" event when it's sent to us.
        tags, tags_hash = self.device.get_tags()

        logger.info("Syncing device " + self.device.serial_number)
        self.send_json({"command": "sync", "tags": tags, "hash": tags_hash})

    def device_reboot(self, event=None):
        # Handles the "device_reboot" event when it's sent to us.
        logger.info("Rebooting device for " + self.device.serial_number)
        self.send_json({"command": "reboot"})

    def update_device_locked_out(self, event=None):
        # Handles the "update_locked_out" event when it's sent to us.
        logger.info(
            "Sending update_device_locked_out for device " + self.device.serial_number
        )
        self.update_device_object()
        self.send_json(
            {
                "command": "update_device_locked_out",
                "locked_out": self.device.locked_out,
            }
        )

    def update_device_object(self, event=None):
        self.device = self.DeviceClass.objects.get(id=self.device.id)
