import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import logging
import datetime
from access.models import (
    Doors,
    Interlock,
    InterlockLog,
    MemberbucksDevice,
    AccessControlledDeviceAPIKey,
)
from memberbucks.models import (
    MemberBucks,
    MemberbucksProductPurchaseLog,
    MemberbucksProduct,
)
from profile.models import Profile, User
from constance import config
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

logger = logging.getLogger("access")


class AccessDeviceConsumer(JsonWebsocketConsumer):
    groups = ["broadcast"]

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.device: MemberbucksDevice | Doors | Interlock | None = None
        self.DeviceClass: MemberbucksDevice | Doors | Interlock | None = None
        self.device_group_name: str | None = None
        self.authorised: bool = False
        self.ping_count: int = 0
        self.connected_at: datetime.datetime | None = None
        self.last_seen: datetime.datetime | None = None

    def connect(self):
        logger.info("Device connected!")
        kwargs = self.scope["url_route"]["kwargs"]
        device_id = kwargs.get("device_id")

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
                f"Commissioned new {self.device.type} device for {self.device.serial_number}"
            )

        if self.device.authorised:
            self.accept()

        else:
            logger.warning(
                f"Device ({self.device.serial_number}) is not authorised yet and has been disconnected."
            )
            self.accept()
            self.close()

    def disconnect(self, close_code):
        logger.info("Device disconnected!")
        logger.info("Device was connected for %s", self.last_seen - self.connected_at)
        self.device.log_disconnected()
        async_to_sync(self.channel_layer.group_discard)(
            self.device_group_name, self.channel_name
        )

    def receive_json(self, content=None, **kwargs):
        """
        Receive message from WebSocket.
        """
        try:
            logger.debug(
                f"Got message from {self.device.type} ({self.device.serial_number}): {json.dumps(content)}",
            )
            self.last_seen = datetime.datetime.now()
            self.device.checkin()

            if content.get("command") == "authenticate":
                logger.debug(
                    "Received an authorisation packet from " + self.device.serial_number
                )

                raw_api_key = content.get("secret_key")
                api_key_is_valid = AccessControlledDeviceAPIKey.objects.is_valid(
                    raw_api_key
                )

                if api_key_is_valid and self.device.authorised:
                    logger.info(
                        "Authorisation successful from " + self.device.serial_number
                    )
                    self.authorised = True
                    self.send_json({"authorised": True})
                    self.device.log_authenticated()
                    self.sync_users({})  # sync the cards down
                    self.update_device_locked_out()

                    if self.device.type == "interlock":
                        self.device.session_end_all("new_connection")
                else:
                    logger.debug(
                        "Authorisation failed from " + self.device.serial_number
                    )
                    self.authorised = False
                    self.send_json({"authorised": False})
                    self.close()
                return

            elif not self.authorised:
                logger.debug("Device is not authorised!")
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

            else:
                if not self.handle_other_packet(content):
                    # if the packet wasn't handled by the subclass, log it
                    logger.warning(
                        f'Received an unknown packet ({content.get("command")}) from {self.device.serial_number}'
                    )

        except Exception as e:
            logger.error("Error receiving message from device: %s", e)
            self.send_json({"command": "error"})
            raise e

    def handle_other_packet(self, content):
        raise NotImplementedError(
            "handle_other_packet() must be implemented by subclass"
        )

    def send_ack(self, command, success=True):
        self.send_json(
            {
                "command": command,
                "success": success,
            }
        )

    def check_authorised(self):
        if self.authorised:
            return True
        else:
            logger.warning(
                f"Device {self.device.serial_number} is not authorised but data was sent to it!"
            )
            raise RuntimeError(
                f"Device {self.device.serial_number} is not authorised but data was sent to it!"
            )

    def sync_users(self, event=None):
        self.check_authorised()

        if self.device.type != "door":
            logger.debug(
                "Skipping device sync for device that is not a door ({}).".format(
                    self.device.name
                )
            )
            return True

        # Handles the "sync_users" event when it's sent to us.
        tags, tags_hash = self.device.get_tags()

        logger.info("Syncing device " + self.device.serial_number)
        self.send_json({"command": "sync", "tags": tags, "hash": tags_hash})

    def device_reboot(self, event=None):
        # Handles the "device_reboot" event when it's sent to us.
        logger.info("Rebooting device for " + self.device.serial_number)
        self.send_json({"command": "reboot"})

    def device_lock(self, event=None):
        # Handles the "device_lock" event when it's sent to us.
        logger.info("Locking device for " + self.device.serial_number)
        self.send_json({"command": "lock"})

    def device_unlock(self, event=None):
        # Handles the "device_unlock" event when it's sent to us.
        logger.info("Unlocking device for " + self.device.serial_number)
        self.send_json({"command": "unlock"})

    def update_device_locked_out(self, event=None):
        self.check_authorised()

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
        self.device = self.DeviceClass.objects.get(
            serial_number=self.device.serial_number
        )


class DoorConsumer(AccessDeviceConsumer):
    type = "door"

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.DeviceClass = Doors

    def handle_other_packet(self, content):
        if content.get("command") == "log_access":
            # handle the case where the profile doesn't exist
            try:
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.device.log_access(profile.user.id, success=True)
                self.send_ack("log_access")
                return True
            except Profile.DoesNotExist:
                self.send_ack("log_access")
                logger.warning(
                    f"Tried to process log_access but profile with card ID {card_id} does not exist."
                )
                return True

        elif content.get("command") == "log_access_denied":
            # handle the case where the profile doesn't exist
            try:
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.device.log_access(profile.user.id, success=False)
                self.send_ack("log_access_denied")
                self.sync_users()
                return True
            except Profile.DoesNotExist:
                self.send_ack("log_access_denied")
                logger.warning(
                    f"Tried to process log_access_denied but profile with card ID {card_id} does not exist."
                )
                return True

        elif content.get("command") == "log_access_locked_out":
            # handle the case where the profile doesn't exist
            try:
                card_id = content.get("card_id")
                profile = Profile.objects.get(rfid=card_id)
                self.device.log_access(profile.user.id, success="locked_out")
                self.send_ack("log_access_locked_out")
                return True
            except Profile.DoesNotExist:
                self.send_ack("log_access_locked_out")
                logger.warning(
                    f"Tried to process log_access_locked_out but profile with card ID {card_id} does not exist."
                )
                return True

        else:
            return False

    def door_bump(self, event=None):
        self.check_authorised()

        # Handles the "door_bump" event when it's sent to us.

        logger.info("Sending door bump for {}".format(self.device.serial_number))
        self.send_json({"command": "bump"})


class InterlockConsumer(AccessDeviceConsumer):
    type = "interlock"
    session = None

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.DeviceClass = Interlock

    def handle_other_packet(self, content):
        if content.get("command") == "interlock_session_start":
            card_id = content.get("card_id")
            profile = Profile.objects.filter(rfid=card_id).first()
            if profile:
                profile.update_last_seen()
            reason = "rejected"

            if profile:
                profile.update_last_seen()
                if profile.state == "active":
                    if self.device.locked_out:
                        reason = "maintenance_lock_out"

                    else:
                        allowed_interlocks = profile.interlocks.all()

                        # user has access to this interlock
                        if allowed_interlocks and self.device in allowed_interlocks:
                            if (
                                profile.is_signed_into_site()
                                or self.device.exempt_signin is True
                                or config.ENABLE_PORTAL_SITE_SIGN_IN is False
                            ):
                                # TODO: check they have enough memberbucks balance
                                self.device.log_access(profile.user, type="activated")
                                self.session = self.device.session_start(profile.user)
                                self.send_json(
                                    {
                                        "command": "interlock_session_start",
                                        "session_id": str(self.session.id),
                                    }
                                )

                                return True
                            else:
                                # user is not signed into the site
                                reason = "not_signed_in"

                # if they are inactive or don't have access
                self.device.log_access(profile.user if profile else None, reason)

            self.send_json(
                {
                    "command": "interlock_session_rejected",
                    "reason": reason,
                }
            )

            return True

        elif content.get("command") == "interlock_session_update":
            session_id = content.get("session_id")
            session_kwh = content.get("session_kwh")

            session = InterlockLog.objects.get(id=session_id)

            if session.date_ended:
                self.send_json(
                    {
                        "command": "interlock_session_update",
                        "success": False,
                        "reason": "session_already_ended",
                    }
                )
                return True

            if session.session_update(session_kwh):
                self.send_json(
                    {
                        "command": "interlock_session_update",
                        "success": True,
                    }
                )

            else:
                self.send_json(
                    {
                        "command": "interlock_session_update",
                        "success": False,
                    }
                )

            return True

        elif content.get("command") == "interlock_session_end":
            card_id = content.get("card_id")
            session_id = content.get("session_id")
            session_kwh = content.get("session_kwh")

            profile = (
                Profile.objects.filter(rfid=card_id).select_related("user").first()
            )
            user = profile.user if profile else None
            session = InterlockLog.objects.get(id=session_id)

            if session.date_ended:
                self.send_json(
                    {
                        "command": "interlock_session_end",
                        "success": False,
                        "reason": "session_already_ended",
                    }
                )
                return True

            if session.session_end(user, session_kwh):
                self.send_json(
                    {
                        "command": "interlock_session_end",
                        "success": True,
                    }
                )

            else:
                self.send_json(
                    {
                        "command": "interlock_session_end",
                        "success": False,
                    }
                )

            return True

        else:
            return False


class MemberbucksConsumer(AccessDeviceConsumer):
    type = "memberbucks"

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.DeviceClass = MemberbucksDevice

    def handle_other_packet(self, content):
        if content.get("command") == "balance":
            card_id = content.get("card_id")

            if card_id is None:
                self.send_json(
                    {
                        "command": "balance",
                        "reason": "invalid_card_id",
                        "success": False,
                    }
                )
                return True

            try:
                profile = Profile.objects.get(rfid=card_id)
                self.send_json(
                    {
                        "command": "balance",
                        "balance": int(profile.memberbucks_balance * 100),
                        "success": True,
                    }
                )
                return True

            except ObjectDoesNotExist:
                self.send_json(
                    {
                        "command": "balance",
                        "reason": "invalid_card_id",
                        "success": False,
                    }
                )
                logger.warning(
                    f"Tried to process balance but profile with card ID {card_id} does not exist."
                )
                return True

        if content.get("command") == "debit" or content.get("command") == "credit":
            card_id = content.get("card_id")
            product_external_id = content.get("product_external_id")
            amount = int(content.get("amount") or 0)
            description = content.get("description", f"{self.device.name} purchase.")
            command = content.get("command")

            if card_id is None:
                self.send_json(
                    {
                        "command": command,
                        "reason": "invalid_card_id",
                        "success": False,
                    }
                )
                return True

            # stops us accidentally accepting a negative value
            if amount <= 0:
                self.send_json(
                    {
                        "command": command,
                        "reason": "invalid_amount",
                        "success": False,
                    }
                )
                return True

            try:
                profile = Profile.objects.get(rfid=card_id)

            except ObjectDoesNotExist:
                self.send_json(
                    {
                        "command": command,
                        "reason": "invalid_card_id",
                        "success": False,
                    }
                )
                logger.warning(
                    f"Tried to process {command} because profile with card ID {card_id} does not exist."
                )
                return True

            if command == "debit" and profile.memberbucks_balance < amount:
                # TODO: auto top up feature

                profile.user.log_event(
                    f"Not enough funds to debit ${amount} from {config.MEMBERBUCKS_NAME} account by {self.device.name}.",
                    "memberbucks",
                )

                subject = (
                    f"Failed to make a ${amount} {config.MEMBERBUCKS_NAME} purchase."
                )
                message = f"We just tried to debit ${amount} from your {config.MEMBERBUCKS_NAME} balance but were not "
                f"successful. You currently have ${profile.memberbucks_balance}. If this wasn't you, please let us know "
                f"immediately."

                User.objects.get(profile=profile).email_notification(subject, message)

                self.send_json(
                    {
                        "command": "debit",
                        "success": False,
                        "reason": "insufficient_funds",
                        "balance": int(profile.memberbucks_balance * 100),
                    }
                )
                return True

            time_dif = (
                timezone.now() - profile.last_memberbucks_purchase
            ).total_seconds()

            # We have a hard rate limit of one transaction every 3 seconds at most
            if time_dif > 3:
                amount = float(amount) if command == "credit" else float(amount * -1)

                if product_external_id:
                    try:
                        product = MemberbucksProduct.objects.get(
                            external_id=product_external_id
                        )
                    except ObjectDoesNotExist:
                        self.send_json(
                            {
                                "command": command,
                                "reason": "invalid_product_external_id",
                                "success": False,
                            }
                        )
                        logger.warning(
                            f"Tried to process {command} but product with external_id {product_external_id} does not exist."
                        )
                        return True
                    purchase_log = MemberbucksProductPurchaseLog()
                    purchase_log.product = product
                    purchase_log.user = profile.user
                    purchase_log.cost_price = product.cost_price
                    purchase_log.price = amount
                    purchase_log.memberbucks_device = self.device
                    purchase_log.save()

                    description = f"{profile.get_full_name()} ({profile.screen_name}) {product.name} purchased from {self.device.name} ({product.external_id_name}) for {amount}."

                transaction = MemberBucks()
                transaction.amount = amount
                transaction.user = profile.user
                transaction.description = description
                transaction.transaction_type = "card"
                transaction.save()

                profile.last_memberbucks_purchase = timezone.now()
                profile.save()
                profile.refresh_from_db()

                subject = (
                    f"You just made a ${amount} {config.MEMBERBUCKS_NAME} purchase."
                )
                message = f"Description: {transaction.description}. Balance Remaining: "
                f"${profile.memberbucks_balance}. If this wasn't you, or you believe there "
                f"has been an error, please let us know."

                User.objects.get(profile=profile).email_notification(subject, message)

                profile.user.log_event(
                    f"{command}ed ${amount} from {config.MEMBERBUCKS_NAME} account.",
                    "memberbucks",
                )

                self.send_json(
                    {
                        "command": command,
                        "balance": int(profile.memberbucks_balance * 100),
                        "amount": int(transaction.amount * 100),
                        "success": True,
                    }
                )
                return True

            else:
                self.send_json(
                    {
                        "command": "rate_limited",
                    }
                )

        else:
            return False
