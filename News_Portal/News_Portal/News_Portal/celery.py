import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_email': {
        'task': 'NewsPortal.tasks.send_week_posts',
        'schedule': crontab(hour=8, minute=0, day_of_week='mon'),
        #'task': 'NewsPortal.tasks.test_email',
        #'schedule': 60,
    },
}

