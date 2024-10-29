from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mainApp.models import Profile
import random
from django.db import transaction
class Command(BaseCommand):
    help = 'Creates or updates sample data of 100 users and their profiles'
    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                for i in range(1, 101):
                    user, created = User.objects.get_or_create(
                        username=f'user{i}',
                        defaults={'email': f'user{i}@example.com'}
                    )
                    if created:
                        user.set_password('password123')
                        user.save()
                        self.stdout.write(self.style.NOTICE(f"Created user: {user.username}, Email: {user.email}"))
                    # If the profile already exists, update it with missing data
                    profile, profile_created = Profile.objects.get_or_create(username=user)
                    if profile_created:
                        self.stdout.write(self.style.NOTICE(f"Creating Profile for: {profile.username}"))
                    else:
                        self.stdout.write(self.style.NOTICE(f"Updating Profile for: {profile.username}"))
                    # Assign profile values and save
                    profile.name = f'User {i}'
                    profile.bc_email = f'user{i}@bc.edu'
                    profile.school = random.choice(['CSOM', 'MCAS', 'LSEHD', 'CSON', 'LAW'])
                    profile.graduation_year = random.randint(2022, 2025)
                    profile.major = f'Major {i}'
                    profile.minor = f'Minor {i}' if random.choice([True, False]) else None
                    profile.bio = f'This is the bio for User {i}.'
                    profile.points = random.randint(0, 100)  # Assigning points here
                    profile.save()
                    self.stdout.write(self.style.SUCCESS(f'Profile for {user.username} has been created/updated with {profile.points} points.'))
            self.stdout.write(self.style.SUCCESS('Successfully created or updated 100 users and their profiles'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating/updating sample data: {e}'))