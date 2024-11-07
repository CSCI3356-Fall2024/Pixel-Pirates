from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from .models import DailyTask

@shared_task
def reset_daily_tasks():
    today = timezone.now().date()
    
    # Reset static tasks for all users to incomplete
    DailyTask.objects.filter(is_static=True).update(completed=False)

    # Create new dynamic tasks for each user
    dynamic_tasks = [
        {"title": "WORD OF THE DAY", "points": 20, "completion_criteria": {'action_date': str(today)}},
        {"title": "PICTURE IN ACTION", "points": 20, "completion_criteria": {'action_date': str(today)}},
    ]

    users = User.objects.all()
    for user in users:
        for task_data in dynamic_tasks:
            # Check if a dynamic task for today already exists
            if not DailyTask.objects.filter(user=user, title=task_data["title"], completion_criteria__action_date=str(today)).exists():
                DailyTask.objects.create(
                    user=user,
                    title=task_data["title"],
                    points=task_data["points"],
                    completed=False,
                    is_static=False,
                    completion_criteria=task_data["completion_criteria"]
                )

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