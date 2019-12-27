import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async.settings')

celery_app = Celery('async', broker="redis://localhost:5672/0")
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(settings.INSTALLED_APPS)
