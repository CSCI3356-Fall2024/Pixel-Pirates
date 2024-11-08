from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from .models import DailyTask, WeeklyTask
from datetime import timedelta
from .task_helpers import *

@shared_task
def reset_daily_tasks():
    # Reset static tasks for all users to incomplete
    DailyTask.objects.filter(is_static=True).update(completed=False)

    # Create new dynamic tasks for each user
    dynamic_tasks = [
        {"title": "WORD OF THE DAY", "points": 20},
        {"title": "PICTURE IN ACTION", "points": 20},
    ]

    for user in User.objects.all():
        create_daily_tasks(user, dynamic_tasks, is_static=False)


@shared_task
def update_daily_tasks():
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
        for task_data in static_tasks:
            DailyTask.objects.get_or_create(
                user=user,
                title=task_data["title"],
                defaults={
                    "points": task_data["points"],
                    "completed": False,
                    "is_static": task_data["is_static"],
                    "completion_criteria": {'action_date': ''},
                }
            )

        for task_data in dynamic_tasks:
            DailyTask.objects.update_or_create(
                user=user,
                title=task_data["title"],
                is_static=False,
                completion_criteria={'action_date': str(today)},
                defaults={
                    "points": task_data["points"],
                    "completed": False,
                }
            )

@shared_task
def generate_weekly_tasks():
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    weekly_tasks = [
        {"title": "ARTICLE QUIZ", "points": 20, "description": "Complete the weeky quiz"}
    ]

    for user in User.objects.all():
        create_weekly_tasks(user, weekly_tasks)