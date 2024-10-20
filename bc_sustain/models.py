from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='username')
    bc_email = models.EmailField(unique=True, default='default@bc.edu')
    school = models.CharField(max_length=100, choices=[
        ('CSOM', 'CSOM'),
        ('MCAS', 'MCAS'),
        ('LSEHD', 'LSEHD'),
        ('CSON', 'CSON'),
        ('LAW', 'LAW'),
    ])
    graduation_year = models.PositiveIntegerField()
    major1 = models.CharField(max_length=100)
    major2 = models.CharField(max_length=100, blank=True, null=True)
    minor1 = models.CharField(max_length=100, blank=True, null=True)
    minor2 = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username.username}'s Profile"