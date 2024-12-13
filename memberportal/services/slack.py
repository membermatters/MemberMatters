import requests
from django.conf import settings
from constance import config
import logging

logger = logging.getLogger("slack")

def post_door_swipe_to_slack(name, door, status):
    if config.ENABLE_SLACK_INTEGRATION and config.SLACK_DOOR_WEBHOOK:
        logger.debug("Posting door swipe to Slack!")

        url = config.SLACK_DOOR_WEBHOOK

        json_message = {}

        if status is True:
            json_message.append(
                {
                    "text": ":unlock: {} just **successfully** swiped at {}.".format(
                        name, door
                    )
                }
            )

        elif status == "not_signed_in":
            json_message.append(
                {
                    "text": ":x: {} swiped at {} but was rejected because they "
                    "aren't signed into site.".format(name, door)
                }
            )

        elif status == "locked_out":
            json_message.append(
                {
                    "text": ":x: {} tried to access the {} but it is currently under a "
                    "maintenance lockout.".format(name, door)
                }
            )

        else:
            json_message.append(
                {
                    "text": f":x: {name} just swiped at {door} but was **rejected**. You "
                    f"can check your"
                    f" access [here]({config.SITE_URL}/account/access/)."
                }
            )

        try:
            requests.post(url, json=json_message, timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return True

    return True

def post_interlock_swipe_to_slack(name, interlock, type, time=None):
    if config.ENABLE_SLACK_INTEGRATION and config.SLACK_INTERLOCK_WEBHOOK:
        logger.debug("Posting interlock swipe to Slack!")
        url = config.SLACK_INTERLOCK_WEBHOOK

        json_message = {}

        if type == "activated":
            json_message.append(
                {
                    "text": ":unlock: {} just **activated** the {}.".format(
                        name, interlock
                    )
                }
            )

        elif type == "rejected":
            json_message.append(
                {
                    "text": f"{name} tried to activate the {interlock} but was "
                    f"**rejected**. You can check your"
                    f" access [here]({config.SITE_URL}/account/access/)."
                }
            )

        elif type == "left_on":
            json_message.append(
                {
                    "text": ":lock: The {} was just turned off by the access system because it timed out (last used by {}). It was on for {}.".format(
                        interlock, name, time
                    )
                }
            )

        elif type == "deactivated":
            json_message.append(
                {
                    "text": ":lock: {} just **deactivated** the {}. It was on for "
                    "{}.".format(name, interlock, time)
                }
            )

        elif type == "locked_out":
            json_message.append(
                {
                    "text": "{} tried to access the {} but it is currently under a "
                    "maintenance lockout".format(name, interlock)
                }
            )

        elif type == "not_signed_in":
            json_message.append(
                {
                    "text": ":lock: {} swiped at {} but was rejected because they "
                    "aren't signed into site.".format(name, interlock)
                }
            )

        try:
            requests.post(url, json=json_message, timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return True

    else:
        return True

def post_kiosk_swipe_to_slack(name, sign_in):
    if config.ENABLE_SLACK_INTEGRATION and config.SLACK_DOOR_WEBHOOK:
        logger.debug("Posting kiosk swipe to Slack!")
        url = config.DISCORD_DOOR_WEBHOOK

        json_message = {}

        json_message.append(
            {
                "text": f":book: {name} just signed {'in' if sign_in else 'out'} at a kiosk."
            }
        )

        try:
            requests.post(url, json=json_message, timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return True

    return True