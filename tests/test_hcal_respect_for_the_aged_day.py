"""
Tests for Respect for the Aged Day calculations.
"""
import unittest
from hcal_holidays import get_holidays

class TestRespectForTheAgedDay(unittest.TestCase):
    """
    Test cases for Respect for the Aged Day rules.
    """
    def test_respect_for_the_aged_day_before_1967(self):
        """Test Respect for the Aged Day before 1967 (Should not exist)."""
        holidays_1966 = get_holidays('Japan', 1966)
        self.assertNotIn((9, 15), holidays_1966)

    def test_respect_for_the_aged_day_fixed(self):
        """Test Respect for the Aged Day 1967-2002 (Sep 15th)."""
        holidays_1967 = get_holidays('Japan', 1967)
        self.assertIn((9, 15), holidays_1967)

        holidays_2002 = get_holidays('Japan', 2002)
        self.assertIn((9, 15), holidays_2002)

    def test_respect_for_the_aged_day_happy_monday(self):
        """Test Respect for the Aged Day from 2003 (3rd Monday of Sep)."""
        # 2003: Sep 1 is Monday. 3rd Monday is 15th.
        holidays_2003 = get_holidays('Japan', 2003)
        self.assertIn((9, 15), holidays_2003)

        # 2023: Sep 1 is Friday.
        # 1st Mon: Sep 4
        # 2nd Mon: Sep 11
        # 3rd Mon: Sep 18
        holidays_2023 = get_holidays('Japan', 2023)
        self.assertIn((9, 18), holidays_2023)
        self.assertNotIn((9, 15), holidays_2023)
