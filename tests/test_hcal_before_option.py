"""
Tests for the hcal -B option.
"""
import unittest
from hcal_util import CALENDAR_WIDTH
from tests.hcal_test_base import HcalTestCase


class TestHcalBeforeOption(HcalTestCase):
    """Test suite for 'hcal -B' functionality."""

    def test_hcal_before_1(self):
        """
        Test that 'hcal -B 1' shows current and previous month.
        """
        # Feb 2025 -> Jan 2025, Feb 2025
        result = self.run_hcal("-B", "1", "2", "2025")
        output = result.stdout

        self.assert_months_in_output(output, ["January 2025", "February 2025"])
        self.assertNotIn("March 2025", output)

    def test_hcal_before_2(self):
        """
        Test that 'hcal -B 2' shows current and previous two months.
        """
        # Mar 2025 -> Jan, Feb, Mar 2025
        result = self.run_hcal("-B", "2", "3", "2025")
        output = result.stdout

        self.assert_months_in_output(output, ["January 2025", "February 2025", "March 2025"])

        # Check alignment (side-by-side for 3 months)
        self.assert_months_row_alignment(output, "January 2025", ["February 2025", "March 2025"])

    def test_hcal_before_3(self):
        """
        Test that 'hcal -B 3' shows 4 months in two rows.
        """
        # Apr 2025 -> Jan, Feb, Mar, Apr 2025
        result = self.run_hcal("-B", "3", "4", "2025")
        self.verify_four_months_output(result.stdout,
                                       ["January 2025", "February 2025",
                                        "March 2025", "April 2025"])

    def test_hcal_before_and_three(self):
        """
        Test 'hcal -3 -B 2' shows 2 before and 1 after (total 4).
        Wait, -3 means 1 before and 1 after.
        If -B 2 is specified, max(1, 2) = 2 before.
        So it should show 2 before (Nov, Dec 2024), current (Jan 2025), and 1 after (Feb 2025).
        """
        # Jan 2025 -> Nov 2024, Dec 2024, Jan 2025, Feb 2025
        result = self.run_hcal("-3", "-B", "2", "1", "2025")
        output = result.stdout

        self.assert_months_in_output(output, ["November 2024", "December 2024",
                                              "January 2025", "February 2025"])

    def test_hcal_before_with_year(self):
        """
        Test 'hcal -y 2025 -B 1' shows 1 month of 2024 + whole year 2025 with year headers.
        """
        result = self.run_hcal("-y", "2025", "-B", "1")
        output = result.stdout

        # Should have year headers
        self.assertIn("2024".center(CALENDAR_WIDTH), output)
        self.assertIn("2025".center(CALENDAR_WIDTH), output)
        self.assertIn("December 2024", output)
        self.assertIn("January 2025", output)
        self.assertIn("December 2025", output)
        self.assertNotIn("November 2024", output)

        # Check that it didn't print error
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
