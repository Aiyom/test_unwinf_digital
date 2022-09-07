import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chan.settings')

app = Celery('Chan')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_always_eager = False

app.conf.beat_schedule = {
    'get_orders': {
        'task': 'crud_google_sheet.tasks.get_ordersWild',
        'schedule': crontab(minute='*/1')
    },
    'call_check': {
        'task': 'crud_google_sheet.tasks.call_check',
        'schedule': crontab(hour='*/24')
    }
}