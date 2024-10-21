from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from django.db import IntegrityError

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def profile_view(request):
    try:
        # Safely retrieve or create the user’s profile
        profile, created = Profile.objects.get_or_create(username=request.user)
    except IntegrityError:
        messages.error(request, "There was an issue retrieving your profile.")
        return redirect('home')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the form data if the email is unique
            try:
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')
            except IntegrityError:
                messages.error(request, "This email is already in use. Please try another one.")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})