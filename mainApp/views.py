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
        # Retrieve or create the profile for the logged-in user
        profile, created = Profile.objects.get_or_create(
            username=request.user,
            defaults={
                'bc_email': request.user.email,
                'name': f"{request.user.first_name} {request.user.last_name}".strip()
            }
        )

        if created:
            messages.success(request, "Profile created successfully!")
        
        required_fields = False
        if profile.name and profile.school and profile.major:
            required_fields = True 
        print(required_fields)

    except IntegrityError:
        messages.error(request, "There was an issue creating your profile.")
        return redirect('home')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                if profile.name and profile.school and profile.major:
                    required_fields = True 
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')
            except IntegrityError:
                messages.error(request, "This email is already in use. Please try another one.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    # Pass the user and profile objects to the template
    return render(request, 'profile.html', {
        'form': form,
        'profile': profile,
        'user': request.user,  # Pass the user object
        'required': required_fields,
    })

def confirmation_view(request):  
    user = request.user
    profile = profile = Profile.objects.get(username=user)

    context = { 
        "profile": profile
    }
    return render(request, "confirmation.html", context)
