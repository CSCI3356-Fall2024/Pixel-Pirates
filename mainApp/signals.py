from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Automatically create a profile for the user
        Profile.objects.create(
            username=instance,  # Assuming 'username' is a OneToOneField to User
            bc_email=instance.email,
            name=f"{instance.first_name} {instance.last_name}",
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the user's profile whenever the User instance is saved
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Handle the case where the profile does not yet exist
        Profile.objects.create(username=instance, bc_email=instance.email)
