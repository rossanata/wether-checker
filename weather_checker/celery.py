import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_checker.settings')

app = Celery('weather_checker')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'update-weather-data-daily': {
        'task': 'weather_app.tasks.update_weather_data_daily',
        'schedule': crontab(minute=0, hour=0),
    },
}

app.autodiscover_tasks()
