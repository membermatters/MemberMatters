from django.conf import settings
from constance import config
from docuseal import docuseal
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
                    "fields": [{
                        "name": "name",
                        "default_value": profile.first_name + " " + profile.last_name
                    }]
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
    profile.memberdoc_url = res["embed_src"]
    profile.save()

def get_docuseal_state(profile):
    #state = docuseal.get_submission(profile.memberdoc_id)
    if profile.memberdoc_id is None:
        return 0
    
    logger.debug("Requesting {}".format("/api/submissions/"+str(profile.memberdoc_id)))
    response = requests.get(url=config.DOCUSEAL_URL+"/api/submissions/"+str(profile.memberdoc_id),headers={"X-Auth-Token":config.DOCUSEAL_API_KEY})
    logger.debug("Got response:\n{}".format(response.json()))
    state = response.json()
    return state["status"]

def get_docuseal_link(profile):
    #sub = docuseal.get_submission(profile.memberdoc_id)
    if profile.memberdoc_id is None:
        return 0
    
    logger.debug("Requesting {}".format("/api/submissions/"+str(profile.memberdoc_id)))
    response = requests.get(url=config.DOCUSEAL_URL+"/api/submissions/"+str(profile.memberdoc_id),headers={"X-Auth-Token":config.DOCUSEAL_API_KEY})
    logger.debug("Got response:\n{}".format(response.json))
    if response.status_code == 200:
        sub = response.json()
        return sub.embed_src
    else:
        return ""