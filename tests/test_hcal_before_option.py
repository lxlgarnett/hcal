"""
Tests for the hcal -B option.
"""
# pylint: disable=duplicate-code
import re
import subprocess
import sys
import unittest


class TestHcalBeforeOption(unittest.TestCase):
    """Test suite for 'hcal -B' functionality."""

    @staticmethod
    def strip_ansi(text):
        """Helper to strip ANSI escape codes."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def test_hcal_before_1(self):
        """
        Test that 'hcal -B 1' shows current and previous month.
        """
        # Feb 2025 -> Jan 2025, Feb 2025
        cmd = [sys.executable, "./hcal", "-B", "1", "2", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("January 2025", output)
        self.assertIn("February 2025", output)
        self.assertNotIn("March 2025", output)

    def test_hcal_before_2(self):
        """
        Test that 'hcal -B 2' shows current and previous two months.
        """
        # Mar 2025 -> Jan, Feb, Mar 2025
        cmd = [sys.executable, "./hcal", "-B", "2", "3", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("January 2025", output)
        self.assertIn("February 2025", output)
        self.assertIn("March 2025", output)

        # Check alignment (side-by-side for 3 months)
        lines = output.split('\n')
        title_line = next((line for line in lines if "January 2025" in line), None)
        self.assertIsNotNone(title_line)
        self.assertIn("February 2025", title_line)
        self.assertIn("March 2025", title_line)

    def test_hcal_before_3(self):
        """
        Test that 'hcal -B 3' shows 4 months in two rows.
        """
        # Apr 2025 -> Jan, Feb, Mar, Apr 2025
        cmd = [sys.executable, "./hcal", "-B", "3", "4", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("January 2025", output)
        self.assertIn("February 2025", output)
        self.assertIn("March 2025", output)
        self.assertIn("April 2025", output)

        # Jan, Feb, Mar should be in one row
        # Apr should be in another row
        lines = output.split('\n')
        first_row_titles = next((line for line in lines if "January 2025" in line), "")
        second_row_titles = next((line for line in lines if "April 2025" in line), "")

        self.assertIn("February 2025", first_row_titles)
        self.assertIn("March 2025", first_row_titles)
        self.assertNotIn("April 2025", first_row_titles)
        self.assertIn("April 2025", second_row_titles)

    def test_hcal_before_and_three(self):
        """
        Test 'hcal -3 -B 2' shows 2 before and 1 after (total 4).
        Wait, -3 means 1 before and 1 after.
        If -B 2 is specified, max(1, 2) = 2 before.
        So it should show 2 before (Nov, Dec 2024), current (Jan 2025), and 1 after (Feb 2025).
        """
        # Jan 2025 -> Nov 2024, Dec 2024, Jan 2025, Feb 2025
        cmd = [sys.executable, "./hcal", "-3", "-B", "2", "1", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("November 2024", output)
        self.assertIn("December 2024", output)
        self.assertIn("January 2025", output)
        self.assertIn("February 2025", output)

    def test_hcal_before_with_year(self):
        """
        Test 'hcal -y 2025 -B 1' shows Dec 2024 + whole year 2025.
        """
        cmd = [sys.executable, "./hcal", "-y", "2025", "-B", "1"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("December 2024", output)
        self.assertIn("January 2025", output)
        self.assertIn("December 2025", output)

        # Check that it didn't print error
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
