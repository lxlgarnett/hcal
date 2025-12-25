"""
Module for calculating holidays.
"""
import datetime


def get_specific_monday(year, month, ordinal):
    """
    Finds the specific Monday of a month (e.g., 2nd Monday).

    Args:
        year (int): The year.
        month (int): The month.
        ordinal (int): The ordinal number of the Monday (e.g., 1 for 1st, 2 for 2nd).

    Returns:
        int: The day of the month.
    """
    # Get the first day of the month
    first_day = datetime.date(year, month, 1)

    # Calculate the day of the first Monday
    # weekday(): 0=Monday, 6=Sunday
    # (0 - first_day.weekday() + 7) % 7 gives days to add to reach the first Monday
    days_to_first_monday = (0 - first_day.weekday() + 7) % 7
    first_monday_day = 1 + days_to_first_monday

    # Calculate the specific Monday
    specific_monday_day = first_monday_day + (ordinal - 1) * 7

    return specific_monday_day


def _get_japan_fixed_holidays(year):
    """Returns a set of fixed date holidays for Japan."""
    holidays = set()
    if year >= 1955:
        holidays.add((1, 1))   # New Year's Day
        holidays.add((5, 3))   # Constitution Memorial Day
        holidays.add((5, 5))   # Children's Day
        holidays.add((11, 3))  # Culture Day
        holidays.add((11, 23)) # Labor Thanksgiving Day

    if year >= 1967:
        holidays.add((2, 11))  # National Foundation Day

    if year >= 2007:
        holidays.add((4, 29))  # Showa Day

    return holidays


def _get_japan_variable_holidays(year):
    """Returns a set of variable date holidays for Japan."""
    holidays = set()

    # Coming of Age Day
    if year >= 2000:
        holidays.add((1, get_specific_monday(year, 1, 2)))
    else:
        holidays.add((1, 15))

    # Emperor's Birthday
    if 1955 <= year <= 1988:
        holidays.add((4, 29))
    elif 1989 <= year <= 2018:
        holidays.add((12, 23))
    elif year >= 2020:
        holidays.add((2, 23))

    # Greenery Day
    if 1989 <= year <= 2006:
        holidays.add((4, 29))
    elif year >= 2007:
        holidays.add((5, 4))

    # Sports Day
    if 1966 <= year <= 1999:
        holidays.add((10, 10))
    elif year >= 2000:
        if year == 2020:
            holidays.add((7, 24))
        elif year == 2021:
            holidays.add((7, 23))
        else:
            holidays.add((10, get_specific_monday(year, 10, 2)))

    return holidays


def _apply_citizens_holiday(holiday_dates, year):
    """Applies the Citizens' Holiday (sandwich rule)."""
    if year < 1986:
        return

    sorted_dates = sorted(list(holiday_dates))
    sandwiches = []
    for i in range(len(sorted_dates) - 1):
        date_1 = sorted_dates[i]
        date_2 = sorted_dates[i + 1]
        if (date_2 - date_1).days == 2:
            sandwich_date = date_1 + datetime.timedelta(days=1)
            # If it's not Sunday and not already a holiday
            if sandwich_date.weekday() != 6:
                sandwiches.append(sandwich_date)
    for s_date in sandwiches:
        holiday_dates.add(s_date)


def _apply_substitute_holiday(holiday_dates):
    """Applies the substitute holiday rule (Monday following Sunday)."""
    sorted_original_dates = sorted(list(holiday_dates))

    for h_date in sorted_original_dates:
        if h_date.weekday() == 6:  # Sunday
            candidate = h_date + datetime.timedelta(days=1)
            while candidate in holiday_dates:
                candidate += datetime.timedelta(days=1)
            holiday_dates.add(candidate)


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
        holidays.update(_get_japan_fixed_holidays(year))
        holidays.update(_get_japan_variable_holidays(year))

        # Convert to date objects for advanced logic
        holiday_dates = set()
        for month, day in holidays:
            try:
                holiday_dates.add(datetime.date(year, month, day))
            except ValueError:
                continue

        _apply_citizens_holiday(holiday_dates, year)
        _apply_substitute_holiday(holiday_dates)

        # Convert back to (month, day) tuples
        holidays = set((d.month, d.day) for d in holiday_dates)

    return holidays
