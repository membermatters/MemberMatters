from twilio.rest import Client
from constance import config
import json
import logging

logger = logging.getLogger("app")


class SMS:
    def __init__(self):
        self.sms_enable = config.SMS_ENABLE
        self.account_sid = config.TWILIO_ACCOUNT_SID
        self.auth_token = config.TWILIO_AUTH_TOKEN
        self.default_country_code = config.SMS_DEFAULT_COUNTRY_CODE
        self.sender_id = config.SMS_SENDER_ID
        self.sms_footer = config.SMS_FOOTER
        if self.sms_enable:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None

        try:
            self.sms_messages = json.loads(config.SMS_MESSAGES)
        except Exception as e:
            logger.error(e)
            raise e

    def _send(self, to_number="", body=""):
        """
        Send an SMS to the specified phone number with the body.
        :param to_number:
        :type to_number: string
        :param body:
        :type body: string
        :return: True or raise exception
        """
        logger.info("Attempting to send message to phone ending in " + to_number[-3:])

        if not self.sms_enable:
            logger.warning("Skipping SMS sending because it's turned off!")
            return False

        if len(body) < 3:
            raise RuntimeError("SMS body has less than 3 characters!")

        if len(to_number) < 10:
            raise RuntimeError("SMS to_number is less than 10!")

        # if the to_number does not include a country code, add our default one to the front
        if not to_number.startswith("+"):
            to_number = self.default_country_code + to_number

        if self.sms_footer:
            body = body + "\n\n" + self.sms_footer

        self.client.messages.create(body=body, from_=self.sender_id, to=to_number)

        logger.info("Sent message to phone ending in " + to_number[-3:])

        return True

    def send_inactive_swipe_alert(self, to_number):
        logger.info("Sending inactive swipe SMS.")
        message = self.sms_messages.get(
            "inactive_swipe",
            "Hi! Your swipe was just declined."
            " Please contact us if you need assistance.",
        )
        self._send(to_number, message)

    def send_locked_out_swipe_alert(self, to_number):
        logger.info("Sending locked out swipe SMS.")
        message = self.sms_messages.get(
            "locked_out_swipe",
            "Hi! Your swipe was just declined due to a temporary maintenance lockout."
            " Please contact us if you need assistance.",
        )
        self._send(to_number, message)

    def send_deactivated_access(self, to_number):
        message = self.sms_messages.get(
            "deactivated_access",
            "Hi! Your site access was just turned off. Please check your email and "
            "contact us if you need assistance.",
        )
        self._send(to_number, message)

    def send_activated_access(self, to_number):
        message = self.sms_messages.get(
            "activated_access",
            "Hi! Your site access was just turned on. Please make sure you stay up to date"
            " with our policies and rules by visiting our website.",
        )
        self._send(to_number, message)
