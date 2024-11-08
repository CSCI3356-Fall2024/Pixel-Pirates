from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from mainApp.models import DailyTask, WeeklyTask

class Command(BaseCommand):
    help = "Update daily and weekly tasks for all users."

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        
        # Define static daily tasks
        static_tasks = [
            {"title": "COMPOSTING", "points": 5, "is_static": True},
            {"title": "RECYCLING", "points": 5, "is_static": True},
            {"title": "GREEN2GO CONTAINER", "points": 15, "is_static": True},
        ]

        # Define dynamic daily tasks for today
        dynamic_tasks = [
            {"title": "WORD OF THE DAY", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
            {"title": "PICTURE IN ACTION", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
        ]

        # Define weekly task
        weekly_tasks = [
            {"title": "ARTICLE QUIZ", "points": 30, "description": "Complete the weekly quiz"}
        ]

        # Calculate start and end of the week
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        print(f"Weekly period: {start_of_week} to {end_of_week}")  # Debugging output

        # Update tasks for each user
        users = User.objects.all()
        for user in users:
            print(f"Processing user: {user.username}")  # Debugging output

            # Add missing static daily tasks
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

            # Add new dynamic daily tasks for today
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

            # Add or update weekly task
            for task_data in weekly_tasks:
                weekly_task, created = WeeklyTask.objects.update_or_create(
                    user=user,
                    title=task_data["title"],
                    start_date=start_of_week,
                    end_date=end_of_week,
                    defaults={
                        "description": task_data["description"],
                        "points": task_data["points"],
                        "completed": False,
                    }
                )
                # Check if task was created or updated
                if created:
                    print(f"Weekly task '{weekly_task.title}' created for user '{user.username}'")
                else:
                    print(f"Weekly task '{weekly_task.title}' updated for user '{user.username}'")

        self.stdout.write(self.style.SUCCESS("Updated daily and weekly tasks for all users."))
