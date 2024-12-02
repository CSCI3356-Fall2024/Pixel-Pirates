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
    list_display = (
        'user',
        'title',
        'points',
        'is_static',
        'completed',
        'completion_criteria'
    )
    list_filter = ('is_static', 'completed', 'completion_criteria')  # Adding filters for better usability
    search_fields = ('user__username', 'title', 'completion_criteria')  # Allows searching by username, title, or criteria

    readonly_fields = ('completion_criteria',)  # Protects timestamps and criteria