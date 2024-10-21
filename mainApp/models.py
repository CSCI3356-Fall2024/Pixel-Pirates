from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    bc_email = models.EmailField(unique=True, default='default@bc.edu')
    school = models.CharField(
        max_length=100, 
        choices=[
            ('CSOM', 'CSOM'),
            ('MCAS', 'MCAS'),
            ('LSEHD', 'LSEHD'),
            ('CSON', 'CSON'),
            ('LAW', 'LAW'),
        ]
    )
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    major = models.CharField(max_length=100)
    minor = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username.username}'s Profile"
