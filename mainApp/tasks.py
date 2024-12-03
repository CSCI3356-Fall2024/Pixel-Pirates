from celery import shared_task
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from .models import DailyTask, WeeklyTask
from datetime import timedelta
from time import sleep
import logging

logger = logging.getLogger(__name__)

@shared_task 
def my_task():
    for i in range(11): 
        print(i)
        sleep(1)
    return "Task Completed"

@shared_task
def generate_daily_tasks():
    """Generate new daily tasks for all users, ensuring unique entries with date and time suffix."""
    current_time = localtime()  # Get current local time
    today_date = current_time.date()  # Extract the date
    time_suffix = current_time.strftime("%H:%M:%S")  # Format the time as HH:MM:SS

    # Define daily tasks
    daily_tasks = [
        {"title": "COMPOSTING", "points": 5, "is_static": True},
        {"title": "RECYCLING", "points": 5, "is_static": True},
        {"title": "GREEN2GO CONTAINER", "points": 15, "is_static": True},
        {"title": "WORD OF THE DAY", "points": 20, "is_static": False},
        {"title": "PICTURE IN ACTION", "points": 20, "is_static": False},
    ]

    for user in User.objects.all():
        for task in daily_tasks:
            DailyTask.objects.update_or_create(
                user=user,
                title=task["title"],
                is_static=task["is_static"],
                completion_criteria=task.get("completion_criteria", {}),
                date_created=localtime,  # Ensure date uniqueness
                defaults={
                    "points": task["points"],
                    "completed": False,
                    "time_created": localtime(),
                },
            )

    logger.info("Daily tasks generated successfully for today's date.")

@shared_task
def generate_weekly_tasks():
    """Generate or update weekly tasks for all users."""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Define weekly tasks
    weekly_tasks = [
        {"title": "ARTICLE QUIZ", "points": 20, "description": "Complete the weekly quiz"}
    ]

    for user in User.objects.all():
        for task in weekly_tasks:
            WeeklyTask.objects.update_or_create(
                user=user,
                title=task["title"],
                start_date=start_of_week,
                defaults={
                    "description": task["description"],
                    "points": task["points"],
                    "completed": False,
                    "end_date": end_of_week,
                }
            )

    logger.info("Weekly tasks generated successfully.")

