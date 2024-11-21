from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
<<<<<<< HEAD
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.dispatch import receiver
=======
from .forms import ProfileForm, CampaignForm, NewsForm, RewardsForm
from .models import Profile, News, Campaign, Rewards
>>>>>>> origin
from django.db import IntegrityError
from django.db.models import F
from allauth.account.signals import user_logged_in
from datetime import timedelta
import json

from .models import (
    Profile,
    News,
    Campaign,
    DailyTask,
    WeeklyTask,
    ReferralTask,
)

from .forms import (
    ProfileForm,
    CampaignForm,
    NewsForm,
)

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
    # Retrieve or create a profile for the logged-in user
    profile, created = Profile.objects.get_or_create(username=request.user)

    # If the profile is newly created, initialize required fields to ensure the user can edit it
    if created:
        messages.info(request, "Welcome! Please complete your profile.")
    
    # Check if the profile has all required fields filled
    required_fields = bool(
        profile.name and profile.school and profile.major and profile.graduation_year
    )

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile updated successfully!")
                
                # Recheck required fields after saving
                required_fields = bool(
                    profile.name and profile.school and profile.major and profile.graduation_year
                )

                # Redirect to refresh the page and reflect changes
                return redirect('profile')
            except Exception as e:
                messages.error(request, f"Error saving profile: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        'profile.html',
        {'form': form, 'profile': profile, 'required': required_fields}
    )

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

@login_required
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

def rewards_view(request):
    profile = request.user.profile 
    campaign_items = Campaign.objects.all()

    context = {
        'profile': profile,
        'campaign_items': campaign_items,
        'required': True
    }
    return render(request, 'rewards.html', context)


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
    user = request.user
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
   # Check for mandatory profile fields
    try:
        profile = user.profile
        if not (profile.name and profile.school and profile.major and profile.graduation_year):
            return redirect('profile')
    except Profile.DoesNotExist:
        return redirect('profile')

    # Retrieve static tasks (e.g., recurring daily tasks)
    static_tasks = DailyTask.objects.filter(user=user, is_static=True)
    
    # Retrieve dynamic tasks for today (e.g., changing daily tasks)
    dynamic_tasks = DailyTask.objects.filter(user=user, is_static=False, completion_criteria__action_date=str(today))

    #weekly tasks 
    weekly_tasks = WeeklyTask.objects.filter(user=user, start_date=start_of_week, end_date=end_of_week)

     # Calculate progress
    total_tasks = static_tasks.count() + dynamic_tasks.count() + weekly_tasks.count()
    completed_tasks = (
        static_tasks.filter(completed=True).count() +
        dynamic_tasks.filter(completed=True).count() +
        weekly_tasks.filter(completed=True).count()
    )
    daily_progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Fetch or create an open referral task for the current user
    referral_task, created = ReferralTask.objects.get_or_create(referrer=request.user, completed=False, defaults={'points': 10})

    context = {
        'profile': profile,
        'static_tasks': static_tasks,
        'dynamic_tasks': dynamic_tasks,
        'weekly_tasks': weekly_tasks,
        'referral_task': referral_task,
        'daily_progress_percentage': daily_progress_percentage,
        'required': True
    }
    return render(request, 'actions.html', context)

# def actions_view(request):
#     # Ensure the user has a complete profile
#     profile = request.user.profile
#     if not (profile.name and profile.school and profile.major and profile.graduation_year):
#         return redirect('profile')

#     # Get today's date for filtering daily tasks
#     today = timezone.now().date()

#     # Retrieve daily tasks associated with the user
#     daily_tasks_different = DailyTask.objects.filter(user=request.user, title__in=["WORD OF THE DAY", "PICTURE IN ACTION"])
#     daily_tasks_same = DailyTask.objects.filter(user=request.user, title__in=["COMPOSTING", "RECYCLING", "GREEN2GO CONTAINER"])

#     # Retrieve the weekly task for the user (assuming one weekly task per user)
#     weekly_task = WeeklyTask.objects.filter(user=request.user).first()

#     # Retrieve an active referral task if available
#     referral_task = ReferralTask.objects.filter(referrer=request.user, completed=False).first()

#     # Calculate daily progress as a percentage based on completed tasks
#     total_daily_tasks = daily_tasks_different.count() + daily_tasks_same.count()
#     completed_daily_tasks = daily_tasks_different.filter(completed=True).count() + daily_tasks_same.filter(completed=True).count()
#     daily_progress_percentage = (completed_daily_tasks / total_daily_tasks * 100) if total_daily_tasks > 0 else 0

#     # Example static data for calendar weeks; ideally, this would be dynamically generated
#     calendar_weeks = [
#         [{'day': 1, 'is_today': False, 'is_streak': False}, {'day': 2, 'is_today': True, 'is_streak': True}, ...],
#     ]

#     # Pass all data to the template
#     context = {
#         'profile': profile,
#         'daily_tasks_different': daily_tasks_different,
#         'daily_tasks_same': daily_tasks_same,
#         'weekly_task': weekly_task,
#         'referral_task': referral_task,
#         'daily_progress_percentage': daily_progress_percentage,
#         'calendar_weeks': calendar_weeks,
#     }
#     return render(request, 'actions.html', context)

@csrf_exempt
def complete_task(request, task_id):
    if request.method == "POST":
        try:
            # Try finding the task in DailyTask, WeeklyTask, or ReferralTask
            task = DailyTask.objects.get(id=task_id)
        except DailyTask.DoesNotExist:
            try:
                task = WeeklyTask.objects.get(id=task_id)
            except WeeklyTask.DoesNotExist:
                try:
                    task = ReferralTask.objects.get(id=task_id)
                except ReferralTask.DoesNotExist:
                    return JsonResponse({"error": "Task not found"}, status=404)

        # If the task is already completed, return a response
        if task.completed:
            return JsonResponse({"error": "Task already completed"}, status=400)

        # Mark the task as completed
        task.completed = True
        if hasattr(task, 'completion_date'):  # Set completion date if the field exists
            task.completion_date = now().date()
        task.save()

        # Add points to the user's profile
        points_to_add = task.points if hasattr(task, 'points') else task.points_awarded
        user_profile = task.user.profile if hasattr(task, 'user') else task.referrer.profile
        user_profile.points += points_to_add
        user_profile.save()

        return JsonResponse({"success": True, "points_added": points_to_add}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)