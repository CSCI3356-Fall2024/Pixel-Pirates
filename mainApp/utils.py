import calendar
from datetime import date
from pinax.referrals.models import Referral
from django.urls import reverse
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