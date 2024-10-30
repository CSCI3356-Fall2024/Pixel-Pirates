from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ProfileForm, CampaignForm
from .models import Profile, News
from django.db import IntegrityError
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
import json

@receiver(user_logged_in)
def handle_login(sender, request, user, **kwargs):
    """Redirect new users to profile page and existing users to home."""
    try:
        # Check if the user has a profile
        Profile.objects.get(username=user)
        # If profile exists, redirect to home
        request.session['login_redirect'] = '/home/'
    except Profile.DoesNotExist:
        # Redirect new users to profile creation page
        request.session['login_redirect'] = '/profile/'

def login_view(request):
    """Handle post-login redirection."""
    if request.user.is_authenticated:
        # Redirect based on session value set during login
        return redirect(request.session.pop('login_redirect', '/home/'))
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

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
    if profile.name and profile.school and profile.major and profile.graduation_year:
        required_fields = True 

    if request.method == 'POST':
        # Bind the form to the POST data and files
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        # Print the POST data and form errors for debugging
        print("POST Data:", request.POST)  # Debugging: Check what data is submitted
        print("Form Errors:", form.errors)  # Debugging: Check for form validation errors

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile updated successfully!")
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

# def home(request):
#     if request.user.is_authenticated:
#         try:
#             profile = request.user.profile
#             if not (profile.name and profile.school and profile.major):
#                 return redirect('profile')
#         except Profile.DoesNotExist:
#             return redirect('profile')
#     else:
#         return redirect('login')

#     context = {
#         "required": True,
#     }
#     return render(request, 'home.html', context)

def home(request):
    if request.user.is_authenticated: #logic for determining if user is signed in properly
        try:
            profile = request.user.profile
            if not (profile.name and profile.school and profile.major):
                return redirect('profile')
            required = True
        except Profile.DoesNotExist:
            return redirect('profile')
    else:
        return redirect('login')

    # fetch top 50 users
    leaderboard_data = Profile.objects.order_by('-points')[:50]
    # fetch news items (doesn't work)
    news_items = News.objects.all()
    # data for barchart
    top_3_users = leaderboard_data[:3]
    top_3_names = [user.name for user in top_3_users]
    top_3_points = [user.points for user in top_3_users]
    #rank and motivational message
    total_users = Profile.objects.count()
    user_rank = Profile.objects.filter(points__gt=profile.points).count() + 1
    if user_rank <= 10:
        motivation_message = "Amazing job! You're in the Top 10. Keep up the good work!"
    elif user_rank <= 20:
        motivation_message = "Great work! You’re in the Top 20. Aim higher and reach the next milestone!"
    elif user_rank <= 50:
        motivation_message = "You’re in the Top 50! Keep going to break into the top ranks."
    elif user_rank <= 75:
        motivation_message = "You're doing well! Continue exploring and earning more points."
    else:
        motivation_message = "Check out the latest news and actions to boost your points and rise up the ranks!"
    
    context = {
        "required": True,
        "leaderboard_data": leaderboard_data,
        "news_items": news_items,
        "leaderboard_names": json.dumps(profile.name), 
        "leaderboard_points": json.dumps(profile.points),  
        "user_rank": user_rank,
        "motivation_message": motivation_message,
        "total_users": total_users,
        "top_3_names": json.dumps(top_3_names),  
        "top_3_points": json.dumps(top_3_points),
        "required": required,  
    }
    return render(request, 'home.html', context)


