import requests
from django.conf import settings
from constance import config


def post_door_swipe_to_discord(name, door, status):
    if config.ENABLE_DISCORD_INTEGRATION:
        url = config.DISCORD_DOOR_WEBHOOK

        json_message = {"description": "", "embeds": []}

        if status is True:
            json_message["embeds"].append(
                {
                    "description": ":unlock: {} just **successfully** swiped at {} door.".format(
                        name, door
                    ),
                    "color": 5025616,
                }
            )

        elif status == "not_signed_in":
            json_message["embeds"].append(
                {
                    "description": ":lock: {} swiped at {} door but was rejected because they "
                    "aren't signed into site.".format(name, door),
                    "color": 5025616,
                }
            )

        else:
            json_message["embeds"].append(
                {
                    "description": f"{name} just swiped at {door} door but was **rejected**. You "
                    f"can check your"
                    f" access [here]({config.SITE_URL}/profile/access/view/).",
                    "color": 16007990,
                }
            )

        try:
            requests.post(url, json=json_message, timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return True

    return True


def post_interlock_swipe_to_discord(name, interlock, type, time=None):
    if config.ENABLE_DISCORD_INTEGRATION:
        url = config.DISCORD_INTERLOCK_WEBHOOK

        json_message = {"description": "", "embeds": []}

        if type == "activated":
            json_message["embeds"].append(
                {
                    "description": ":unlock: {} just **activated** the {}.".format(
                        name, interlock
                    ),
                    "color": 5025616,
                }
            )

        elif type == "rejected":
            json_message["embeds"].append(
                {
                    "description": f"{name} tried to activate the {interlock} but was "
                    f"**rejected**. You can check your"
                    f" access [here]({config.SITE_URL}/profile/access/view/).",
                    "color": 16007990,
                }
            )

        elif type == "left_on":
            json_message["embeds"].append(
                {
                    "description": ":lock: The {} was just turned off by the access system because it timed out (last used by {}). It was on for {}.".format(
                        interlock, name, time
                    ),
                    "color": 16750592,
                }
            )

        elif type == "deactivated":
            json_message["embeds"].append(
                {
                    "description": ":lock: {} just **deactivated** the {}. It was on for "
                    "{}.".format(name, interlock, time),
                    "color": 5025616,
                }
            )

        elif type == "maintenance_lock_out":
            json_message["embeds"].append(
                {
                    "description": "{} tried to access the {} but it is currently under a "
                    "maintenance lockout".format(name, interlock),
                    "color": 16007990,
                }
            )

        elif type == "not_signed_in":
            json_message["embeds"].append(
                {
                    "description": ":lock: {} swiped at {} but was rejected because they "
                    "aren't signed into site.".format(name, interlock),
                    "color": 5025616,
                }
            )

        try:
            requests.post(url, json=json_message, timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return True

    else:
        return True
