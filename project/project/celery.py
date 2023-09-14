import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "action_every_thursday_17am": {
        "task": "appointments.tasks.weekly_send_email_task",
        "schedule": crontab(minute=14, hour=17, day_of_week="thu"),
        "args": (),
    }
}

# celery -A project worker -l INFO --pool=solo
