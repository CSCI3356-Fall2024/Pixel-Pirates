from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.dispatch import receiver
from django.db import IntegrityError
from django.db.models import F
from allauth.account.signals import user_logged_in
from datetime import timedelta, time
import json
from django.utils import timezone
from django.db.models import Window
from django.db.models.functions import Rank
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models.functions import RowNumber
from calendar import monthrange
from datetime import date

from .utils import *
from .models import *
from .forms import *

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
    campaign_form = CampaignForm()
    news_form = NewsForm()
    reward_form = RewardsForm()
    return render(request, 'choose_action.html', {
        'required': required,
        'campaign_form': campaign_form,
        'news_form': news_form,
        'reward_form': reward_form,
    })

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
    try:
        profile = request.user.profile
        if not (profile.name and profile.school and profile.major):
            return redirect('profile')
        required = True
    except Profile.DoesNotExist:
        return redirect('profile')

        # Update the rank for the current user
    all_profiles = (
        Profile.objects.annotate(rank=Window(
            expression=RowNumber(),
            order_by=[F('points').desc(), F('last_points_update').asc()]
        ))
        .order_by('rank')
    )

    leaderboard_data = []
    for user in all_profiles[:50]:
        # Calculate rank change
        rank_change = 0 # Change default to 0
        if user.previous_rank is not None:
            rank_change = user.previous_rank - user.rank

        # Update the user's previous rank
        user.rank_change = rank_change
        user.previous_rank = user.rank
        user.save(update_fields=['rank_change', 'previous_rank'])

        leaderboard_data.append({
            'id': user.id,
            'name': user.name,
            'points': user.points,
            'picture': user.picture.url if user.picture else None,
            'rank': user.rank,
            'rank_change': rank_change,  # Changed so dealt with default in above lines
            'is_current_user': user.id == profile.id,
            #'abs_rank_change': abs(rank_change) if rank_change is not None else 0,  # Calculate absolute rank change
        })

    # Correctly get the rank for the current user
    user_rank = None
    for user in all_profiles:
        if user.id == profile.id:
            user_rank = user.rank
            break

    total_users = Profile.objects.count()
    user_in_top_50 = user_rank <= 50  # Check if the user is in the top 50

    # User info dictionary
    user_info = {
        'rank': user_rank,
        'name': profile.name,
        'points': profile.points,
        'picture': profile.picture.url if profile.picture else None,
    }

    # Top 3 users for leaderboard display
    top_3_users = leaderboard_data[:3]
    top_3_names = [user['name'] for user in top_3_users]
    top_3_points = [user['points'] for user in top_3_users]

    # Get news and campaign items for the homepage
    news_items = News.objects.all()
    campaign_items = Campaign.objects.all()

    # Determine motivational message based on correct user rank
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
    }

    return render(request, 'home.html', context)

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect('home')  

    users = User.objects.all()
    context = {
        'users': users,
        'required': True  
    }

    return render(request, 'manage_users.html', context)

@user_passes_test(lambda u: u.is_superuser)  # Only superusers can access this
def toggle_supervisor(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        user.is_superuser = False
    else:
        user.is_superuser = True
    user.save()
    return redirect('manage_users')  # Redirect to the manage users page

@login_required
def actions_view(request):
    user = request.user
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_date = today - timedelta(days=30)  # Start date for streak calendar

    # Get the month and year from the query parameters
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)

    try:
        # Ensure year and month are integers
        year = int(year)
        month = int(month)
    except ValueError:
        # Fallback to current year and month if conversion fails
        year = today.year
        month = today.month

    # Calculate the first and last days of the selected month
    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, monthrange(year, month)[1])

    # Get the previous and next month for navigation
    previous_month = month - 1 if month > 1 else 12
    previous_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    # Generate a list of months and years for the dropdown
    available_months_years = []
    for y in range(today.year - 2, today.year + 3):  # 2 years before and after the current year
        for m in range(1, 13):
            available_months_years.append({
                "value": f"{y}-{m:02d}",
                "label": f"{date(y, m, 1).strftime('%B %Y')}"
            })

    # Check for mandatory profile fields
    try:
        profile = user.profile
        if not (profile.name and profile.school and profile.major and profile.graduation_year):
            return redirect('profile')
    except Profile.DoesNotExist:
        return redirect('profile')

    # Retrieve tasks
    static_tasks = DailyTask.objects.filter(user=user, is_static=True)
    dynamic_tasks = DailyTask.objects.filter(user=user, is_static=False, completion_criteria__action_date=str(today))
    weekly_tasks = WeeklyTask.objects.filter(user=user, start_date=start_of_week, end_date=end_of_week)

    # Calculate daily progress
    total_tasks = static_tasks.count() + dynamic_tasks.count()
    completed_tasks = (
        static_tasks.filter(completed=True).count() +
        dynamic_tasks.filter(completed=True).count()
    )
    daily_progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Completed dates for streaks
    streak_days = DailyTask.objects.filter(
        user=user,
        completed=True,
        is_static=False,
        completion_criteria__action_date__gte=str(start_date),
        completion_criteria__action_date__lte=str(today)
    ).values_list('completion_criteria__action_date', flat=True)
    completed_dates = set(streak_days)

    # Calculate streak status (current streak)
    current_streak = 0
    date_pointer = today

    while date_pointer.strftime("%Y-%m-%d") in completed_dates:
        current_streak += 1
        date_pointer -= timedelta(days=1)

    # Calculate streak multiplier
    streak_multiplier = 1 + (current_streak // 7) * 0.1  # Increment multiplier by 0.1 for each 7 days

    # Update the profile dynamically
    user.profile.streak_status = current_streak
    user.profile.streak_bonus = round(streak_multiplier, 1)  # Round multiplier to 1 decimal
    user.profile.save()

    # Adjust streak description for singular/plural
    streak_description = (
        f"{current_streak} Day Streak"
        if current_streak == 1
        else f"{current_streak} Days Streak"
    )

    # Generate calendar
    calendar_weeks = generate_calendar(year, month, completed_dates)

    # Referral task
    referral_task, created = ReferralTask.objects.get_or_create(referrer=user, completed=False, defaults={'points': 10})

    context = {
        'profile': user.profile,
        'static_tasks': static_tasks,
        'dynamic_tasks': dynamic_tasks,
        'weekly_tasks': weekly_tasks,  # Add weekly tasks back to the context
        'referral_task': referral_task,
        'daily_progress_percentage': daily_progress_percentage,
        'calendar_weeks': calendar_weeks,
        'completed_dates': completed_dates,
        'month_year_options': available_months_years,
        'current_month_year': f"{year}-{month:02d}",
        'current_month': first_day_of_month.strftime("%B"),
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
        'streak_description': streak_description,
        'required': True,
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
@login_required
def complete_task(request, task_id):
    if request.method == "POST":
        try:
            # Try finding the task in DailyTask, WeeklyTask, or ReferralTask
            task = DailyTask.objects.filter(user=request.user).get(id=task_id)
        except DailyTask.DoesNotExist:
            try:
                task = WeeklyTask.objects.filter(user=request.user).get(id=task_id)
            except WeeklyTask.DoesNotExist:
                try:
                    task = ReferralTask.objects.filter(referrer=request.user).get(id=task_id)
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
        points_to_add = getattr(task, 'points', getattr(task, 'points_awarded', 0))
        user_profile = getattr(task, 'user', getattr(task, 'referrer', None)).profile
        user_profile.points += points_to_add
        user_profile.save()

        return JsonResponse({"success": True, "points_added": points_to_add}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)