import unittest
from hcal_holidays import get_holidays
import datetime

class TestJapanHolidays(unittest.TestCase):
    def test_substitute_holiday_simple(self):
        # Feb 11, 2024 is National Foundation Day and it is a Sunday.
        # So Feb 12, 2024 should be a holiday.
        holidays_2024 = get_holidays('Japan', 2024)
        self.assertIn((2, 11), holidays_2024)
        self.assertIn((2, 12), holidays_2024, "Feb 12, 2024 should be a substitute holiday")

    def test_substitute_holiday_consecutive(self):
        # May 3, 2020 (Constitution Memorial Day) was a Sunday.
        # May 4 (Greenery Day) is a holiday.
        # May 5 (Children's Day) is a holiday.
        # So May 6 should be the substitute holiday.
        holidays_2020 = get_holidays('Japan', 2020)
        self.assertIn((5, 3), holidays_2020)
        self.assertIn((5, 4), holidays_2020)
        self.assertIn((5, 5), holidays_2020)
        self.assertIn((5, 6), holidays_2020, "May 6, 2020 should be a substitute holiday")

    def test_no_substitute_on_saturday(self):
        # Feb 11, 2023 was a Saturday.
        # No substitute holiday.
        holidays_2023 = get_holidays('Japan', 2023)
        self.assertIn((2, 11), holidays_2023)
        self.assertNotIn((2, 12), holidays_2023)
        self.assertNotIn((2, 13), holidays_2023)

if __name__ == '__main__':
    unittest.main()
