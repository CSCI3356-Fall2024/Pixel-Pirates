from django.urls import path
from .views import home, profile_view, logout_view

urlpatterns = [
    path("", home, name="home"),
    path("profile/", profile_view, name="profile"),
    path("logout/", logout_view, name="logout")
]