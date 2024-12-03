from django.apps import AppConfig
from django.conf import settings
from django.utils.timezone import localtime
import logging

logger = logging.getLogger(__name__)

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'

    def ready(self):
        """
        Perform app-specific initialization, including connecting signals and scheduling tasks.
        """
        import mainApp.signals  # Ensure signals are connected
        super().ready()  # Ensure parent logic executes

        # Schedule the midnight task only when running the server or Celery
        if any(arg in self.argv for arg in ['runserver', 'celery']):
            try:
                self.schedule_tasks()
            except Exception as e:
                logger.error(f"Error scheduling tasks: {e}")

    def schedule_tasks(self):
        """
        Schedule periodic tasks for generating daily and weekly tasks.
        """
        from django_celery_beat.models import CrontabSchedule, PeriodicTask

        # Use the timezone from settings
        app_timezone = settings.TIME_ZONE

        # Schedule daily tasks to run every minute (for testing purposes)
        daily_crontab, created = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_month="*",
            month_of_year="*",
            day_of_week="*",  # Every day
            timezone=app_timezone,
        )
        # Create a new periodic task every time this is invoked, with a unique name
        timestamp = localtime().strftime('%Y-%m-%d %H:%M:%S')
        PeriodicTask.objects.create(
            crontab=daily_crontab,
            name=f"Generate Daily Tasks {timestamp}",
            task="mainApp.tasks.generate_daily_tasks",
        )

        logger.info(f"New daily task created successfully at {timestamp}.")

        # Schedule weekly tasks to run every Sunday at midnight
        weekly_crontab, created = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_month="*",
            month_of_year="*",
            day_of_week="0",  # Sunday
            timezone=app_timezone,
        )
        PeriodicTask.objects.get_or_create(
            crontab=weekly_crontab,
            name="Generate Weekly Tasks Every Sunday",
            defaults={"task": "mainApp.tasks.generate_weekly_tasks"},
        )

        logger.info("Periodic tasks scheduled successfully.")

    @property
    def argv(self):
        """Helper to check command-line arguments."""
        import sys
        return sys.argv