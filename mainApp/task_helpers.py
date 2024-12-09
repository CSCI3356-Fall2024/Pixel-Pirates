from .models import DailyTask, WeeklyTask
from django.utils import timezone
from datetime import timedelta

def create_daily_tasks(user, task_data, is_static=False):
    """Create daily tasks for a specific user."""
    now = timezone.now() - timedelta(hours=5)
    today = now.date()
    for task in task_data:
        action_date = str(today) if not is_static else ''
        DailyTask.objects.update_or_create(
            user=user,
            title=task["title"],
            is_static=is_static,
            completion_criteria={"action_date": action_date},
            defaults={
                "points": task["points"],
                "completed": False,
            }
        )

def create_weekly_tasks(user, weekly_task_data, start_date, end_date):
    """Create weekly tasks for a specific user based on a specified week's range."""
    for task in weekly_task_data:
        WeeklyTask.objects.update_or_create(
            user=user,
            title=task["title"],
            start_date=start_date,
            defaults={
                "description": task["description"],
                "points": task["points"],
                "completed": False,
                "end_date": end_date,
            }
        )
