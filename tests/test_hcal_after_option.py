"""
Tests for the hcal -A option.
"""
import unittest
from hcal_util import CALENDAR_WIDTH
from tests.hcal_test_base import HcalTestCase


class TestHcalAfterOption(HcalTestCase):
    """Test suite for 'hcal -A' functionality."""

    def test_hcal_after_1(self):
        """
        Test that 'hcal -A 1' shows current and next month.
        """
        # Jan 2025 -> Jan 2025, Feb 2025
        result = self.run_hcal("-A", "1", "1", "2025")
        output = result.stdout

        self.assert_months_in_output(output, ["January 2025", "February 2025"])
        self.assertNotIn("December 2024", output)

    def test_hcal_after_2(self):
        """
        Test that 'hcal -A 2' shows current and next two months.
        """
        # Jan 2025 -> Jan, Feb, Mar 2025
        result = self.run_hcal("-A", "2", "1", "2025")
        output = result.stdout

        self.assert_months_in_output(output, ["January 2025", "February 2025", "March 2025"])

        # Check alignment (side-by-side for 3 months)
        self.assert_months_row_alignment(output, "January 2025", ["February 2025", "March 2025"])

    def test_hcal_after_3(self):
        """
        Test that 'hcal -A 3' shows 4 months in two rows.
        """
        # Jan 2025 -> Jan, Feb, Mar, Apr 2025
        result = self.run_hcal("-A", "3", "1", "2025")
        self.verify_four_months_output(result.stdout,
                                       ["January 2025", "February 2025",
                                        "March 2025", "April 2025"])

    def test_hcal_after_and_three(self):
        """
        Test 'hcal -3 -A 2' shows 1 before and 2 after (total 4).
        """
        # Jan 2025 -> Dec 2024, Jan 2025, Feb 2025, Mar 2025
        result = self.run_hcal("-3", "-A", "2", "1", "2025")
        output = result.stdout

        self.assert_months_in_output(output, ["December 2024", "January 2025",
                                              "February 2025", "March 2025"])

    def test_hcal_after_with_year(self):
        """
        Test 'hcal -y 2025 -A 1' shows whole year 2025 + 1 month of 2026.
        """
        result = self.run_hcal("-y", "2025", "-A", "1")
        output = result.stdout

        # Should NOT have year headers
        self.assertNotIn("2025".center(CALENDAR_WIDTH), output)
        self.assertNotIn("2026".center(CALENDAR_WIDTH), output)
        self.assertIn("January 2025", output)
        self.assertIn("December 2025", output)
        self.assertIn("January 2026", output)
        self.assertNotIn("February 2026", output)

        # Check that it didn't print error
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
