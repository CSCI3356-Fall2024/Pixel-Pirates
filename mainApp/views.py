from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile


def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

#Create your views here.
def profile_view(request):
    profile, created = Profile.objects.get_or_create(username=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = request.user
            profile.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form, "profile": profile})

def confirmation_view(request):  
    profile = Profile.objects.get(id=1) #the database must be empty in order for this work 
    user = request.user

    context = { 
        "profile": profile,
        "user": user
    }
    return render(request, "confirmation.html", context)
