import unittest
from hcal_holidays import get_holidays

class TestJapanNationalFoundationDay(unittest.TestCase):
    """
    Unit tests for National Foundation Day logic in Japan.
    """

    def test_national_foundation_day_before_1967(self):
        """
        Test that National Foundation Day is not observed before 1967.
        """
        holidays_1966 = get_holidays('Japan', 1966)
        self.assertNotIn((2, 11), holidays_1966, "National Foundation Day should not be observed in 1966")

    def test_national_foundation_day_from_1967(self):
        """
        Test that National Foundation Day is observed starting from 1967.
        """
        holidays_1967 = get_holidays('Japan', 1967)
        self.assertIn((2, 11), holidays_1967, "National Foundation Day should be observed in 1967")

    def test_national_foundation_day_current_year(self):
        """
        Test that National Foundation Day is observed in recent years.
        """
        holidays_2024 = get_holidays('Japan', 2024)
        self.assertIn((2, 11), holidays_2024, "National Foundation Day should be observed in 2024")

if __name__ == '__main__':
    unittest.main()
