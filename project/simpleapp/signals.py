from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import News

from .tasks import send_notifications

@receiver(m2m_changed, sender=News.category.through)
def notify_about__new_news(sender, instance, action, **kwargs):
    if action == 'post_add':
        subscribers_emails = []

        for category in instance.category.all():
            subscribers = category.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)

