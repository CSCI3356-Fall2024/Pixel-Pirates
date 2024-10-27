from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ProfileForm, CampaignForm
from .models import Profile, News
from django.db import IntegrityError

def google_login(request):
    return redirect('/auth/login/google-oauth2/')

def login(request):
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

@login_required
def profile_view(request):
    try:
        # Get the profile linked to the user
        profile = Profile.objects.get(username=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Creating a new profile.")
        profile = Profile(username=request.user)
        profile.save()
    
    required_fields = False
    if profile.name and profile.school and profile.major:
        required_fields = True 
    print(required_fields)

    if request.method == 'POST':
        # Bind the form to the POST data and files
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        # Print the POST data and form errors for debugging
        print("POST Data:", request.POST)  # Debugging: Check what data is submitted
        print("Form Errors:", form.errors)  # Debugging: Check for form validation errors

        if form.is_valid():
            try:
                if profile.name and profile.school and profile.major:
                    required_fields = True 
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('confirmation')  # Redirect to avoid duplicate form submissions
            except Exception as e:
                messages.error(request, f"Error saving profile: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile, 'required': required_fields})

def confirmation_view(request):  
    user = request.user
    profile = profile = Profile.objects.get(username=user)
    
    context = { 
        "profile": profile,
        "required" : True
    }
    return render(request, "confirmation.html", context)


def campaign_view(request):
    required = request.user.is_authenticated  
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('profile')  # Redirect to the profile page after successful save
    else:
        form = CampaignForm()  # Display an empty form on GET request

    return render(request, 'campaign.html', {'form': form, 'required': required})

def home(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if not (profile.name and profile.school and profile.major):
                return redirect('profile')
        except Profile.DoesNotExist:
            return redirect('profile')
    else:
        return redirect('login')

    context = {
        "required": True,
    }
    return render(request, 'home.html', context)

