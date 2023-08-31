from django.template.loader import render_to_string
from django.utils.html import escape
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

        if user:
            user.log_event(
                "Sent email with subject: " + subject,
                "email",
                "Email content: " + message,
            )
    else:
        if user:
            user.log_event(
                "Email NOT sent due to configuration issue: " + subject,
                "email",
                "Email content: " + message,
            )
    return True


def send_email_to_admin(subject: object, title: object, message: object, reply_to=None):
    return send_single_email(config.EMAIL_ADMIN, subject, title, message, reply_to)
