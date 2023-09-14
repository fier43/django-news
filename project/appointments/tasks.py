from celery import shared_task
from django.template.loader import render_to_string
import datetime
from simpleapp.models import News, Category
from project.settings import DEFAULT_FROM_EMAIL, SITE_URL
from django.core.mail import EmailMultiAlternatives
from project.celery import app


@shared_task
def send_email_task(pk):
    news = News.objects.get(pk=pk)
    categories = news.category.all()
    title = news.title
    subscribers_emails = []
    for category in categories:
        subscribers_user = category.subscribers.all()
        for sub_user in subscribers_user:
            subscribers_emails.append(sub_user.email)

    html_contect = render_to_string(
        "post_created_email.html",
        {"text": f"{news.title}", "link": f"{SITE_URL}/news/{pk}"},
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body="",
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_contect, "text/html")
    msg.send()


# отправляем письмо на почту раз в неделю
@shared_task
def weekly_send_email_task():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    news = News.objects.filter(date__gte=last_week)
    categories = set(news.values_list("category__name", flat=True))
    subscribers = set(
        Category.objects.filter(name__in=categories).values_list(
            "subscribers__email", flat=True
        )
    )

    html_content = render_to_string(
        "daile_news.html",
        {
            "link": SITE_URL,
            "news": news,
        },
    )

    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body="",
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


# celery -A project worker -l INFO --pool=solo
