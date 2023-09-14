from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from simpleapp.models import News

from .tasks import send_email_task


@receiver(m2m_changed, sender=News.category.through)
def send_email_task_call(sender, instance, action, **kwargs):
    if action == "post_add":
        send_email_task.delay(instance.pk)
