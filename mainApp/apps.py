from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'

    def ready(self):
        from django_celery_beat.models import IntervalSchedule, PeriodicTask  # Import here
        try:
            # Schedule daily tasks
            interval, created = IntervalSchedule.objects.get_or_create(
                every=1,  
                period=IntervalSchedule.DAYS,
            )
            if created:
                logger.info(f"Daily Interval created: {interval.id}")

            PeriodicTask.objects.get_or_create(
                interval=interval,
                name="Generate Daily Tasks",
                task="mainApp.tasks.generate_daily_tasks",
            )
            logger.info("Periodic task for daily tasks created")

            # Schedule weekly tasks
            weekly_interval, created = IntervalSchedule.objects.get_or_create(
                every=7,
                period=IntervalSchedule.DAYS,
            )
            if created:
                logger.info(f"Weekly Interval created: {weekly_interval.id}")

            PeriodicTask.objects.get_or_create(
                interval=weekly_interval,
                name="Generate Weekly Tasks",
                task="mainApp.tasks.generate_weekly_tasks",
            )
            logger.info("Periodic task for weekly tasks created")

        except Exception as e:
            logger.error(f"Error scheduling tasks: {e}")
