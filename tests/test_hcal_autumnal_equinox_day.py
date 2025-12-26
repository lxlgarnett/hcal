"""
Tests for Autumnal Equinox Day calculation.
"""
import unittest
from hcal_holidays import get_holidays

class TestHcalAutumnalEquinoxDay(unittest.TestCase):
    """Test suite for Autumnal Equinox Day logic."""

    def test_autumnal_equinox_1955_1979(self):
        """Test dates between 1955 and 1979."""
        # 1960: September 23
        holidays_1960 = get_holidays('Japan', 1960)
        self.assertIn((9, 23), holidays_1960)

        # 1975: September 24
        holidays_1975 = get_holidays('Japan', 1975)
        self.assertIn((9, 24), holidays_1975)

    def test_autumnal_equinox_1980_2099(self):
        """Test dates between 1980 and 2099."""
        # 2023: September 23
        holidays_2023 = get_holidays('Japan', 2023)
        self.assertIn((9, 23), holidays_2023)

        # 2024: September 22
        holidays_2024 = get_holidays('Japan', 2024)
        self.assertIn((9, 22), holidays_2024)

        # 2025: September 23
        holidays_2025 = get_holidays('Japan', 2025)
        self.assertIn((9, 23), holidays_2025)

    def test_autumnal_equinox_pre_1955(self):
        """Test dates before 1955 (should be None/not present)."""
        # Should not be present before 1955
        holidays_1947 = get_holidays('Japan', 1947)
        # Check September 22, 23, 24 just in case
        self.assertNotIn((9, 22), holidays_1947)
        self.assertNotIn((9, 23), holidays_1947)
        self.assertNotIn((9, 24), holidays_1947)

        # 1950 should also not have it
        holidays_1950 = get_holidays('Japan', 1950)
        self.assertNotIn((9, 23), holidays_1950)

if __name__ == '__main__':
    unittest.main()
