from django.template.loader import render_to_string
from django.utils.html import escape
from constance import config
from postmarker.core import PostmarkClient


def send_single_email(
    to_email: object,
    subject: object,
    template_vars: object,
    template_name="email_without_button.html",
    reply_to=None,
    user: object | None = None,
) -> object:
    # TODO: move to celery

    if template_vars.get("message"):
        template_vars["message"] = escape(template_vars["message"]).replace(
            "~br~", "<br>"
        )

    email_string = render_to_string(
        template_name, {"email": template_vars, "config": config}
    )

    if config.POSTMARK_API_KEY:
        postmark = PostmarkClient(server_token=config.POSTMARK_API_KEY)
        postmark.emails.send(
            From=config.EMAIL_DEFAULT_FROM,
            To=to_email,
            Subject=subject,
            HtmlBody=email_string,
            ReplyTo=reply_to or config.EMAIL_DEFAULT_FROM,
        )

        if user:
            user.log_event(
                "Sent email with subject: " + subject,
                "email",
                "Email content: " + template_vars.get("message"),
            )
    else:
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
    template_name="email_without_button.html",
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
