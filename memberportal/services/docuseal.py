from django.conf import settings
from constance import config
from docuseal import docuseal
from profile.models import Profile, User
import json
import logging
from time import now

logger = logging.getLogger("docuseal")

docuseal.key = config.DOCUSEAL_API_KEY
docuseal.url = config.DOCUSEAL_URL
try:
    template_ids = json.load(config.DOCUSEAL_TEMPLATE_IDS)
except:
    logger.error("Failed to parse template_id list")


def create_submissions_for_subscription(profile):
    for doc in template_ids:
        try:
            res = docuseal.create_submission(
                {
                    "template_id": doc,
                    "send_email": False,
                    "submitters": [{"role": "Applicant", "email": profile.user.email}],
                }
            )
        except docuseal.ApiError:
            logger.error("Submission creation failed!")
            continue

        logger.debug(
            "Created submission {} with slug {}".format(res.submission_id, res.slug)
        )
