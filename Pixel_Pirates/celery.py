import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pixel_Pirates.settings')
app = Celery('Pixel_Pirates')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'reset-daily-tasks-every-midnight': {
        'task': 'mainApp.tasks.reset_daily_tasks',  # Update path as needed
        'schedule': crontab(minute=0, hour=0),  # Midnight every day
    },
    'update-daily-tasks': {
        'task': 'mainApp.tasks.update_daily_tasks',
        'schedule': crontab(hour=0, minute=0),  # Runs daily at midnight
    },
    'generate-weekly-tasks': {
        'task': 'mainApp.tasks.generate_weekly_tasks',
        'schedule': crontab(minute=0, hour=0, day_of_week=1)
    }
}