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
from .models import Profile, ReferralTask, ReferralTempStore
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from .task_helpers import *
from pinax.referrals.models import Referral

import logging
logger = logging.getLogger(__name__)

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

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    """
    Handles user signup, processes referral codes, and creates/upgrades profiles.
    """
    temp_username = request.session.pop('temp_username', None)
    referral_code = None
    referrer_profile = None

    # Retrieve referral code from ReferralTempStore
    if temp_username:
        try:
            # Retrieve referral code from ReferralTempStore
            temp_store = ReferralTempStore.objects.get(username=temp_username)
            referral_code = temp_store.referral_code
            
            # Save the referral code to the user's profile
            profile, created = Profile.objects.get_or_create(username=user)
            profile.referral_code = referral_code
            profile.save()
            
            # Clean up the temporary referral store
            temp_store.delete()
            print(f"Referral code retrieved and saved for user {user.username}: {referral_code}")
        except ReferralTempStore.DoesNotExist:
            print(f"No referral code found for temp user {temp_username}")
    
    # Process referral code if it exists
        if temp_username:
            try:
                # Retrieve referral code from ReferralTempStore
                temp_store = ReferralTempStore.objects.get(username=temp_username)
                referral_code = temp_store.referral_code
                
                # Save the referral code to the user's profile
                profile, created = Profile.objects.get_or_create(username=user)
                profile.referral_code = referral_code
                profile.save()
                
                # Clean up the temporary referral store
                temp_store.delete()
                print(f"Referral code retrieved and saved for user {user.username}: {referral_code}")
            except ReferralTempStore.DoesNotExist:
                print(f"No referral code found for temp user {temp_username}")
        

    # Generate a referral for the new user
    referral = Referral.create(
        user=user,
        redirect_to=reverse("home")
    )
    profile.referral = referral
    profile.save()

    print(f"Profile created/updated for user: {user.username}")

# Create or update profile and tasks after saving a User
@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    """
    Ensures profile creation and assigns default tasks for new users.
    """
    profile, _ = Profile.objects.get_or_create(
        username=instance,
        defaults={'bc_email': instance.email}
    )

    if created:
        logger.info(f"Creating default tasks for user: {instance.username}")
        today = localtime().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Define default tasks
        daily_tasks = [
            {"title": "COMPOSTING", "points": 5, "is_static": True},
            {"title": "RECYCLING", "points": 5, "is_static": True},
            {"title": "GREEN2GO CONTAINER", "points": 15, "is_static": True},
            {"title": "WORD OF THE DAY", "points": 20, "is_static": False},
            {"title": "PICTURE IN ACTION", "points": 20, "is_static": False},
        ]
        weekly_tasks = [
            {"title": "ARTICLE QUIZ", "points": 20, "description": "Complete the weekly quiz"},
        ]

        # Create daily tasks
        for task in daily_tasks:
            DailyTask.objects.get_or_create(
                user=instance,
                title=task["title"],
                defaults={
                    "is_static": task["is_static"],
                    "points": task["points"],
                    "completed": False,
                    "date_created": today,
                }
            )

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

