from django.contrib import admin
from .models import Profile, Campaign, News, Rewards, Redeemed

# Register your models here.
admin.site.register(Profile)
admin.site.register(Campaign)
admin.site.register(News)
admin.site.register(Rewards)
admin.site.register(Redeemed)