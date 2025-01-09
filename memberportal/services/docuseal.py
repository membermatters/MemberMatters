from django.conf import settings
from constance import config
from docuseal import docuseal
import json
import logging
import requests

logger = logging.getLogger("docuseal")

docuseal.key = config.DOCUSEAL_API_KEY
docuseal.url = config.DOCUSEAL_URL
template_id = config.DOCUSEAL_TEMPLATE_ID

def create_submission_for_subscription(profile):
    try:
        data = {
                "template_id": template_id,
                "send_email": "False",
                "submitters": [
                {
                    "role": "First Party",
                    "name": profile.first_name + " " + profile.last_name,
                    "email": profile.user.email
                }]
            }
        logger.debug("Submitting to Docuseal with:\n{}".format(data))
        #res = docuseal.create_submission(data)
        # **cocks shotgun** docuseal python api is haunted
        # seriously, it's busted, this is a work around until they fix upstream.  Leaving this section with unhandled exceptions to debug wierdness
        response = requests.post(url=config.DOCUSEAL_URL+"/api/submissions",headers={"X-Auth-Token":config.DOCUSEAL_API_KEY},json=data)
        res = response.json()[0]
        logger.debug("Got response:\n{}".format(res))
    except Exception as ex:
        logger.error("Submission creation failed!\n{}".format(ex))
        raise ex

    logger.debug(
        "Created submission {} with slug {}".format(res["submission_id"], res["slug"])
    )
    profile.memberdoc_id = res["submission_id"]
    profile.save()

def get_docuseal_signed(profile):
    #state = docuseal.get_submission(profile.memberdoc_id)
    response = requets.get(url=config.DOCUSEAL_URL+"/api/submissions/"+str(profile.memberdoc_id),headers={"X-Auth-Token":config.DOCUSEAL_API_KEY})
    state = response.json()[0]
    if state.status != "completed":
        return 0
    return 1

def get_docuseal_link(profile):
    #sub = docuseal.get_submission(profile.memberdoc_id)
    response = requets.get(url=config.DOCUSEAL_URL+"/api/submissions/"+str(profile.memberdoc_id),headers={"X-Auth-Token":config.DOCUSEAL_API_KEY})
    sub = response.json()[0]
    return sub.embed_src