"""
Tests for Mountain Day in Japan.
"""
import unittest
from hcal_holidays import get_holidays

class TestHcalMountainDay(unittest.TestCase):
    def test_mountain_day_before_2016(self):
        """Mountain Day did not exist before 2016."""
        holidays = get_holidays('Japan', 2015)
        self.assertNotIn((8, 11), holidays)

    def test_mountain_day_fixed_2016(self):
        """Mountain Day started in 2016 on Aug 11."""
        holidays = get_holidays('Japan', 2016)
        self.assertIn((8, 11), holidays)

    def test_mountain_day_2020_olympics(self):
        """Mountain Day moved to Aug 10 in 2020."""
        holidays = get_holidays('Japan', 2020)
        self.assertIn((8, 10), holidays)
        self.assertNotIn((8, 11), holidays)

    def test_mountain_day_2021_olympics(self):
        """Mountain Day moved to Aug 8 in 2021."""
        holidays = get_holidays('Japan', 2021)
        self.assertIn((8, 8), holidays)
        self.assertNotIn((8, 11), holidays)
        
        # August 8, 2021 was a Sunday.
        # Aug 9 (Monday) should be a substitute holiday.
        self.assertIn((8, 9), holidays)

    def test_mountain_day_recent_years(self):
        """Test recent years."""
        holidays = get_holidays('Japan', 2024)
        self.assertIn((8, 11), holidays)

        # 2024: Aug 11 is Sunday.
        # Aug 12 (Monday) should be a substitute holiday.
        self.assertIn((8, 12), holidays)

if __name__ == '__main__':
    unittest.main()
