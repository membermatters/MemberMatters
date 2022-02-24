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
) -> object:
    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string(
        "email_without_button.html", {"email": email_vars, "config": config}
    )

    postmark = PostmarkClient(server_token=config.POSTMARK_API_KEY)
    postmark.emails.send(
        From=config.EMAIL_DEFAULT_FROM, To=email, Subject=subject, HtmlBody=email_string
    )

    log_user_event(
        user,
        "Sent email with subject: " + subject,
        "email",
        "Email content: " + message,
    )
    return True


def send_email_to_admin(
    subject: object,
    title: object,
    message: object,
):
    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string(
        "email_without_button.html", {"email": email_vars, "config": config}
    )

    postmark = PostmarkClient(server_token=config.POSTMARK_API_KEY)
    postmark.emails.send(
        From=config.EMAIL_DEFAULT_FROM,
        To=config.EMAIL_ADMIN,
        Subject=subject,
        HtmlBody=email_string,
    )
