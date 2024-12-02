from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from .models import DailyTask, WeeklyTask
from datetime import timedelta
from .task_helpers import *
import logging
logger = logging.getLogger(__name__)

def manage_daily_tasks():
    today = timezone.now().date()

    static_tasks = [
        {"title": "COMPOSTING", "points": 5, "is_static": True},
        {"title": "RECYCLING", "points": 5, "is_static": True},
        {"title": "GREEN2GO CONTAINER", "points": 15, "is_static": True},
    ]

    dynamic_tasks = [
        {"title": "WORD OF THE DAY", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
        {"title": "PICTURE IN ACTION", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
    ]

    for user in User.objects.all():
        # Ensure static tasks exist or reset them
        for task_data in static_tasks:
            DailyTask.objects.update_or_create(
                user=user,
                title=task_data["title"],
                is_static=True,  # Ensure static tasks are targeted
                defaults={
                    "points": task_data["points"],
                    "completed": False,
                }
            )

        # Handle dynamic tasks like static tasks by resetting their completed status
        for task_data in dynamic_tasks:
            task, created = DailyTask.objects.update_or_create(
                user=user,
                title=task_data["title"],
                is_static=False,
                completion_criteria={'action_date': str(today)},  # Ensure this is unique
                defaults={
                    "points": task_data["points"],
                    "completed": False,
                }
            )
            if created:
                logger.info(f"Dynamic Task created: {task.title} for {user.username}")
            else:
                logger.info(f"Dynamic Task exists: {task.title} for {user.username}")



@shared_task
def generate_weekly_tasks():
    """Generate or update weekly tasks for all users."""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Start of the current week
    end_of_week = start_of_week + timedelta(days=6)         # End of the current week

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