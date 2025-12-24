import calendar
import os
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


def read_config(file_path):
    """
    Reads configuration from a file.
    Format expected: KEY=VALUE per line.
    Lines starting with # are comments.
    """
    config = {}
    expanded_path = os.path.expanduser(file_path)

    if not os.path.exists(expanded_path):
        return config

    try:
        with open(expanded_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading config file {expanded_path}: {e}")

    return config


class HighlightCalendar(calendar.TextCalendar):
    """
    A custom TextCalendar that highlights the current day, weekends, and holidays.
    """

    def __init__(self, firstweekday=0, today_year=None, today_month=None, today_day=None, country=None,
                 highlight_today=True):
        """
        Initializes the HighlightCalendar.

        Args:
            firstweekday (int): The first day of the week (0=Monday, 6=Sunday).
            today_year (int): The current year.
            today_month (int): The current month.
            today_day (int): The current day.
            country (str): The country code for holiday calculations (e.g., 'Japan').
            highlight_today (bool): Whether to highlight today's date.
        """
        super().__init__(firstweekday)
        self.today_year = today_year
        self.today_month = today_month
        self.today_day = today_day
        self.country = country
        self.highlight_today = highlight_today
        self.curr_y = 0
        self.curr_m = 0
        self.holidays = set()

    def formatday(self, day, weekday, width):
        """
        Returns a formatted string for a single day.

        Highlights the current day, weekends, and holidays with ANSI color codes.

        Args:
            day (int): The day number.
            weekday (int): The day of the week (0=Monday, 6=Sunday).
            width (int): The width of the column.

        Returns:
            str: The formatted day string.
        """
        s = super().formatday(day, weekday, width)
        if day == 0: return s

        # Check if this is today
        if (self.highlight_today and
                self.curr_y == self.today_year and
                self.curr_m == self.today_month and
                day == self.today_day):
            # White background (47), Black text (30) for contrast
            return f"\033[47;30m{s}\033[0m"

        # Check for Holidays
        if self.country:
            # Refresh holidays if year changes (though formatmonth sets curr_y)
            # Optimization: We could cache this, but it's cheap to fetch for now.
            from hcal_holidays import get_holidays
            self.holidays = get_holidays(self.country, self.curr_y)

            if (self.curr_m, day) in self.holidays:
                return f"\033[31m{s}\033[0m"  # Red

        # Weekend coloring
        if weekday == calendar.SUNDAY:
            return f"\033[31m{s}\033[0m"  # Red
        elif weekday == calendar.SATURDAY:
            return f"\033[34m{s}\033[0m"  # Blue

        return s

    def formatmonth(self, theyear, themonth, w=0, l=0):
        """
        Returns a formatted month string.

        Args:
            theyear (int): The year.
            themonth (int): The month.
            w (int): Width of date columns.
            l (int): Number of newlines between weeks.

        Returns:
            str: The formatted month string.
        """
        self.curr_y = theyear
        self.curr_m = themonth
        return super().formatmonth(theyear, themonth, w, l)
