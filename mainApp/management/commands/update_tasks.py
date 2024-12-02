from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from models import DailyTask, WeeklyTask
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def manage_tasks():
    today = timezone.now().date()

    # Define static and dynamic tasks
    static_tasks = [
        {"title": "COMPOSTING", "points": 5, "is_static": True},
        {"title": "RECYCLING", "points": 5, "is_static": True},
        {"title": "GREEN2GO CONTAINER", "points": 15, "is_static": True},
    ]

    dynamic_tasks = [
        {"title": "WORD OF THE DAY", "points": 20, "is_static": False, "completion_criteria": {"action_date": str(today)}},
        {"title": "PICTURE IN ACTION", "points": 20, "is_static": False, "completion_criteria": {"action_date": str(today)}},
    ]

    # Weekly task details
    weekly_tasks = [
        {"title": "ARTICLE QUIZ", "points": 30, "description": "Complete the weekly quiz"}
    ]

    # Calculate start and end of the week
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    for user in User.objects.all():
        logger.info(f"Processing tasks for user: {user.username}")

        # Add missing static tasks
        for task_data in static_tasks:
            DailyTask.objects.get_or_create(
                user=user,
                title=task_data["title"],
                defaults={
                    "points": task_data["points"],
                    "completed": False,
                    "is_static": task_data["is_static"],
                    "completion_criteria": {"action_date": ""},
                },
            )

        # Add or update dynamic tasks
        for task_data in dynamic_tasks:
            DailyTask.objects.update_or_create(
                user=user,
                title=task_data["title"],
                is_static=False,
                completion_criteria={"action_date": str(today)},
                defaults={
                    "points": task_data["points"],
                    "completed": False,
                },
            )

        # Add or update weekly tasks
        for task_data in weekly_tasks:
            WeeklyTask.objects.update_or_create(
                user=user,
                title=task_data["title"],
                start_date=start_of_week,
                end_date=end_of_week,
                defaults={
                    "description": task_data["description"],
                    "points": task_data["points"],
                    "completed": False,
                },
            )
    logger.info("Daily and weekly tasks updated successfully.")
