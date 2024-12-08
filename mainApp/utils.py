import calendar
from datetime import date
from pinax.referrals.models import Referral
from django.urls import reverse
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
import uuid

def generate_calendar(year, month, completed_dates):
    # Get the calendar for the month
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)  # Returns weeks with day numbers

    # Build the calendar structure with completed status
    calendar_weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:  # Days outside the month
                week_data.append({"date": None, "completed": False})
            else:
                day_date = date(year, month, day)
                week_data.append({
                    "date": day_date,
                    "completed": day_date.strftime("%Y-%m-%d") in completed_dates
                })
        calendar_weeks.append(week_data)
    
    return calendar_weeks

def assign_referral_to_user(profile):
    """Creates and assigns a referral to the profile."""
    referral = Referral.create(
        user=profile.username,  # Assuming `username` is linked to User
        redirect_to=reverse("home")
    )
    profile.referral = referral
    profile.save()

def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code

def get_user_by_referral_code(referral_code):
    try:
        profile = Profile.objects.get(referral_code=referral_code)
        return profile.username  # Assuming 'username' is a ForeignKey to User
    except ObjectDoesNotExist:
        print(f"No user found with referral code: {referral_code}")
        return None

def get_referring_user(referral_code):
    try:
        profile = Profile.objects.get(referral_code=referral_code)
        return profile.recommended_by  # Assuming 'recommended_by' is a ForeignKey to User
    except ObjectDoesNotExist:
        print(f"No referring user found for referral code: {referral_code}")
        return None