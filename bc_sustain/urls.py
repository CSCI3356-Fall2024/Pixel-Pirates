# define paths to different webpages
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileView, name='home'),
    path("profile/", views.ProfileView, name="profile"),
]