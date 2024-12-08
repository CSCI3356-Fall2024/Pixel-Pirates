# Pixel_Pirates/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),  
    path("accounts/signup/", RedirectView.as_view(url='profile')), 
    path("", include("mainApp.urls")),  
    path("referrals/", include("pinax.referrals.urls", namespace="pinax_referrals")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
