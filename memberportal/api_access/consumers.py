import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from constance import config
import logging
import datetime
from access.models import Doors

logger = logging.getLogger()


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
        async_to_sync(self.channel_layer.group_add)(self.door_group_name, self.channel_name)

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
        async_to_sync(self.channel_layer.group_discard)(self.door_group_name, self.channel_name)

    def receive_json(self, content=None, **kwargs):
        """
        Receive message from WebSocket.
        """
        try:
            logger.debug("Got message from door: %s", content)
            self.last_seen = datetime.datetime.now()
            self.door.checkin()

            if content.get("api_secret_key"):
                logger.info("Received an authorisation packet from " + self.door_id)
                if content.get("api_secret_key") == config.API_SECRET_KEY:
                    logger.debug("Authorisation successful!")
                    self.authorised = True
                    self.send_json({"authorised": True})
                else:
                    logger.debug("Authorisation failed!")
                    self.authorised = False
                    self.send_json({"authorised": False})
                return

            elif not self.authorised:
                logger.debug("Device is not authorised!")
                self.send_json({"authorised": False})
                return

            if content.get("command") == "ping":
                logger.debug("Received a ping packet from " + self.door_id)
                self.ping_count += 1
                self.send_json({"command": "pong"})

            if content.get("command") == "ip_address":
                logger.debug("Received an IP address packet from " + self.door_id)
                self.door.ip_address = content.get("ip_address")
                self.door.save()

        except Exception as e:
            logger.error("Error receiving message from door: %s", e)
            logger.error(e)
            self.send_json({"command": "error", "error": str(e)})

    def door_bump(self, event):
        # Handles the "door.bump" event when it's sent to us.
        self.send_json({"command": "bump"})
