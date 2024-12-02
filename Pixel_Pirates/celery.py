import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pixel_Pirates.settings')
app = Celery('Pixel_Pirates')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'manage-daily-tasks': {
#         'task': 'mainApp.tasks.manage_daily_tasks',
#         'schedule': crontab(hour=0, minute=0),  # Runs daily at midnight
#     },
#     'generate-weekly-tasks': {
#         'task': 'mainApp.tasks.generate_weekly_tasks',
#         'schedule': crontab(minute=0, hour=0, day_of_week=1)  # Runs every Monday at midnight
#     }
# }


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')