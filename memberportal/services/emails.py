from django.template.loader import render_to_string
from django.utils.html import escape
from sendgrid.helpers.mail import *
from membermatters.helpers import log_user_event
from constance import config
import sendgrid


def send_group_email(user, emails, subject, title, message):
    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string(
        "email_without_button.html", {"email": email_vars, "config": config}
    )
    emails.append(config.EMAIL_ADMIN)
    mail = Mail()

    for to_email in emails:
        print(to_email)
        # Create new instance for each email
        personalization = Personalization()
        # Add email addresses to personalization instance
        personalization.add_to(Email(to_email))
        # Add personalization instance to Mail object
        mail.add_personalization(personalization)

    # Add data that is common to all personalizations
    mail.from_email = Email(config.EMAIL_DEFAULT_FROM)
    mail.reply_to = Email(user.email)
    mail.subject = subject
    mail.add_content(Content("text/html", email_string))

    # Send
    sg = sendgrid.SendGridAPIClient(config.SENDGRID_API_KEY)
    response = sg.send(mail)

    if response.status_code == 202:
        log_user_event(
            user,
            "Sent email with subject: " + subject,
            "email",
            "Email content: " + email_string,
        )
        return True
    else:
        log_user_event(
            user,
            "Failed to send email with subject: " + subject,
            "email",
            "Email content: " + email_string,
        )
        return False


def send_single_email(
    user: object,
    email: object,
    subject: object,
    title: object,
    message: object,
    from_user=False,
) -> object:
    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string(
        "email_without_button.html", {"email": email_vars, "config": config}
    )

    sg = sendgrid.SendGridAPIClient(config.SENDGRID_API_KEY)
    from_email = From(config.EMAIL_DEFAULT_FROM)
    to_email = To(email)
    subject = subject
    content = Content("text/html", email_string)
    mail = Mail(from_email, to_email, subject, content)

    if from_user:
        mail.reply_to = ReplyTo(user.email, user.profile.get_full_name())

    response = sg.send(mail)

    if response.status_code == 202:
        log_user_event(
            user,
            "Sent email with subject: " + subject,
            "email",
            "Email content: " + message,
        )
        return True
    else:
        return False


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

    sg = sendgrid.SendGridAPIClient(config.SENDGRID_API_KEY)
    from_email = From(config.EMAIL_DEFAULT_FROM)
    to_email = To(config.EMAIL_ADMIN)
    subject = subject
    content = Content("text/html", email_string)
    mail = Mail(from_email, to_email, subject, content)

    return sg.send(mail)
