from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from .choices import MAJOR_CHOICES, MINOR_CHOICES, SCHOOL_CHOICES

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE) #this is just the user itself, not the actual username of the user
    name = models.CharField(max_length=100)                         
    bc_email = models.EmailField(unique=True, default='default@bc.edu')
    school = models.CharField(max_length=100, choices=SCHOOL_CHOICES)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    major = MultiSelectField(choices=MAJOR_CHOICES, blank=True)
    minor = MultiSelectField(choices=MINOR_CHOICES, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    points = models.IntegerField(default=0)
    previous_rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username.username}'s Profile"
 

class Campaign(models.Model):
    title = models.CharField(max_length=200)  # Changed to CharField for better practice
    description = models.TextField(max_length=500)  # Increased max length
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    points = models.IntegerField(default=0)
    news = models.BooleanField(default=True)
    LOCATION_CHOICES = [
        ('Lower', 'Lower'),
        ('McElroy', 'McElroy'),
        ('Stuart', 'Stuart'),
        ("Addie's", "Addie's"),
        ("Eagle's Nest", "Eagle's Nest"),
    ]
    location = MultiSelectField(choices=LOCATION_CHOICES, blank=True)

    validation = models.CharField(
        max_length=100, 
        choices=[
            ('photo validation', 'photo validation'),
            ('QR', 'QR'),
        ],
        default='photo validation'
    )

    def __str__(self):
        return self.title
    
class News(models.Model):
    display_title = models.CharField(max_length=500)
    external_url = models.URLField(max_length=500, blank=True, null=True)  # field for external URL to display on landing page
    date_posted = models.DateTimeField(auto_now_add=True)
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    news_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
                                 
    def __str__(self):
        return self.display_title
    
#create a new rewards
class Rewards(models.Model):
    title = models.CharField(max_length=500)
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    description = models.TextField(max_length=500)
    points = models.IntegerField(default=0)
                                 
    def __str__(self):
        return self.title
    
class Redeemed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.title
