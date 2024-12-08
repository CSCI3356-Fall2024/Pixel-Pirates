from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime
from django.dispatch import receiver
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from allauth.account.signals import user_logged_in
from datetime import timedelta, time
from django.utils import timezone
from django.db.models import Window
from django.db.models.functions import Rank
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models.functions import RowNumber
from calendar import monthrange
from django.shortcuts import render
from datetime import date
from django.db.models import Count

from .tasks import *
from .utils import *
from .models import *
from .forms import *
from .word_search import *

import json
import qrcode

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

def quiz_view(request):
    required = request.user.is_authenticated
    if request.method == 'POST':
        form = ArticleQuizForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = ArticleQuizForm()
    return render(request, 'create_quiz.html', {'form': form, 'required': required})

@login_required
def choose_action_view(request):
    required = request.user.is_authenticated
    if request.method == 'POST':
        campaign_form = CampaignForm(request.POST, request.FILES)
        news_form = NewsForm(request.POST, request.FILES)
        reward_form = RewardsForm(request.POST, request.FILES)
        quiz_form = ArticleQuizForm(request.POST, request.FILES)
        if campaign_form.is_valid():
            campaign_form.save()  # Save the form data to the database
            return redirect('home')  # Redirect to the home page after successful save
        if news_form.is_valid():
            news_form.save()
            return redirect('home') 
        if reward_form.is_valid():
            reward_form.save()
            return redirect('home')  
        if quiz_form.is_valid():
            quiz_form.save()
            return redirect('home') 
        return render(request, 'choose_action.html', {
            'required': required,
            'campaign_form': campaign_form,
            'news_form': news_form,
            'reward_form': reward_form,
            'quiz_form': quiz_form
        })
    else:
        campaign_form = CampaignForm()  # Display an empty form on GET request
        news_form = NewsForm()
        reward_form = RewardsForm()
        quiz_form = ArticleQuizForm()
        return render(request, 'choose_action.html', {
            'required': required,
            'campaign_form': campaign_form,
            'news_form': news_form,
            'reward_form': reward_form,
            'quiz_form': quiz_form
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


@login_required
def rewards_view(request):
    profile = request.user.profile 
    user = request.user
    now = timezone.now() #in UTC

    history_items = History.objects.filter(user=user)

    filtered_rewards = Rewards.objects.exclude(redeemed__user=user)
    available_rewards = []

    #checks if it's in the proper timeframe
    for reward in filtered_rewards:
        start_datetime = datetime.combine(reward.date_begin, reward.time_begin)
        end_datetime = datetime.combine(reward.date_end, reward.time_end)

        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone()) #adjusts to UTC 
        end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone()) #adjusts to UTC 

        if start_datetime <= now <= end_datetime:
            available_rewards.append(reward)

    filtered_redeem = Redeemed.objects.filter(user=user)
    redeemed_items = []

    #checks if it's in the proper timeframe 
    for redeem in filtered_redeem:
        start_datetime = datetime.combine(redeem.date_begin, redeem.time_begin)
        end_datetime = datetime.combine(redeem.date_end, redeem.time_end)

        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())

        if start_datetime <= now <= end_datetime:
            redeemed_items.append(redeem)

    redeemed_items = reversed(redeemed_items)
    available_rewards = reversed(available_rewards)
    history_items = reversed(history_items)

    #disregards timeframe for superuser
    if user.is_superuser: 
        available_rewards = filtered_rewards


    context = {
        'profile': profile,
        'redeemed_items': redeemed_items,
        'available_rewards': available_rewards,
        'history_items': history_items,
        'required': True
    }
    return render(request, 'rewards.html', context)

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
def redeem_reward(request):
    if request.method == 'POST':
        reward_id = request.POST.get('reward_id')
        reward = get_object_or_404(Rewards, id=reward_id)

        start = timezone.now() - timedelta(hours=5)
        start_day = start.date()

        end_day = start_day + timedelta(days=30)

        profile = request.user.profile
        profile.points -= reward.points
        reward.amount -= 1
        reward.save()
        profile.save()

        Redeemed.objects.create(
            user=request.user,
            rewards=reward,
            title=reward.title,
            date_begin=start_day,
            date_end=end_day,
            time_begin=time(0, 0),
            time_end=time(23,59),
            description=reward.description
        )

        History.objects.create(
            user=request.user,
            title=reward.title,
            date_created=start_day,
            time_created=start.time(), 
            points=reward.points,
            is_redeem=True,
            location=None,
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

    for user in all_profiles:
        user.previous_rank = user.current_rank
        user.current_rank = user.rank

        if user.previous_rank is not None:
            user.rank_change = user.previous_rank - user.current_rank
        else:
            user.rank_change = 0

        user.save(update_fields=['previous_rank', 'current_rank', 'rank_change'])

    # Refresh profile instance to ensure changes are loaded
    profile.refresh_from_db()

    # Use the latest rank to determine motivational message
    user_rank = profile.current_rank
    total_users = Profile.objects.count()
    user_in_top_50 = user_rank <= 50 if user_rank else False

    # Update the leaderboard data with persisted rank changes
    leaderboard_data = [
        {
            'id': user.id,
            'name': user.name,
            'points': user.points,
            'picture': user.picture.url if user.picture else None,
            'rank': user.current_rank,
            'rank_change': user.rank_change,
            'is_current_user': user.id == profile.id,
        }
        for user in all_profiles[:50]
    ]

    # Create user info dictionary
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
    user.is_superuser = not user.is_superuser  # Toggle superuser status
    user.save()
    return redirect('manage_users')

@login_required
def actions_view(request):
    user = request.user
    today = localtime().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_date = today - timedelta(days=30)  # Start date for streak calendar

    # Get the month and year from the query parameters
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)

    try:
        year = int(year)
        month = int(month)
    except ValueError:
        year, month = today.year, today.month

    # Calculate the first and last days of the selected month
    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, monthrange(year, month)[1])

    # Get the previous and next month for navigation
    previous_month = month - 1 if month > 1 else 12
    previous_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    # Generate a list of months and years for the dropdown
    available_months_years = [
        {"value": f"{y}-{m:02d}", "label": f"{date(y, m, 1).strftime('%B %Y')}"}
        for y in range(today.year - 2, today.year + 3) for m in range(1, 13)
    ]

    # Check for mandatory profile fields
    try:
        profile = user.profile
        if not (profile.name and profile.school and profile.major and profile.graduation_year):
            return redirect('profile')
    except AttributeError:
        return redirect('profile')

    # Retrieve tasks
    static_tasks = DailyTask.objects.filter(user=user, is_static=True)
    dynamic_tasks = DailyTask.objects.filter(user=user, is_static=False, completion_criteria__action_date=str(localtime().date()))
    weekly_tasks = WeeklyTask.objects.filter(user=user, start_date=start_of_week, end_date=end_of_week)

    task_word = None
    word_task = dynamic_tasks.filter(title="WORD OF THE DAY").first()
    feedback_message = ""

    # Handle the "WORD OF THE DAY" task
    if word_task:
        if not word_task.word:  # Only assign if not already set
            result = get_word_search_string()
            word_task.content = result[0]
            word_task.word = result[1]
            word_task.save()
        task_word = word_task.word

    # Handle forms
    photo_form = DailyTaskPhotoForm(request.POST, request.FILES or None)
    wod_form = WODAnswerForm(request.POST or None)

    if request.method == 'POST':
        # Handle "WORD OF THE DAY" answer
        if 'response' in request.POST and word_task:
            if wod_form.is_valid():
                answer = wod_form.cleaned_data['response']
                if answer.lower() == task_word.lower():
                    mark_task_completed(word_task)
                    return redirect("actions")

        # Handle photo upload for specific tasks
        if 'photo' in request.FILES:
            task_id = request.POST.get('task_id')
            if task_id:
                try:
                    task = DailyTask.objects.get(id=task_id, user=user)
                except DailyTask.DoesNotExist:
                    task = None

                if task and task.title in ["COMPOSTING", "RECYCLING", "PICTURE IN ACTION"]:
                    if photo_form.is_valid():
                        task.photo = photo_form.cleaned_data['photo']
                        mark_task_completed(task)
                        return redirect("actions")

    # Handle QR code for Green 2 Go
    green2go_task = static_tasks.filter(title="GREEN2GO CONTAINER").first()

    if green2go_task and not green2go_task.qr_code_link:
        # Generate a unique QR code link
        qr_code_link = f"{request.scheme}://{request.get_host()}/qrscan/complete/{green2go_task.id}/"
        green2go_task.qr_code_link = qr_code_link
        green2go_task.save()

        # Generate QR code image
        qr_code_image = qrcode.make(qr_code_link)
        qr_code_image.save(f"mainApp/static/qr_codes/task_{green2go_task.id}.png")

    # Calculate daily progress
    total_tasks = static_tasks.count() + dynamic_tasks.count()
    completed_tasks = (
        static_tasks.filter(completed=True).count() +
        dynamic_tasks.filter(completed=True).count()
    )
    daily_progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Get completed dates for streaks
    completed_dates = (
        DailyTask.objects.filter(
            user=user,
            completed=True,
            is_static=False,
            completion_criteria__action_date__gte=str(start_date),
            completion_criteria__action_date__lte=str(today)
        )
        .values('completion_criteria__action_date')
        .annotate(completed_task_count=Count('id'))
        .filter(completed_task_count=2)
        .values_list('completion_criteria__action_date', flat=True)
    )

    completed_dates_set = set(completed_dates)

    # Calculate streak status
    current_streak = 0
    date_pointer = today
    while date_pointer.strftime("%Y-%m-%d") in completed_dates_set:
        current_streak += 1
        date_pointer -= timedelta(days=1)

    streak_multiplier = 1 + (current_streak // 7) * 0.1

    # Update the profile dynamically
    user.profile.streak_status = current_streak
    user.profile.streak_bonus = round(streak_multiplier, 1)
    user.profile.save()

    streak_description = (
        f"{current_streak} Day Streak"
        if current_streak == 1
        else f"{current_streak} Days Streak"
    )

    # Generate calendar
    calendar_weeks = generate_calendar(year, month, completed_dates)

    # Referral task
    referral_task, _ = ReferralTask.objects.get_or_create(referrer=user, completed=False, defaults={'points': 10})

    context = {
        'profile': user.profile,
        'static_tasks': static_tasks,
        'dynamic_tasks': dynamic_tasks,
        'weekly_tasks': weekly_tasks,
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
        'task_word': task_word,
        'photo_form': photo_form,
        'form': wod_form,
        'green2go_task': green2go_task,
    }
    return render(request, 'actions.html', context)

def mark_task_completed(task):
    """Marks a task as completed and updates the user's points."""
    task.completed = True
    task.save()
    profile = task.user.profile
    profile.points += task.points
    profile.save()

    start = timezone.now() - timedelta(hours=5)
    start_day = start.date()

    History.objects.create(
            user=task.user,
            title=task.title,
            date_created=start_day,
            time_created=start.time(), 
            points=task.points,
            is_redeem=False,
            location=None,
        )


#I don't think it's being used anymore 
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
        
        # Handle photo submission
        if 'photo' in request.FILES:
            task.photo = request.FILES['photo']
            # Save the photo to PhotoSubmission model
            PhotoSubmission.objects.create(user=request.user, task=task, photo=task.photo)

        # If the task is already completed, return a response
        if task.completed:
            return JsonResponse({"error": "Task already completed"}, status=400)

        # Mark the task as completed
        task.completed = True
        if hasattr(task, 'completion_date'):  # Set completion date if the field exists
            task.completion_date = localtime().date()
        task.save()

        # Add points to the user's profile
        points_to_add = getattr(task, 'points', getattr(task, 'points_awarded', 0))
        user_profile = getattr(task, 'user', getattr(task, 'referrer', None)).profile
        user_profile.points += points_to_add
        user_profile.save()

        return JsonResponse({"success": True, "points_added": points_to_add}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def explore_view(request):
    # Filter DailyTask objects where photos exist
    photos = DailyTask.objects.filter(photo__isnull=False).order_by('-time_created')
    context = {
        'photos': photos,
        'required': True,
    }
    return render(request, 'explore.html', context)

@login_required
def article_quiz_view(request):
    print("test 1")
    quiz = ArticleQuiz.objects.latest('date_begin')
    form = ArticleQuizAnswerForm(request.POST)
    # Set the choices for each question in the view
    question_1_choices = [
        (quiz.q1_correct_answer, quiz.q1_correct_answer),
        (quiz.q1_false_answer_1, quiz.q1_false_answer_1),
        (quiz.q1_false_answer_2, quiz.q1_false_answer_2),
    ]
    random.shuffle(question_1_choices)  # Shuffle the choices
    
    question_2_choices = [
        (quiz.q2_correct_answer, quiz.q2_correct_answer),
        (quiz.q2_false_answer_1, quiz.q2_false_answer_1),
        (quiz.q2_false_answer_2, quiz.q2_false_answer_2),
    ]
    random.shuffle(question_2_choices)  # Shuffle the choices
    
    question_3_choices = [
        (quiz.q3_correct_answer, quiz.q3_correct_answer),
        (quiz.q3_false_answer_1, quiz.q3_false_answer_1),
        (quiz.q3_false_answer_2, quiz.q3_false_answer_2),
    ]
    random.shuffle(question_3_choices)  # Shuffle the choices
    
    form.fields['question_1_answer'].choices = question_1_choices
    form.fields['question_2_answer'].choices = question_2_choices
    form.fields['question_3_answer'].choices = question_3_choices

    feedback = {
        'question_1': '',
        'question_2': '',
        'question_3': ''
    }
    print("test 2")
    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        score = 0

        # Check each answer and provide feedback
        if form.cleaned_data['question_1_answer'] == quiz.q1_correct_answer:
            print("test")
            print(form.cleaned_data['question_1_answer'])
            score += 1
            feedback['question_1'] = 'Correct!'
        else:
            feedback['question_1'] = f'Incorrect! Try again!'

        if form.cleaned_data['question_2_answer'] == quiz.q2_correct_answer:
            score += 1
            feedback['question_2'] = 'Correct!'
        else:
            feedback['question_2'] = f'Incorrect! Try again!'

        if form.cleaned_data['question_3_answer'] == quiz.q3_correct_answer:
            score += 1
            feedback['question_3'] = 'Correct!'
        else:
            feedback['question_3'] = f'Incorrect! Try again!'

        if score == 3: 
            task = WeeklyTask.objects.filter(user=request.user, completed=False).first()
            if task:
                mark_task_completed(task)
                task.save()
        # Render the result page with the score and feedback
        return render(request, 'article_quiz.html', {
            'form': form,
            'quiz': quiz,
            'score': score,
            'feedback': feedback,
            'required': True
        })

    # Render the quiz page with the form
    return render(request, 'article_quiz.html', {'form': form, 'quiz': quiz, 'required': True})

# def run_daily_task(request):
#     """Manually trigger the daily tasks."""
#     generate_daily_tasks.delay()
#     return HttpResponse("Daily tasks started!")

# def run_weekly_task(request):
#     """Manually trigger the weekly tasks."""
#     generate_weekly_tasks.delay()
#     return HttpResponse("Weekly tasks started!")

# def schedule_tasks(request):
#     """Schedule daily and weekly tasks using django-celery-beat."""
#     # Daily tasks schedule
#     interval, _ = IntervalSchedule.objects.get_or_create(
#         every=1,
#         period=IntervalSchedule.MINUTES,
#     )

#     PeriodicTask.objects.get_or_create(
#         interval=interval,
#         name="Generate Daily Tasks",
#         task="mainApp.tasks.generate_daily_tasks",
#     )

#     # Weekly tasks schedule
#     weekly_interval, _ = IntervalSchedule.objects.get_or_create(
#         every=7,
#         period=IntervalSchedule.DAYS,
#     )

#     PeriodicTask.objects.get_or_create(
#         interval=weekly_interval,
#         name="Generate Weekly Tasks",
#         task="mainApp.tasks.generate_weekly_tasks",
#     )

#     return HttpResponse("Daily and Weekly tasks scheduled!")

# def index(request):
#     my_task.delay()
#     return HttpResponse("Task Started")

# def schedule_task(request):
#     interval, _ = IntervalSchedule.objects.get_or_create(
#         every=1,
#         period=IntervalSchedule.MINUTES,
#     )

#     PeriodicTask.objects.get_or_create(
#         interval=interval,
#         name="My Tasks",
#         task="mainApp.tasks.generate_daily_tasks",
#     )

#     return HttpResponse("Task Scheduled")