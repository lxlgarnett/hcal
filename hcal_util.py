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
    def __init__(self, firstweekday=0, today_year=None, today_month=None, today_day=None, country=None):
        super().__init__(firstweekday)
        self.today_year = today_year
        self.today_month = today_month
        self.today_day = today_day
        self.country = country
        self.curr_y = 0
        self.curr_m = 0
        self.holidays = set()

    def formatday(self, day, weekday, width):
        s = super().formatday(day, weekday, width)
        if day == 0: return s

        # Check if this is today
        if (self.curr_y == self.today_year and
                self.curr_m == self.today_month and
                day == self.today_day):
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
        elif weekday == calendar.SATURDAY:
            return f"\033[34m{s}\033[0m"  # Blue

        return s

    def formatmonth(self, theyear, themonth, w=0, l=0):
        self.curr_y = theyear
        self.curr_m = themonth
        return super().formatmonth(theyear, themonth, w, l)
