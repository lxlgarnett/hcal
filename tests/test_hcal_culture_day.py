import unittest
from hcal_holidays import get_holidays

class TestJapanCultureDay(unittest.TestCase):
    """
    Unit tests for Culture Day logic in Japan.
    """

    def test_culture_day_before_1955(self):
        """
        Test that Culture Day is not observed before 1955.
        """
        holidays_1954 = get_holidays('Japan', 1954)
        self.assertNotIn((11, 3), holidays_1954, "Culture Day should not be observed in 1954")

    def test_culture_day_from_1955(self):
        """
        Test that Culture Day is observed starting from 1955.
        """
        holidays_1955 = get_holidays('Japan', 1955)
        self.assertIn((11, 3), holidays_1955, "Culture Day should be observed in 1955")

    def test_culture_day_current_year(self):
        """
        Test that Culture Day is observed in recent years.
        """
        holidays_2024 = get_holidays('Japan', 2024)
        self.assertIn((11, 3), holidays_2024, "Culture Day should be observed in 2024")

if __name__ == '__main__':
    unittest.main()
