from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib import messages 
from django.shortcuts import redirect 
from django.core.exceptions import ValidationError
from django.contrib.auth import logout 
from allauth.core.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models.signals import post_save
from .models import Profile, ReferralTask
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from .task_helpers import *

@receiver(user_signed_up)
def create_profile_on_google_signup(request, user, **kwargs):
    """Create or update profile on Google OAuth sign-up."""
    sociallogin = kwargs.get('sociallogin')

    if sociallogin:
        # Extract email and username from Google's OAuth response
        email = sociallogin.account.extra_data.get('email', '')

        if not email.endswith('@bc.edu'):
            user.delete()
            logout(request)
            messages.error(request, 'only email domain with @bc.edu are allowed')
            raise ImmediateHttpResponse(redirect('login'))
        username_part = email.split('@')[0]  # Extract everything before '@'

        # Extract first and last names from Google's response
        first_name = sociallogin.account.extra_data.get('given_name', '')
        last_name = sociallogin.account.extra_data.get('family_name', '')

        # Debugging: Print statements to confirm the extracted data
        print(f"Username: {username_part}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")

        # Update the User instance before creating the profile
        user.username = username_part  # Set username to part before '@'
        user.first_name = first_name
        user.last_name = last_name
        user.save()  # Save the updated user instance

        # Now, create or update the user's profile
        Profile.objects.update_or_create(
            username=user,  # OneToOneField with User
            defaults={
                'bc_email': email,
                'name': f"{first_name} {last_name}".strip(),
            }
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """Ensure profile is created or saved whenever a User instance is saved."""
    if created:
        Profile.objects.get_or_create(
            username=instance,
            defaults={'bc_email': instance.email}
        )
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # Create the profile if it doesn't exist
            Profile.objects.create(username=instance, bc_email=instance.email)

@receiver(post_save, sender=User)
def create_default_tasks_for_new_user(sender, instance, created, **kwargs):
    """Create default tasks for a new user."""
    if created:
        from django.utils.timezone import now
        from datetime import timedelta
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Creating tasks for new user: {instance.username}")
        local_now = localtime()
        today = local_now.date()
        
        # Define tasks
        daily_tasks = [
            {"title": "COMPOSTING", "points": 5, "is_static": True},
            {"title": "RECYCLING", "points": 5, "is_static": True},
            {"title": "GREEN2GO CONTAINER", "points": 15, "is_static": True},
            {"title": "WORD OF THE DAY", "points": 20, "is_static": False, "completion_criteria": {"action_date": str(today)}},
            {"title": "PICTURE IN ACTION", "points": 20, "is_static": False, "completion_criteria": {"action_date": str(today)}},
        ]
        weekly_tasks = [
            {"title": "ARTICLE QUIZ", "points": 20, "description": "Complete the weekly quiz"},
        ]
        
        # Weekly range
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        # Create daily tasks without duplicates
        for task in daily_tasks:
            task_exists = DailyTask.objects.filter(
                user=instance,
                title=task["title"],
                is_static=task["is_static"],
                completion_criteria=task.get("completion_criteria", {})
            ).exists()

            if not task_exists:
                DailyTask.objects.create(
                    user=instance,
                    title=task["title"],
                    is_static=task["is_static"],
                    points=task["points"],
                    completed=False,
                    date_created=today,
                    time_created=local_now,
                    completion_criteria=task.get("completion_criteria", {}),
                )
                logger.info(f"Created task: {task['title']} (Static: {task['is_static']}) for user {instance.username}")

        
        # Create weekly tasks
        for task in weekly_tasks:
            WeeklyTask.objects.get_or_create(
                user=instance,
                title=task["title"],
                defaults={
                    "points": task["points"],
                    "completed": False,
                    "description": task.get("description", ""),
                    "start_date": start_of_week,
                    "end_date": end_of_week,
                }
            )
  
@receiver(post_save, sender=User)
def check_referral_completion(sender, instance, created, **kwarg):
    if created:
        # Check if a ReferralTask with this user's email exists
        referral = ReferralTask.objects.filter(referee_email=instance.email, completed=False).first()
        if referral:
            referral.complete_referral()