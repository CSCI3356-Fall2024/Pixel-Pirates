from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Campaign)
admin.site.register(News)
admin.site.register(Rewards)
admin.site.register(Redeemed)
admin.site.register(History)

# Admin for DailyTask
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'points', 'date_created', 'time_created', 'completed', 'is_static')  # Added time_created
    list_filter = ('completed', 'is_static', 'date_created', 'time_created')  # Added time_created filter
    search_fields = ('title', 'user__username')  # Allow search by task title and username
    ordering = ('-time_created',)  # Order by time created descending

# Admin for WeeklyTask
class WeeklyTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'points', 'start_date', 'end_date', 'completed')  # Fields to display in list view
    list_filter = ('completed', 'start_date', 'end_date')  # Add filters for completion and date ranges
    search_fields = ('title', 'user__username')  # Allow search by task title and username
    ordering = ('-start_date',)  # Order by start date descending

# Registering models with their respective admin
admin.site.register(DailyTask, DailyTaskAdmin)
admin.site.register(WeeklyTask, WeeklyTaskAdmin)
admin.site.register(ArticleQuiz)
admin.site.register(ReferralTempStore)

