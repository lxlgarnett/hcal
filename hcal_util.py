import calendar

class HighlightCalendar(calendar.TextCalendar):
    def __init__(self, firstweekday=0, today_year=None, today_month=None, today_day=None):
        super().__init__(firstweekday)
        self.today_year = today_year
        self.today_month = today_month
        self.today_day = today_day
        self.curr_y = 0
        self.curr_m = 0

    def formatday(self, day, weekday, width):
        s = super().formatday(day, weekday, width)
        if day == 0: return s 
        
        # Check if this is today
        if (self.curr_y == self.today_year and 
            self.curr_m == self.today_month and 
            day == self.today_day):
            # White background (47), Black text (30) for contrast
            return f"\033[47;30m{s}\033[0m"
        
        # Weekend coloring
        if weekday == calendar.SUNDAY:
            return f"\033[31m{s}\033[0m" # Red
        elif weekday == calendar.SATURDAY:
            return f"\033[34m{s}\033[0m" # Blue

        return s


    def formatmonth(self, theyear, themonth, w=0, l=0):
        self.curr_y = theyear
        self.curr_m = themonth
        return super().formatmonth(theyear, themonth, w, l)
