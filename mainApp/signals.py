from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib import messages 
from django.shortcuts import redirect 
from django.core.exceptions import ValidationError
from django.contrib.auth import logout 
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models.signals import post_save
from .models import Profile, DailyTask
from django.contrib.auth.models import User
from django.utils import timezone

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
def create_default_daily_tasks(sender, instance, created, **kwargs):
    if created:
        # Create static tasks 
        static_tasks = [
            {"title": "COMPOSTING", "points": 5},
            {"title": "RECYCLING", "points": 5},
            {"title": "GREEN2GO CONTAINER", "points": 15},
        ]

        for task_data in static_tasks:
            DailyTask.objects.create(
                user = instance,
                title = task_data["title"],
                points = task_data["points"],
                completed = False,
                is_static = True,
                completion_criteria = {'action_date': ''},
            )

        today = timezone.now().date()
        dynamic_tasks = [
            {"title": "WORD OF THE DAY", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
            {"title": "PICTURE IN ACTION", "points": 20, "is_static": False, "completion_criteria": {'action_date': str(today)}},
        ]
        for task_data in dynamic_tasks:
            DailyTask.objects.create(
                user=instance,
                title=task_data["title"],
                points=task_data["points"],
                completed=False,
                is_static=task_data["is_static"],
                completion_criteria=task_data["completion_criteria"],
            )
