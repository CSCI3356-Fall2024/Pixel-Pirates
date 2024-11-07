from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from mainApp.models import DailyTask

class Command(BaseCommand):
    help = "Update daily tasks for all users."

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        # Define the static tasks
        static_tasks = [
            {"title": "COMPOSTING", "points": 5, "is_static": True},
            {"title": "RECYCLING", "points": 5, "is_static": True},
            {"title": "GREEN2GO CONTAINER", "points": 15, "is_static": True},
        ]

        # Define the dynamic tasks for today
        dynamic_tasks = [
            {"title": "WORD OF THE DAY", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
            {"title": "PICTURE IN ACTION", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
        ]

        # Update tasks for each user
        users = User.objects.all()
        for user in users:
            # Add missing static tasks
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

            # Add new dynamic tasks for today
            for task_data in dynamic_tasks:
                # Ensure only one instance of each dynamic task per day
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

        self.stdout.write(self.style.SUCCESS("Updated daily tasks for all users."))
