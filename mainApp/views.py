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

# Create your views here.
def profile_view(request):
    profile, created = Profile.objects.get_or_create(username=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print(form)
            #profile = form.save()
            #profile.username = request.user
            #profile.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile_test.html", {"form": form, "profile": profile})
