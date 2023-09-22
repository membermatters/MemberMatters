from django.template.loader import render_to_string
from django.utils.html import escape
from constance import config
from postmarker.core import PostmarkClient, ClientError
import logging
import json

logger = logging.getLogger("app")


def send_single_email(
    to_email: object,
    subject: object,
    template_vars: object,
    template_name,
    reply_to=None,
    user: object | None = None,
) -> object:
    # TODO: move to celery

    template_to_use = template_name if template_name else "email_without_button.html"
    logger.debug("Using email template: " + template_to_use)
    logger.debug("Using template vars: " + json.dumps(template_vars))

    if template_vars.get("message"):
        template_vars["message"] = escape(template_vars["message"]).replace(
            "~br~", "<br>"
        )

    email_string = render_to_string(
        template_to_use, {"email": template_vars, "config": config}
    )

    if config.POSTMARK_API_KEY:
        postmark = PostmarkClient(server_token=config.POSTMARK_API_KEY)
        try:
            postmark.emails.send(
                From=config.EMAIL_DEFAULT_FROM,
                To=to_email,
                Subject=subject,
                HtmlBody=email_string,
                ReplyTo=reply_to or config.EMAIL_DEFAULT_FROM,
            )
        except ClientError as e:
            code = e.error_code

            if code == 406:
                if user:
                    logger.warning(
                        f"Email NOT sent because recipient is INACTIVE in postmark"
                    )
                    user.log_event(
                        "Email NOT sent because recipient is INACTIVE in postmark: ",
                        "email",
                        "Email content: " + json.dumps(template_vars),
                    )
            else:
                logger.error("Error sending email: " + str(e))
                raise e

        if user:
            logger.info("Email sent to " + to_email + " with subject: " + subject)
            user.log_event(
                "Sent email with subject: " + subject,
                "email",
                "Email content: " + template_vars.get("message"),
            )
    else:
        logger.warning("No postmark API key set, not sending email")
        if user:
            user.log_event(
                "Email NOT sent due to configuration issue: " + subject,
                "email",
                "Email content: " + template_vars.get("message"),
            )
    return True


def send_email_to_admin(
    subject: object,
    template_vars: object,
    template_name,
    reply_to=None,
    user: object | None = None,
) -> object:
    return send_single_email(
        config.EMAIL_ADMIN,
        subject,
        template_vars,
        template_name=template_name,
        reply_to=reply_to,
        user=user,
    )
