"""
Tests for the hcal -3 option.
"""
# pylint: disable=duplicate-code
import re
import subprocess
import sys
import unittest


class TestHcalThreeMonths(unittest.TestCase):
    """Test suite for 'hcal -3' functionality."""

    @staticmethod
    def strip_ansi(text):
        """Helper to strip ANSI escape codes."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def test_hcal_three_months(self):
        """
        Test that 'hcal -3' shows previous, current, and next month.
        """
        # Pick a specific month to test: Jan 2025
        # Prev: Dec 2024
        # Next: Feb 2025
        cmd = [sys.executable, "./hcal", "-3", "1", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        # Check headers
        self.assertIn("December 2024", output)
        self.assertIn("January 2025", output)
        self.assertIn("February 2025", output)

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
        Test that 'hcal -3' output lines are properly padded to 64 chars visually.
        20 + 2 + 20 + 2 + 20 = 64.
        """
        cmd = [sys.executable, "./hcal", "-3", "1", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')

        for line in lines:
            if not line:
                continue
            vis_len = len(self.strip_ansi(line))
            self.assertEqual(vis_len, 64, f"Line length {vis_len} != 64: '{line}'")

    def test_hcal_three_months_default(self):
        """
        Test 'hcal -3' without args (defaults to current month).
        """
        # Just check command runs successfully
        cmd = [sys.executable, "./hcal", "-3"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        self.assertEqual(result.returncode, 0)

    def test_hcal_three_months_error_on_year(self):
        """
        Test 'hcal -3 2025' prints error.
        """
        cmd = [sys.executable, "./hcal", "-3", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertIn("not valid with year", result.stderr)


if __name__ == "__main__":
    unittest.main()
