from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from django.db import IntegrityError

def login(request):
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("/")

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
    return render(request, "campaign.html", {"required": required})
