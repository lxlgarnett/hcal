"""
Utility functions and classes for hcal.
"""
import calendar
import os
from hcal_holidays import get_holidays


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
        with open(expanded_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except (OSError, IOError) as e:
        print(f"Error reading config file {expanded_path}: {e}")

    return config


class HighlightCalendar(calendar.TextCalendar):
    """
    A custom TextCalendar that highlights the current day, weekends, and holidays.
    """

    def __init__(self, firstweekday=0, today=None, country=None,
                 highlight_today=True):
        """
        Initializes the HighlightCalendar.

        Args:
            firstweekday (int): The first day of the week (0=Monday, 6=Sunday).
            today (datetime.date): The current date.
            country (str): The country code for holiday calculations (e.g., 'Japan').
            highlight_today (bool): Whether to highlight today's date.
        """
        super().__init__(firstweekday)
        self.today = today
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
        if day == 0:
            return s

        # Check if this is today
        if (self.highlight_today and self.today and
                self.curr_y == self.today.year and
                self.curr_m == self.today.month and
                day == self.today.day):
            # White background (47), Black text (30) for contrast
            return f"\033[47;30m{s}\033[0m"

        # Check for Holidays
        if self.country:
            # Refresh holidays if year changes (though formatmonth sets curr_y)
            # Optimization: We could cache this, but it's cheap to fetch for now.
            self.holidays = get_holidays(self.country, self.curr_y)

            if (self.curr_m, day) in self.holidays:
                return f"\033[31m{s}\033[0m"  # Red

        # Weekend coloring
        if weekday == calendar.SUNDAY:
            return f"\033[31m{s}\033[0m"  # Red
        if weekday == calendar.SATURDAY:
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
