from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("confirmation/", views.confirmation_view, name="confirmation"),
    path("home/", views.home_view, name="home"),
    path("actions/", views.actions_view, name="actions"),
    path("choose_action/", views.choose_action_view, name = "choose_action"),
    path("create_news/", views.news_view, name = "create_news"),
    path('create_news/edit/<int:id>/', views.edit_news, name='edit_news'),
    path("rewards/", views.rewards_view, name='rewards'),
    path("redeem_reward/", views.redeem_reward, name='redeem_reward'),
    path('rewards/edit/<int:id>/', views.edit_rewards, name='edit_rewards'),
    path('create_reward/', views.create_reward, name='create_reward'),
    path('create_reward/edit/<int:id>/', views.edit_rewards, name='edit_rewards'),
    path("create_campaign/", views.campaign_view, name="create_campaign"), 
    path("create_campaign/edit/<int:id>/", views.edit_campaign, name="edit_campaign"),  
]