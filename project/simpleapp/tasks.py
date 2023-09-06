from celery import shared_task

from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from project.settings import DEFAULT_FROM_EMAIL, SITE_URL

@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_contect = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_contect, 'text/html')
    msg.send()
