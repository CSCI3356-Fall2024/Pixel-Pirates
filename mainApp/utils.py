from datetime import timedelta

def generate_calendar(start_date, end_date, completed_dates):
    from datetime import timedelta
    import calendar

    days = []
    current_date = start_date
    while current_date <= end_date:
        days.append({
            'date': current_date,
            'completed': str(current_date) in completed_dates,
        })
        current_date += timedelta(days=1)

    # Pad the first week
    first_weekday = start_date.weekday()
    days = [{'date': None, 'completed': False}] * first_weekday + days

    # Split into weeks (7 days each)
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]
    return weeks
