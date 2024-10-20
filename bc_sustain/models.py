from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()
    major1 = models.CharField(max_length=100)
    major2 = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"