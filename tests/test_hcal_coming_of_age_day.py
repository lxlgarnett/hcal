import unittest
from hcal_holidays import get_holidays

class TestComingOfAgeDay(unittest.TestCase):
    def test_coming_of_age_day_before_2000(self):
        # Before 2000, it should be January 15th
        holidays_1999 = get_holidays('Japan', 1999)
        self.assertIn((1, 15), holidays_1999)
        # It should NOT be the 2nd Monday (Jan 11th in 1999) unless Jan 11 is Jan 15 (which implies logic error check)
        # Jan 1st 1999 is Friday. 
        # Jan 4 is Mon (1st). Jan 11 is Mon (2nd).
        # So if the bug exists, (1, 11) might be in holidays instead of (1, 15).
        self.assertNotIn((1, 11), holidays_1999, "Coming of Age Day should not be 2nd Monday in 1999")

    def test_coming_of_age_day_from_2000(self):
        # From 2000, it should be 2nd Monday of January
        # 2000 Jan 1 is Saturday.
        # Jan 3 is Mon (1st). Jan 10 is Mon (2nd).
        holidays_2000 = get_holidays('Japan', 2000)
        self.assertIn((1, 10), holidays_2000)
        self.assertNotIn((1, 15), holidays_2000, "Coming of Age Day should not be Jan 15 in 2000")
