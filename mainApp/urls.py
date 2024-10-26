from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("confirmation/", views.confirmation_view, name="confirmation")

]