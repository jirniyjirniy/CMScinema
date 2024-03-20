from celery_progress.backend import ProgressRecorder
from django.core.mail import EmailMultiAlternatives

from celery import shared_task


@shared_task(bind=True)
def send_email_task(self, recipient_emails, subject, template_content):
    progress_recorder = ProgressRecorder(self)
    total_emails = len(recipient_emails)

    try:
        for index, recipient_email in enumerate(recipient_emails, 1):
            email = EmailMultiAlternatives(subject, template_content, to=recipient_emails)
            email.content_subtype = 'html'
            progress_recorder.set_progress(index, total_emails, description=f'Отправка письма на {recipient_email}')
            email.send()
    except Exception as e:
        print(f"Error sending email: {e}")
        return {'success': False}
    return 'Отправлено'


# @shared_task()
# def send_email_task(recipient_emails, subject, template_content):
#     try:
#         email = EmailMultiAlternatives(subject, template_content, to=recipient_emails)
#         email.content_subtype = 'html'
#         email.send()
#         return 'Отправлено'
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         return {'success': False}
