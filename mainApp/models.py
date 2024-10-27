from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE) #this is just the user itself, not the actual username of the user
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
 

class Campaign(models.Model):
    title = models.CharField(max_length=200)  # Changed to CharField for better practice
    description = models.TextField(max_length=500)  # Increased max length
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    points = models.IntegerField(default=0)
    news = models.BooleanField(default=False)
    validation = models.CharField(
        max_length=100, 
        choices=[
            ('photo validation', 'photo validation'),
            ('QR', 'QR'),
        ],
        default='photo validation'
    )
    location = MultiSelectField(
        choices=[
            ('Lower', 'Lower'),
            ('McElroy', 'McElroy'),
            ('Stuart', 'Stuart'),
            ("Addie's", "Addie's"),
            ("Eagle's Nest", "Eagle's Nest"),
        ],
        default=list,
        blank=True
    )

    def __str__(self):
        return self.title