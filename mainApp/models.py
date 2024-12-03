from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from .choices import MAJOR_CHOICES, MINOR_CHOICES, SCHOOL_CHOICES
from django.utils.timezone import localtime

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
    total_points = models.IntegerField(default=0)  # All-time accumulated points
    previous_rank = models.IntegerField(null=True, blank=True)
    current_rank = models.IntegerField(null=True, blank=True)
    last_points_update = models.DateTimeField(default=timezone.now)
    rank_change = models.IntegerField(default=0, null=True)
    streak_status = models.IntegerField(default=0)

    def update_points(self, new_points):
        self.points = new_points
        self.last_points_update = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:  
            original = Profile.objects.get(pk=self.pk)
            if original.points != self.points:
                self.last_points_update = timezone.now()
        super(Profile, self).save(*args, **kwargs)

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
    
class DailyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_tasks')
    title = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    is_static = models.BooleanField(default=True)
    completion_criteria = models.JSONField(default=dict)
    date_created = models.DateField(editable=False)
    time_created = models.DateTimeField(default=localtime)  # Added field to store both date and time

    class Meta:
        # unique_together = ('user', 'title', 'is_static', 'completion_criteria')
        constraints = []
    
    def save(self, *args, **kwargs):
        # Set `date_created` explicitly from `time_created`
        self.date_created = self.time_created.date()
        super().save(*args, **kwargs)

    def complete_task(self):
        """Mark the task as completed and set the submission time."""
        if not self.completed:
            self.completed = True
            self.time_submitted = localtime()  # Set current date and time
            self.save()

    def __str__(self):
        return f"{self.title} - {'Completed' if self.completed else 'Open'}"

class WeeklyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    completion_criteria = models.JSONField(default=dict)

    def check_completion(self):
        today = timezone.now().date()

        if self.start_date <= today <= self.end_date and self.completion_criteria.get('criteria_met'):
            self.completed = True
            self.user.profile.points += self.points  
            self.user.profile.save()
            self.save()
    
    def __str__(self):
        return f"{self.title} - {'Completed' if self.completed else 'Open'}"
    

class ReferralTask(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referee_email = models.EmailField()
    points = models.IntegerField(default=10)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)

    @property
    def title(self):
        """Returns a consistent title for referral tasks."""
        return "REFERRAL TASK"

    def complete_referral(self):
        """Marks the referral as completed, awards points, and sets completion date."""
        if not self.completed:
            self.completed = True
            self.completion_date = timezone.now().date()
            self.referrer.profile.points += self.points
            self.referrer.profile.save()
            self.save()

    def __str__(self):
        return f"Referral from {self.referrer.username} to {self.referee_email} - {'Completed' if self.completed else 'Pending'}"
#create a new rewards
class Rewards(models.Model):
    title = models.CharField(max_length=500)
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    description = models.TextField(max_length=500)
    points = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
                                 
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

class ArticleQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    article_url = models.URLField(max_length=500, blank=True, null=True)  # field for external URL to display on landing page
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    question_1 = models.CharField(max_length=100, null=True, blank=True)
    q1_false_answer_1 = models.CharField(max_length=100, null=True, blank=True)
    q1_false_answer_2 = models.CharField(max_length=100, null=True, blank=True)
    q1_correct_answer = models.CharField(max_length=100, null=True, blank=True)
    question_2 = models.CharField(max_length=100, null=True, blank=True)
    q2_false_answer_1 = models.CharField(max_length=100, null=True, blank=True)
    q2_false_answer_2 = models.CharField(max_length=100, null=True, blank=True)
    q2_correct_answer = models.CharField(max_length=100, null=True, blank=True)
    question_3 = models.CharField(max_length=100, null=True, blank=True)
    q3_false_answer_1 = models.CharField(max_length=100, null=True, blank=True)
    q3_false_answer_2 = models.CharField(max_length=100, null=True, blank=True)
    q3_correct_answer = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self) -> str:
        return self.title