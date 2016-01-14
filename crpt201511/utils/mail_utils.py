import sys
from django.template import loader, Context

from crpt201511.my_mail import MyMail
from crpt201511.trace import trace_action
from crpt201511.settings import SUPPORT_MAIL_LIST
from crpt201511.constants import TRACE_MAIL_COMMENT


def send_comments_email(text, section, person):
    try:
        my_mail = MyMail()
        recipients = SUPPORT_MAIL_LIST
        subject = "CRPT - Comment - " + section.name + " - " + person.name

        html_template = loader.get_template('crpt201511/email/comment.html')
        html_content = html_template.render(Context({'person': person, 'comment': text, }))
        text_template = loader.get_template('crpt201511/email/comment.txt')
        text_content = text_template.render(Context({'person': person, 'comment': text, }))

        my_mail.send_mail(subject, html_content, text_content, recipients)

        trace_action(TRACE_MAIL_COMMENT, person, "Section: " + section.name + " - Comment: " + text)
    except:
        print("Error sending comment email. Person:" + person.name)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass

