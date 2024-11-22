from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Campaign)
admin.site.register(News)
admin.site.register(Rewards)
admin.site.register(Redeemed)
@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'points', 'is_static', 'completed')
    list_filter = ('is_static', 'completed')
    search_fields = ('user__username', 'title')