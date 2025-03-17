from django.conf import settings
from constance import config
import json
import logging
import requests

logger = logging.getLogger("docuseal")


def create_submission_for_subscription(profile):
    try:
        data = {
            "template_id": config.DOCUSEAL_TEMPLATE_ID,
            ### Customize the following to fit your instance deployment and template
            "send_email": "False",
            "completed_redirect_url": config.SITE_URL,
            "submitters": [
                {
                    "role": "First Party",
                    "name": profile.first_name + " " + profile.last_name,
                    "email": profile.user.email,
                    "fields": [
                        {
                            "name": "name",
                            "default_value": profile.first_name
                            + " "
                            + profile.last_name,
                        }
                    ],
                }
            ],
        }
        logger.debug("Submitting to Docuseal with:\n{}".format(data))

        # there seem to be inconsistencies between the docuseal package's expected backend api and what is implemented by the docuseal
        # application (at least with the opensource option as of writing).  Opting to use requests package as a workaround.
        response = requests.post(
            url=config.DOCUSEAL_URL + "/api/submissions",
            headers={"X-Auth-Token": config.DOCUSEAL_API_KEY},
            json=data,
        )
        res = response.json()[0]
        logger.debug("Got response:\n{}".format(res))
    except Exception as ex:
        # holy overly-broad exception handlers batman!
        logger.error("Submission creation failed!\n{}".format(ex))
        raise ex

    logger.debug(
        "Created submission {} with slug {}".format(res["submission_id"], res["slug"])
    )
    profile.memberdoc_id = res["submission_id"]
    profile.memberdoc_url = res["embed_src"]
    profile.save()


def get_docuseal_submission(profile):
    if profile.memberdoc_id is None:
        return None

    logger.debug(
        "Requesting {}".format("/api/submissions/" + str(profile.memberdoc_id))
    )
    try:
        response = requests.get(
            url=config.DOCUSEAL_URL + "/api/submissions/" + str(profile.memberdoc_id),
            headers={"X-Auth-Token": config.DOCUSEAL_API_KEY},
        )
        logger.debug("Got response:\n{}".format(response.json()))
        state = response.json()
    except Exception as ex:
        # holy overly-broad exception handlers batman!
        logger.error("Finding submission state failed!\n{}".format(ex))
        raise ex

    return state
