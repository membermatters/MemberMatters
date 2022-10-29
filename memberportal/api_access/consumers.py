import hashlib
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from constance import config
import logging
import datetime

from access.models import Doors
from access.views import post_door_swipe_to_discord
from profile.models import Profile
from services import sms

logger = logging.getLogger("app")


def get_door_tags(door_id, return_hash=False):
    door = Doors.objects.get(pk=door_id)

    authorised_tags = list()

    for profile in Profile.objects.all():
        if door in profile.doors.all() and profile.state == "active":
            if profile.rfid and (
                profile.is_signed_into_site() or door.exempt_signin is True
            ):
                authorised_tags.append(profile.rfid)

    if return_hash:
        return hashlib.md5(str(authorised_tags).encode("utf-8")).hexdigest()

    else:
        return authorised_tags


class AccessDoorConsumer(JsonWebsocketConsumer):
    groups = ["broadcast"]

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.door_id = None
        self.door_group_name = None
        self.authorised = False
        self.ping_count = 0
        self.connected_at = None
        self.last_seen = None
        self.door = None

    def connect(self):
        logger.info("Door connected!")

        self.door_id = self.scope["url_route"]["kwargs"]["door_id"]
        self.door_group_name = "door_" + self.door_id
        async_to_sync(self.channel_layer.group_add)(
            self.door_group_name, self.channel_name
        )

        self.connected_at = datetime.datetime.now()
        self.last_seen = self.connected_at
        self.door = Doors.objects.get(serial_number=self.door_id)
        self.door.checkin()

        # if we got a door object, then accept it
        if self.door:
            self.accept()
            return

        self.close()

    def disconnect(self, close_code):
        logger.info("Door disconnected!")
        logger.info("Door was connected for %s", self.last_seen - self.connected_at)
        async_to_sync(self.channel_layer.group_discard)(
            self.door_group_name, self.channel_name
        )

    def receive_json(self, content=None, **kwargs):
        """
        Receive message from WebSocket.
        """
        try:
            logger.info("Got message from door (%s): %s", self.door.id, content)
            self.last_seen = datetime.datetime.now()
            self.door.checkin()

            if content.get("api_secret_key"):
                logger.info("Received an authorisation packet from " + self.door_id)
                if content.get("api_secret_key") == config.API_SECRET_KEY:
                    logger.info("Authorisation successful from " + self.door_id)
                    self.authorised = True
                    self.send_json({"authorised": True})
                    self.sync_users({})  # sync the cards down
                else:
                    logger.debug("Authorisation failed from " + self.door_id)
                    self.authorised = False
                    self.send_json({"authorised": False})
                return

            elif not self.authorised:
                logger.info("Device is not authorised!")
                self.send_json({"authorised": False})
                return

            if content.get("command") == "ping":
                self.ping_count += 1
                self.send_json({"command": "pong"})

            elif content.get("command") == "ip_address":
                self.door.ip_address = content.get("ip_address")
                self.door.save(update_fields=["ip_address"])

            elif content.get("command") == "sync":
                self.sync_users({})

            elif content.get("command") == "log_access":
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.door.log_access(profile.user.id)

                post_door_swipe_to_discord(
                    profile.get_full_name(), self.door.name, True
                )

            elif content.get("command") == "log_access_denied":
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.door.log_access(profile.user.id, success=False)

                post_door_swipe_to_discord(
                    profile.get_full_name(), self.door.name, False
                )
                sms_message = sms.SMS()
                sms_message.send_inactive_swipe_alert(profile.phone)

            else:
                logger.info("Received an unknown packet from " + self.door_id)

        except Exception as e:
            logger.error("Error receiving message from door: %s", e)
            logger.error(e)
            self.send_json({"command": "error", "error": str(e)})

    def door_bump(self, event=None):
        # Handles the "door_bump" event when it's sent to us.

        logger.info("Sending door bump for {}".format(self.door_id))
        print("Sending door bump for {}".format(self.door_id))
        self.send_json({"command": "bump"})

    def sync_users(self, event=None):
        # Handles the "sync_users" event when it's sent to us.

        tags = get_door_tags(self.door.id)
        tags_hash = hashlib.md5(str(tags).encode("utf-8")).hexdigest()

        logger.info("Syncing door " + self.door_id)
        self.send_json({"command": "sync", "tags": tags, "hash": tags_hash})

    def device_reboot(self, event=None):
        # Handles the "device_reboot" event when it's sent to us.
        logger.info("Rebooting door for " + self.door_id)
        self.send_json({"command": "reboot"})
