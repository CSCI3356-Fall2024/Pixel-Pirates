from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile

def ProfileView(request):
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
