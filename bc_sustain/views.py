from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProfileForm

# Create your views here.
def ProfileView(request):
    # check if the profile is filled, redirect if not
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("student_landing")
        else:
            form = ProfileForm()

    return render(request, "profile.html")