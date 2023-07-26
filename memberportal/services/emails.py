from django.template.loader import render_to_string
from django.utils.html import escape
from membermatters.helpers import log_user_event
from constance import config
from postmarker.core import PostmarkClient


def send_single_email(
    user: object,
    email: object,
    subject: object,
    title: object,
    message: object,
    reply_to=None,
) -> object:
    # TODO: move to celery

    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string(
        "email_without_button.html", {"email": email_vars, "config": config}
    )

    if config.POSTMARK_API_KEY:
        postmark = PostmarkClient(server_token=config.POSTMARK_API_KEY)
        postmark.emails.send(
            From=config.EMAIL_DEFAULT_FROM,
            To=email,
            Subject=subject,
            HtmlBody=email_string,
            ReplyTo=reply_to or config.EMAIL_DEFAULT_FROM,
        )

        log_user_event(
            user,
            "Sent email with subject: " + subject,
            "email",
            "Email content: " + message,
        )
    else:
        log_user_event(
            self,
            "Email NOT sent due to configuration issue: " + subject,
            "email",
            "Email content: " + message,
        )
    return True


def send_email_to_admin(subject: object, title: object, message: object, reply_to=None):
    # TODO: move to celery

    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string(
        "email_without_button.html", {"email": email_vars, "config": config}
    )

    if config.POSTMARK_API_KEY:
        postmark = PostmarkClient(server_token=config.POSTMARK_API_KEY)
        postmark.emails.send(
            From=config.EMAIL_DEFAULT_FROM,
            To=config.EMAIL_ADMIN,
            Subject=subject,
            HtmlBody=email_string,
            ReplyTo=reply_to or config.EMAIL_DEFAULT_FROM,
        )
    else:
        print("Email NOT sent due to configuration issue: " + subject)
