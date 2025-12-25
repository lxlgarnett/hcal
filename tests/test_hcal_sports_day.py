"""
Tests for Sports Day calculations.
"""
import unittest
from hcal_holidays import get_holidays

class TestSportsDay(unittest.TestCase):
    """
    Test cases for Sports Day rules.
    """
    def test_sports_day_1966_1999(self):
        """Test Sports Day on Oct 10 (1966-1999)."""
        # 1966: Oct 10
        holidays_1966 = get_holidays('Japan', 1966)
        self.assertIn((10, 10), holidays_1966, "Sports Day should be on Oct 10 in 1966")

        # 1999: Oct 10
        holidays_1999 = get_holidays('Japan', 1999)
        self.assertIn((10, 10), holidays_1999, "Sports Day should be on Oct 10 in 1999")

    def test_sports_day_2000_happy_monday(self):
        """Test Sports Day as Happy Monday (2nd Mon of Oct) from 2000."""
        # 2000: Oct 1 is Sunday. 2nd Monday is Oct 9.
        # Oct 1 (Sun), Oct 2 (Mon) -> 1st Monday. Oct 9 -> 2nd Monday.
        holidays_2000 = get_holidays('Japan', 2000)
        self.assertIn((10, 9), holidays_2000, "Sports Day should be on Oct 9 (2nd Mon) in 2000")

        # 2019: Oct 1 is Tuesday.
        # 1(Tu), 2(We), 3(Th), 4(Fr), 5(Sa), 6(Su), 7(Mon) -> 1st Monday.
        # 14 -> 2nd Monday.
        holidays_2019 = get_holidays('Japan', 2019)
        self.assertIn((10, 14), holidays_2019, "Sports Day should be on Oct 14 in 2019")

    def test_sports_day_olympics_exceptions(self):
        """Test Sports Day exceptions for 2020 and 2021 Olympics."""
        # 2020: July 24
        holidays_2020 = get_holidays('Japan', 2020)
        self.assertIn((7, 24), holidays_2020, "Sports Day should be on July 24 in 2020")
        # Ensure it is NOT on Oct 12 (2nd Mon of Oct 2020)
        # Oct 1 (Th). Oct 5 (Mon), Oct 12 (Mon)
        self.assertNotIn((10, 12), holidays_2020, "Sports Day should NOT be on Oct 12 in 2020")

        # 2021: July 23
        holidays_2021 = get_holidays('Japan', 2021)
        self.assertIn((7, 23), holidays_2021, "Sports Day should be on July 23 in 2021")
        # Ensure it is NOT on Oct 11 (2nd Mon of Oct 2021)
        # Oct 1 (Fr). Oct 4 (Mon), Oct 11 (Mon)
        self.assertNotIn((10, 11), holidays_2021, "Sports Day should NOT be on Oct 11 in 2021")

    def test_sports_day_2022_return_to_happy_monday(self):
        """Test Sports Day return to Happy Monday in 2022."""
        # 2022: Oct 1 is Sat.
        # 1(Sa), 2(Su), 3(Mon) -> 1st Mon.
        # 10 -> 2nd Mon.
        holidays_2022 = get_holidays('Japan', 2022)
        self.assertIn((10, 10), holidays_2022, "Sports Day should be on Oct 10 in 2022")

if __name__ == '__main__':
    unittest.main()
