import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model_tutor.settings')

app = Celery('mc_donalds')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()