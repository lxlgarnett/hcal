"""
Tests for the hcal -A option.
"""
import re
import subprocess
import sys
import unittest


class TestHcalAfterOption(unittest.TestCase):
    """Test suite for 'hcal -A' functionality."""

    @staticmethod
    def strip_ansi(text):
        """Helper to strip ANSI escape codes."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def test_hcal_after_1(self):
        """
        Test that 'hcal -A 1' shows current and next month.
        """
        # Jan 2025 -> Jan 2025, Feb 2025
        cmd = [sys.executable, "./hcal", "-A", "1", "1", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("January 2025", output)
        self.assertIn("February 2025", output)
        self.assertNotIn("December 2024", output)

    def test_hcal_after_2(self):
        """
        Test that 'hcal -A 2' shows current and next two months.
        """
        # Jan 2025 -> Jan, Feb, Mar 2025
        cmd = [sys.executable, "./hcal", "-A", "2", "1", "2025"]
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

    def test_hcal_after_3(self):
        """
        Test that 'hcal -A 3' shows 4 months in two rows.
        """
        # Jan 2025 -> Jan, Feb, Mar, Apr 2025
        cmd = [sys.executable, "./hcal", "-A", "3", "1", "2025"]
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

    def test_hcal_after_and_three(self):
        """
        Test 'hcal -3 -A 2' shows 1 before and 2 after (total 4).
        """
        # Jan 2025 -> Dec 2024, Jan 2025, Feb 2025, Mar 2025
        cmd = [sys.executable, "./hcal", "-3", "-A", "2", "1", "2025"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("December 2024", output)
        self.assertIn("January 2025", output)
        self.assertIn("February 2025", output)
        self.assertIn("March 2025", output)

    def test_hcal_after_with_year(self):
        """
        Test 'hcal -y 2025 -A 1' shows whole year 2025 + Jan 2026.
        """
        cmd = [sys.executable, "./hcal", "-y", "2025", "-A", "1"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        self.assertIn("January 2025", output)
        self.assertIn("December 2025", output)
        self.assertIn("January 2026", output)
        
        # Check that it didn't print error
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
