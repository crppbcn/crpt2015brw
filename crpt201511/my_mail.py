import sys

from crpt201511.settings import EMAIL_HOST_USER, BASE_DIR
from crpt201511.utils.env_utils import *
from django.core.mail import EmailMultiAlternatives


class MyMail:

    def __init__(self):
        pass

    @staticmethod
    def send_mail(subject, html_content, text_content, recipients, expert_request=None, attach_tor=False,
                  attach_letter=False):

        # control of execution
        if email_is_off():
            return

        # control of environment
        if env_is_local():
            pass

        # test indicator to render PDF as test sample
        test = test_is_on()
        if test:
            # subject with TEST
            subject = "This is a TEST email! " + subject

        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'

        # attachments stuff, if any

        msg.send()
