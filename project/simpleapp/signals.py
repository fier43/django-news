from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from .models import News
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from project.settings import DEFAULT_FROM_EMAIL, SITE_URL

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

@receiver(m2m_changed, sender=News.category.through)
def notify_about__new_news(sender, instance, action, **kwargs):
    if action == 'post_add':
        subscribers_emails = []

        for category in instance.category.all():
            subscribers = category.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)

        # for subscriber in subscribers:
        #     subject = instance.title
        #     message = f"Здравствуй, {subscriber.username}. Новая статья в твоем любимом разделе!\n\n"
        #     message += f"<b>{instance.title}</b>\n\n"
        #     message += f"{instance.description[:50]}..."
        #     # send_mail(subject, message, 'DimonDexp@yandex.ru', [subscriber.email], html_message=message)

        #     email = EmailMessage(subject, message, 'DimonDexp@yandex.ru', to=[subscriber.email])
        #     email.send()
