from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("confirmation/", views.confirmation_view, name="confirmation"),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('toggle-supervisor/<int:user_id>/', views.toggle_supervisor, name='toggle_supervisor'),
    path("home/", views.home_view, name="home"),
    path("actions/", views.actions_view, name="actions"),
    path("choose_action/", views.choose_action_view, name = "choose_action"),
    path('tasks/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('create_news/edit/<int:id>/', views.edit_news, name='edit_news'),
    path("rewards/", views.rewards_view, name='rewards'),
    path("redeem_reward/", views.redeem_reward, name='redeem_reward'),
    path('rewards/edit/<int:id>/', views.edit_rewards, name='edit_rewards'),
    path('create_reward/edit/<int:id>/', views.edit_rewards, name='edit_rewards'),
    path("create_campaign/edit/<int:id>/", views.edit_campaign, name="edit_campaign"),  
    # path("run-daily-tasks/", views.run_daily_task, name="run_daily_tasks"),
    # path("run-weekly-tasks/", views.run_weekly_task, name="run_weekly_tasks"),
    # path("schedule-tasks/", views.schedule_tasks, name="schedule_tasks"),
    # path("index/", views.index, name="index"),
    # path("schedule/", views.schedule_task, name="schedule")
]