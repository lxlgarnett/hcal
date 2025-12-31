"""
Tests for the hcal -3 option.
"""
import unittest
from tests.test_constants import CALENDAR_WIDTH
from tests.hcal_test_base import HcalTestCase


class TestHcalThreeMonths(HcalTestCase):
    """Test suite for 'hcal -3' functionality."""

    def test_hcal_three_months(self):
        """
        Test that 'hcal -3' shows previous, current, and next month.
        """
        # Pick a specific month to test: Jan 2025
        # Prev: Dec 2024
        # Next: Feb 2025
        result = self.run_hcal("-3", "1", "2025")
        output = result.stdout

        # Check headers
        self.assert_months_in_output(output, ["December 2024", "January 2025", "February 2025"])

        # Check alignment (crude check)
        lines = output.split('\n')
        # Find the line with January 2025
        title_line = next((line for line in lines if "January 2025" in line), None)

        self.assertIsNotNone(title_line, "Title line not found.")

        # December 2024 should be left, January 2025 center, February 2025 right
        idx_dec = title_line.find("December 2024")
        idx_jan = title_line.find("January 2025")
        idx_feb = title_line.find("February 2025")

        self.assertNotEqual(idx_dec, -1)
        self.assertNotEqual(idx_jan, -1)
        self.assertNotEqual(idx_feb, -1)
        self.assertTrue(idx_dec < idx_jan < idx_feb, "Months ordering incorrect.")

    def test_hcal_three_months_alignment(self):
        """
        Test that 'hcal -3' output lines are properly padded to CALENDAR_WIDTH chars visually.
        20 + 2 + 20 + 2 + 20 = 64.
        """
        result = self.run_hcal("-3", "1", "2025")
        lines = result.stdout.split('\n')

        for line in lines:
            if not line:
                continue
            self.assert_visual_length(line, CALENDAR_WIDTH)

    def test_hcal_three_months_default(self):
        """
        Test 'hcal -3' without args (defaults to current month).
        """
        # Just check command runs successfully
        result = self.run_hcal("-3")
        self.assertEqual(result.returncode, 0)

    def test_hcal_three_months_error_on_year(self):
        """
        Test 'hcal -3 2025' prints error.
        """
        result = self.run_hcal("-3", "2025", check=False)
        self.assertIn("not valid with year", result.stderr)


if __name__ == "__main__":
    unittest.main()
