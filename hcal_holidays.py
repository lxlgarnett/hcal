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


def _get_coming_of_age_day(year):
    """Returns Coming of Age Day."""
    if year >= 2000:
        return (1, get_specific_monday(year, 1, 2))
    return (1, 15)


def _get_emperor_birthday(year):
    """Returns Emperor's Birthday."""
    if 1955 <= year <= 1988:
        return (4, 29)
    if 1989 <= year <= 2018:
        return (12, 23)
    if year >= 2020:
        return (2, 23)
    return None


def _get_marine_day(year):
    """Returns Marine Day (Sea Day)."""
    if 1996 <= year <= 2002:
        return (7, 20)
    if year >= 2003:
        if year == 2020:
            return (7, 23)
        if year == 2021:
            return (7, 22)
        return (7, get_specific_monday(year, 7, 3))
    return None


def _get_greenery_day(year):
    """Returns Greenery Day."""
    if 1989 <= year <= 2006:
        return (4, 29)
    if year >= 2007:
        return (5, 4)
    return None


def _get_vernal_equinox_day(year):
    """
    Returns Vernal Equinox Day (Shunbun no Hi).
    Calculated using astronomical approximation.
    """
    if year < 1955:
        return None

    if 1955 <= year <= 1979:
        constant = 20.8357
    elif 1980 <= year <= 2099:
        constant = 20.8431
    else:
        # Fallback or future expansion; currently not strictly defined by this formula
        return None

    day = int(constant + 0.242194 * (year - 1980)) - int((year - 1980) // 4)
    return (3, day)


def _get_sports_day(year):
    """Returns Sports Day."""
    if 1966 <= year <= 1999:
        return (10, 10)
    if year >= 2000:
        if year == 2020:
            return (7, 24)
        if year == 2021:
            return (7, 23)
        return (10, get_specific_monday(year, 10, 2))
    return None


def _get_mountain_day(year):
    """Returns Mountain Day."""
    if year < 2016:
        return None
    if year == 2020:
        return (8, 10)
    if year == 2021:
        return (8, 8)
    return (8, 11)


def _get_japan_variable_holidays(year):
    """Returns a set of variable date holidays for Japan."""
    holidays = set()

    # Coming of Age Day
    holidays.add(_get_coming_of_age_day(year))

    # Emperor's Birthday
    emp_bday = _get_emperor_birthday(year)
    if emp_bday:
        holidays.add(emp_bday)

    # Marine Day (Sea Day)
    marine_day = _get_marine_day(year)
    if marine_day:
        holidays.add(marine_day)

    # Mountain Day
    mountain_day = _get_mountain_day(year)
    if mountain_day:
        holidays.add(mountain_day)

    # Greenery Day
    greenery_day = _get_greenery_day(year)
    if greenery_day:
        holidays.add(greenery_day)

    # Vernal Equinox Day
    vernal_equinox = _get_vernal_equinox_day(year)
    if vernal_equinox:
        holidays.add(vernal_equinox)

    # Sports Day
    sports_day = _get_sports_day(year)
    if sports_day:
        holidays.add(sports_day)

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
