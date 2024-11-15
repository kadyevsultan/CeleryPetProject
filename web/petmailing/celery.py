import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petmailing.settings')

app = Celery('petmailing')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
