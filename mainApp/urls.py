from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("profile/", views.ProfileView, name="profile"),
    path("logout", views.logout_view)
]