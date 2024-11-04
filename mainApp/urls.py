from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("confirmation/", views.confirmation_view, name="confirmation"),
    path("campaign/", views.campaign_view, name="campaign"),
    path("home/", views.home_view, name="home"),
    path("actions/", views.actions_view, name="actions"),
    path("choose_action/", views.choose_action_view, name = "choose_action"),
    path("news/", views.news_view, name = "news"),
    path("rewards/", views.rewards_view, name='login')
]