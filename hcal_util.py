"""
Utility functions and classes for hcal.
"""
import calendar
import datetime
import os
from hcal_holidays import get_holidays

ANSI_COLORS = {
    'red': '\033[31m',
    'green': '\033[32m',
    'blue': '\033[34m',
    'yellow': '\033[33m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
}

CALENDAR_WIDTH = 64
DAYS_IN_WEEK = 7
JULIAN_COL_WIDTH = 3
DEFAULT_COL_WIDTH = 2


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
        with open(expanded_path, 'r', encoding='utf-8') as config_file:
            for line in config_file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except (OSError, IOError) as error:
        print(f"Error reading config file {expanded_path}: {error}")

    return config


class HighlightCalendar(calendar.TextCalendar):
    """
    A custom TextCalendar that highlights the current day, weekends, and holidays.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, firstweekday=0, today=None, country=None,
                 highlight_today=True, holiday_color='red', julian=False):
        """
        Initializes the HighlightCalendar.

        Args:
            firstweekday (int): The first day of the week (0=Monday, 6=Sunday).
            today (datetime.date): The current date.
            country (str): The country code for holiday calculations (e.g., 'Japan').
            highlight_today (bool): Whether to highlight today's date.
            holiday_color (str): The color name for holidays.
            julian (bool): Whether to display Julian days (day of year).
        """
        # pylint: disable=too-many-arguments, too-many-positional-arguments
        super().__init__(firstweekday)
        self.today = today
        self.country = country
        self.highlight_today = highlight_today
        self.curr_y = 0
        self.curr_m = 0
        self.holidays = set()
        self.holiday_color_code = ANSI_COLORS.get(holiday_color.lower(), ANSI_COLORS['red'])
        self.julian = julian

        # Calculate dimensions
        spaces_in_week_line = DAYS_IN_WEEK - 1

        if self.julian:
            # Day of year can be 3 digits
            col_width = JULIAN_COL_WIDTH
            # The 'w' argument for formatmonth should be 3 for Julian days
            self.formatmonth_w = JULIAN_COL_WIDTH
        else:
            # Default calendar day width is 2
            col_width = DEFAULT_COL_WIDTH
            # The 'w' argument for formatmonth should be 0 to use the default width
            # for non-Julian days.
            self.formatmonth_w = 0

        self.month_width = col_width * DAYS_IN_WEEK + spaces_in_week_line

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
        if self.julian and day > 0:
            date_obj = datetime.date(self.curr_y, self.curr_m, day)
            day_str = str(date_obj.timetuple().tm_yday).rjust(width)
        else:
            day_str = super().formatday(day, weekday, width)

        if day == 0:
            return day_str

        # Check if this is today
        if (self.highlight_today and self.today and
                self.curr_y == self.today.year and
                self.curr_m == self.today.month and
                day == self.today.day):
            # White background (47), Black text (30) for contrast
            return f"\033[47;30m{day_str}\033[0m"

        # Check for Holidays
        if self.country:
            # Refresh holidays if year changes (though formatmonth sets curr_y)
            # Optimization: We could cache this, but it's cheap to fetch for now.
            self.holidays = get_holidays(self.country, self.curr_y)

            if (self.curr_m, day) in self.holidays:
                return f"{self.holiday_color_code}{day_str}\033[0m"

        # Weekend coloring
        if weekday == calendar.SUNDAY:
            return f"\033[31m{day_str}\033[0m"  # Red
        if weekday == calendar.SATURDAY:
            return f"\033[34m{day_str}\033[0m"  # Blue

        return day_str

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
