import logging

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger("main.utils")


def send_email_safe(email_subject, email_body, rec, html_version=None, bcc=[]):
    if type(rec) == type(()): # need to convert so we can append to it later
        rec = list(rec)
    if type(rec) != type([]):
        rec = [rec]
    if type(bcc) == type(()): # need to convert so we can append to it later
        bcc = list(bcc)
    if type(bcc) != type([]):
        bcc = [bcc]
    try:
        from_email = "Cobian Portal <" + settings.EMAIL_NO_REPLY + ">"
        if html_version:
            b = EmailMultiAlternatives(email_subject, email_body, from_email, rec, bcc=bcc)
            b.attach_alternative(html_version, "text/html")
        else:
            b = EmailMessage(email_subject, email_body, from_email, rec, bcc=bcc)
        b.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error("Failed to send email '%s' to %s: %s", email_subject, rec, e)
        return False


def make_both_emails(file_base, options, context_instance=None):
    options["image_path"] = settings.EMAIL_STATIC_URL
    my_body = render_to_string(file_base + ".html", options, context_instance=context_instance)
    my_text_body = render_to_string(file_base + ".txt", options, context_instance=context_instance)
    return my_text_body, my_body


def send_email(email_subject, email_body, rec, bcc=[]):
    if type(rec) == type(()): # need to convert so we can append to it later
        rec = list(rec)
    if type(rec) != type([]):
        rec = [rec]
    if type(bcc) == type(()): # need to convert so we can append to it later
        bcc = list(bcc)
    if type(bcc) != type([]):
        bcc = [bcc]
    try:
        from_email = "Cobian Portal <" + settings.EMAIL_NO_REPLY + ">"
        b = EmailMultiAlternatives(email_subject, email_body, from_email, rec, bcc=bcc)
        b.attach_alternative(email_body, "text/html")
        b.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error("Failed to send email '%s' to %s: %s", email_subject, rec, e)
        return False


def make_html_email(file_base, options, context_instance=None):
    options["image_path"] = settings.EMAIL_STATIC_URL
    my_body = render_to_string(file_base + ".html", options, context_instance=context_instance)
    return my_body