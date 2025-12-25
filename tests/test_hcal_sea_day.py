"""
Tests for Sea Day (Marine Day) in Japan.
"""
import datetime
import unittest
from hcal_holidays import get_holidays

class TestHcalSeaDay(unittest.TestCase):
    def test_sea_day_before_1996(self):
        """Sea Day did not exist before 1996."""
        holidays = get_holidays('Japan', 1995)
        # July 20th shouldn't be a holiday unless it's a Sunday (it was Thursday)
        # 3rd Monday of July (July 17) shouldn't be a holiday
        self.assertNotIn((7, 20), holidays)
        self.assertNotIn((7, 17), holidays)

    def test_sea_day_fixed_1996_to_2002(self):
        """Sea Day was fixed on July 20th from 1996 to 2002."""
        # 1996: July 20 is Saturday.
        holidays = get_holidays('Japan', 1996)
        self.assertIn((7, 20), holidays)

        # 2002: July 20 is Saturday.
        holidays = get_holidays('Japan', 2002)
        self.assertIn((7, 20), holidays)

    def test_sea_day_happy_monday_2003(self):
        """Sea Day became 3rd Monday of July from 2003 onwards."""
        # 2003: July 1 is Tuesday.
        # 1st Mon: 7, 2nd Mon: 14, 3rd Mon: 21
        holidays = get_holidays('Japan', 2003)
        self.assertIn((7, 21), holidays)
        self.assertNotIn((7, 20), holidays) # July 20 is Sunday, but not Sea Day.

    def test_sea_day_2020_olympics(self):
        """Sea Day moved to July 23 in 2020 for Olympics."""
        holidays = get_holidays('Japan', 2020)
        self.assertIn((7, 23), holidays)
        # 3rd Monday was July 20.
        self.assertNotIn((7, 20), holidays)

    def test_sea_day_2021_olympics(self):
        """Sea Day moved to July 22 in 2021 for Olympics."""
        holidays = get_holidays('Japan', 2021)
        self.assertIn((7, 22), holidays)
        # 3rd Monday was July 19.
        self.assertNotIn((7, 19), holidays)

    def test_sea_day_recent_years(self):
        """Test recent years."""
        # 2023: July 1 is Saturday.
        # 1st Mon: 3, 2nd: 10, 3rd: 17
        holidays = get_holidays('Japan', 2023)
        self.assertIn((7, 17), holidays)

        # 2024: July 1 is Monday.
        # 1st Mon: 1, 2nd: 8, 3rd: 15
        holidays = get_holidays('Japan', 2024)
        self.assertIn((7, 15), holidays)

if __name__ == '__main__':
    unittest.main()
