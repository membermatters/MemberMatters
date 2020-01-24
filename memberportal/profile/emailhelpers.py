from django.template.loader import render_to_string
from django.utils.html import escape
from django.conf import settings
from sendgrid.helpers.mail import *
from memberportal.helpers import log_user_event
import sendgrid
import os


def send_group_email(user, emails, subject, title, message):
    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string('email_without_button.html', {'email': email_vars})
    emails.append(settings.EXEC_EMAIL)

    if "PORTAL_SENDGRID_API_KEY" in os.environ:
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
        mail.from_email = Email(settings.FROM_EMAIL)
        mail.reply_to = Email(user.email)
        mail.subject = subject
        mail.add_content(Content('text/html', email_string))

        # Send
        sg = sendgrid.SendGridAPIClient(os.environ.get('PORTAL_SENDGRID_API_KEY'))
        response = sg.send(mail)

        if response.status_code == 202:
            log_user_event(user, "Sent email with subject: " + subject, "email", "Email content: " + email_string)
            return True
        else:
            log_user_event(user, "Failed to send email with subject: " + subject, "email", "Email content: " + email_string)
            return False
    else:
        raise RuntimeError("No SendGrid API key found in environment variables.")


def send_single_email(user, email, subject, title, message):
    message = escape(message)
    message = message.replace("~br~", "<br>")
    email_vars = {"preheader": "", "title": title, "message": message}
    email_string = render_to_string('email_without_button.html', {'email': email_vars})

    if "PORTAL_SENDGRID_API_KEY" in os.environ:
        sg = sendgrid.SendGridAPIClient(os.environ.get('PORTAL_SENDGRID_API_KEY'))
        from_email = From(settings.FROM_EMAIL)
        to_email = To(email)
        subject = subject
        content = Content("text/html", email_string)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.send(mail)

        if response.status_code == 202:
            log_user_event(user, "Sent email with subject: " + subject, "email", "Email content: " + message)
            return True
        else:
            return False

    log_user_event(user, "Failed to send email with subject: " + subject, "email", "Email content: " + message)
    raise RuntimeError("No SendGrid API key found in environment variables.")
