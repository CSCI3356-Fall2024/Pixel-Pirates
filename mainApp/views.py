from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ProfileForm, CampaignForm, NewsForm, RewardsForm
from .models import Profile, News, Campaign, Rewards, Redeemed
from django.db import IntegrityError
from django.db.models import F
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
import json
from django.utils import timezone
from datetime import timedelta, time 

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
    #messages.success(request, "You have been logged out successfully.")
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

@login_required
def choose_action_view(request):
    required = request.user.is_authenticated
    return render(request, 'choose_action.html', {'required': required})

def campaign_view(request):
    required = request.user.is_authenticated  
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('home')  # Redirect to the home page after successful save
    else:
        form = CampaignForm()  # Display an empty form on GET request

    return render(request, 'create_campaign.html', {'form': form, 'required': required})

def news_view(request):
    required = request.user.is_authenticated
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = NewsForm()
    return render(request, 'create_news.html', {'form': form, 'required': required})

def create_reward(request):
    required = request.user.is_authenticated
    if request.method == 'POST':
        form = RewardsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = RewardsForm()
    return render(request, 'create_reward.html', {'form': form, 'required': required})

@login_required
def rewards_view(request):
    profile = request.user.profile 
    user = request.user
    # Get titles of rewards redeemed by the user
    redeemed_titles = Redeemed.objects.filter(user=user).values_list('title', flat=True)
    # Filter rewards not redeemed by the user
    available_rewards = Rewards.objects.exclude(title__in=redeemed_titles)

    redeemed_items = Redeemed.objects.filter(user=user)

    context = {
        'profile': profile,
        'redeemed_items': redeemed_items,
        'available_rewards': available_rewards,
        'required': True
    }
    return render(request, 'rewards.html', context)

@login_required
def redeem_reward(request):
    if request.method == 'POST':
        reward_id = request.POST.get('reward_id')
        reward = get_object_or_404(Rewards, id=reward_id)

        start_day = timezone.now().date()
        end_day = start_day + timedelta(days=30)

        profile = request.user.profile
        profile.points -= reward.points
        profile.save()

        Redeemed.objects.create(
            user=request.user,
            title=reward.title,
            date_begin=start_day,
            date_end=end_day,
            time_begin=time(0, 0),
            time_end=time(23,59),
            description=reward.description
        )
        return redirect('rewards')


@login_required
def edit_news(request, id):
    news_item = get_object_or_404(News, id=id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'edit_news.html', {'form': form, 'news_item': news_item, 'required': True})

@login_required
def edit_campaign(request, id):
    campaign_item = get_object_or_404(Campaign, id=id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign_item)
        if form.is_valid():
            form.save()
            next_url = request.GET.get('next')
            return redirect(next_url) if next_url else redirect('home')
    else:
        form = CampaignForm(instance=campaign_item)
    
    return render(request, 'edit_campaign.html', {'form': form, 'campaign_item': campaign_item, 'required': True})

# edit_rewards here
@login_required
def edit_rewards(request, id):
    rewards_item = get_object_or_404(Rewards, id=id)
    if request.method == 'POST':
        form = RewardsForm(request.POST, request.FILES, instance=rewards_item)
        if form.is_valid():
            form.save()
    else:
        form = RewardsForm(instance=rewards_item)
    
    return render(request, 'edit_rewards.html', {'form': form, 'rewards_item': rewards_item, 'required': True})

@login_required
def home_view(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if not (profile.name and profile.school and profile.major):
                return redirect('profile')
            required = True
        except Profile.DoesNotExist:
            return redirect('profile')
    else:
        return redirect('login')

    leaderboard_data = Profile.objects.order_by('-points').annotate(
        rank=F('points')
    )[:50]

    top_3_users = leaderboard_data[:3]
    top_3_names = [user.name for user in top_3_users]
    top_3_points = [user.points for user in top_3_users]

    news_items = News.objects.all()
    campaign_items = Campaign.objects.all()

    total_users = Profile.objects.count()
    user_rank = Profile.objects.filter(points__gt=profile.points).count() + 1

    user_rank = Profile.objects.filter(points__gt=profile.points).count() + 1
    user_info = {
        'rank': user_rank,
        'name': profile.name,
        'points': profile.points,
        'picture': profile.picture.url if profile.picture else None,
    }

    leaderboard_data = Profile.objects.order_by('-points')[:50]
    user_rank = Profile.objects.filter(points__gt=profile.points).count() + 1
    user_in_top_50 = user_rank <= 50  # Check if the user is in the top 50

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
        "user_rank": user_rank,
        "motivation_message": motivation_message,
        "total_users": total_users,
        "top_3_names": json.dumps(top_3_names),
        "top_3_points": json.dumps(top_3_points),
        "news_items": news_items,
        "campaign_items": campaign_items,
        "leaderboard_names": json.dumps(profile.name), 
        "leaderboard_points": json.dumps(profile.points),
        "user_in_top_50": user_in_top_50,
        "user_info": user_info,
        "required": required,  
    }
    return render(request, 'home.html', context)

@login_required
def actions_view(request):
    profile = request.user.profile

    if not (profile.name and profile.school and profile.major and profile.graduation_year):
        return redirect('profile')  

    daily_tasks = [
        {'name': 'Word of the Day', 'points': 20, 'status': 'completed'},
        {'name': 'Picture in Action', 'points': 20, 'status': 'open'},
        {'name': 'Composting', 'points': 5, 'status': 'completed'},
        {'name': 'Recycling', 'points': 5, 'status': 'open'},
        {'name': 'Green2Go Container', 'points': 15, 'status': 'open'},
    ]
    weekly_task = {'name': 'Article Quiz', 'points': 15, 'status': 'in progress'}
    referral_task = {'name': 'Refer a Friend', 'points': 10, 'status': 'open'}
    daily_progress_percentage = 60 

    calendar_weeks = [
        [{'day': 1, 'is_today': False, 'is_streak': False}, ...],  
    ]

    context = {
        'daily_tasks': daily_tasks,
        'weekly_task': weekly_task,
        'referral_task': referral_task,
        'daily_progress_percentage': daily_progress_percentage,
        'calendar_weeks': calendar_weeks,
        'required': True
    }
    return render(request, 'actions.html', context)