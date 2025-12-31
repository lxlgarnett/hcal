"""
Tests for hcal -j option (Julian days).
"""
import unittest
from hcal_test_base import HcalTestCase


class TestHcalJulian(HcalTestCase):
    """Tests for the -j option."""

    def test_julian_january_2025(self):
        """Test Julian days for January 2025."""
        result = self.run_hcal("-j", "1", "2025")
        output = result.stdout

        # Check header
        self.assertIn("January 2025", output)

        # Check specific Julian days
        # Jan 1 is 1
        self.assertIn(" 1", output)
        # Jan 31 is 31
        self.assertIn(" 31", output)

        # Check visual width of lines (should be 27 for month lines)
        lines = output.split('\n')
        # Find a line with dates
        date_line = next((line for line in lines if " 1" in line), None)
        self.assertIsNotNone(date_line)
        self.assert_visual_length(date_line, 27)

    def test_julian_december_2025(self):
        """Test Julian days for December 2025."""
        result = self.run_hcal("-j", "12", "2025")
        output = result.stdout

        # Check header
        self.assertIn("December 2025", output)

        # Check specific Julian days
        # Dec 1 is 335
        self.assertIn("335", output)
        # Dec 31 is 365
        self.assertIn("365", output)

    def test_julian_three_months(self):
        """Test Julian days with -3 option."""
        # Run for Dec 2025 (shows Nov 2025, Dec 2025, Jan 2026)
        result = self.run_hcal("-j", "-3", "12", "2025")
        output = result.stdout

        self.assertIn("November 2025", output)
        self.assertIn("December 2025", output)
        self.assertIn("January 2026", output)

        # Nov 1 is 305
        self.assertIn("305", output)
        # Jan 1 is 1
        self.assertIn(" 1", output)

        # Check alignment/width
        # Row width should be 27 * 3 + 2 * 2 = 85
        lines = output.split('\n')
        # Find the line containing day 1 of Jan 2026 (which is in the 3rd block)
        # It's hard to target specific line without context, but we can check max length
        max_len = max(len(self.strip_ansi(line)) for line in lines)
        self.assertEqual(max_len, 85)

    def test_julian_leap_year_2024(self):
        """Test Julian days for leap year 2024."""
        # February 2024
        result = self.run_hcal("-j", "2", "2024")
        output = result.stdout
        self.assertIn("February 2024", output)
        # Feb 1 is 32
        self.assertIn(" 32", output)
        # Feb 29 is 60
        self.assertIn(" 60", output)

        # March 2024
        result = self.run_hcal("-j", "3", "2024")
        output = result.stdout
        self.assertIn("March 2024", output)
        # Mar 1 is 61
        self.assertIn(" 61", output)

        # December 2024
        result = self.run_hcal("-j", "12", "2024")
        output = result.stdout
        self.assertIn("December 2024", output)
        # Dec 31 is 366
        self.assertIn("366", output)

if __name__ == "__main__":
    unittest.main()
