import datetime


def get_holidays(country, year):
    """
    Returns a set of (month, day) tuples for the holidays of the specified country and year.

    Currently, supports 'Japan' with fixed holidays and substitute holiday logic.

    Args:
        country (str): The name of the country (e.g., 'Japan').
        year (int): The year to calculate holidays for.

    Returns:
        set: A set of tuples (month, day) representing the holidays.
    """
    holidays = set()

    if country.lower() == 'japan':
        # Fixed holidays
        holidays.add((1, 1))  # New Year's Day

        # Coming of Age Day (2nd Monday of January)
        # Happy Monday System (since 2000)
        first_jan = datetime.date(year, 1, 1)
        # weekday(): 0=Mon, 6=Sun
        first_monday_day = 1 + (0 - first_jan.weekday() + 7) % 7
        second_monday_day = first_monday_day + 7
        holidays.add((1, second_monday_day))

        holidays.add((2, 11))  # National Foundation Day
        holidays.add((4, 29))  # Showa Day
        holidays.add((5, 3))  # Constitution Memorial Day
        holidays.add((5, 4))  # Greenery Day
        holidays.add((5, 5))  # Children's Day
        holidays.add((11, 3))  # Culture Day
        holidays.add((11, 23))  # Labor Thanksgiving Day

        # Emperor's Birthday
        if year <= 1988:
            holidays.add((4, 29))  
        elif 1989 <= year <= 2018:
            holidays.add((12, 23))  
        elif year >= 2020:
            holidays.add((2, 23))
        
        # Simple Logic for Vernal/Autumnal Equinox (Approximate)
        # These change slightly, but for a simple CLI tool, approximations or specific year logic might be needed.
        # Keeping it simple with fixed dates for now as requested for "New Year".

        # Substitute Holiday Logic
        # Convert to list of date objects to handle weekday checks and date math
        holiday_dates = set()
        for month, day in holidays:
            try:
                holiday_dates.add(datetime.date(year, month, day))
            except ValueError:
                continue

        # Iterate over original holidays to check for Sunday rule
        # We use a sorted list of the original holidays to process them in order,
        # though strictly speaking the order doesn't change the outcome of the logic
        # as long as we check against the full set of holidays (including previously added substitutes?
        # No, usually substitutes don't chain from other substitutes, but they do chain from fixed holidays overlapping).
        # Actually, if we have Sun (Holiday 1), Mon (Holiday 2), the substitute for Holiday 1 goes to Tue.
        # If Tue was also a fixed holiday, it would go to Wed.

        # Use a copy to iterate so we don't modify what we are iterating over in a way that affects logic wrongly,
        # although adding to 'holiday_dates' is fine as we only care if 'candidate' is occupied.
        sorted_original_dates = sorted(list(holiday_dates))

        for h_date in sorted_original_dates:
            if h_date.weekday() == 6:  # Sunday
                candidate = h_date + datetime.timedelta(days=1)
                while candidate in holiday_dates:
                    candidate += datetime.timedelta(days=1)
                holiday_dates.add(candidate)

        # Update holidays set with any new substitutes
        holidays = set((d.month, d.day) for d in holiday_dates)

    return holidays
