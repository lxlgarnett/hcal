"""
Tests for holiday color customization via .hcalrc.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

class TestHcalHolidayColor(unittest.TestCase):
    """
    Test suite for checking holiday color rendering based on configuration.
    """
    def setUp(self):
        """Set up a temporary HOME directory and define hcal path."""
        # Create a temporary directory for HOME
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME')
        os.environ['HOME'] = self.test_dir

        # Path to hcal script
        self.hcal_path = os.path.abspath("./hcal")

    def tearDown(self):
        """Clean up the temporary directory and restore HOME."""
        # Cleanup
        shutil.rmtree(self.test_dir)
        if self.original_home:
            os.environ['HOME'] = self.original_home

    def test_holiday_color_green(self):
        """Test that holiday color is green when configured in .hcalrc."""
        # Create .hcalrc with green holiday color
        with open(os.path.join(self.test_dir, ".hcalrc"), "w", encoding="utf-8") as f:
            f.write("country=Japan\n")
            f.write("holiday_color=green\n")

        # Run hcal for Jan 2024 (Jan 1 is holiday in JP, and it is a Monday)
        cmd = [sys.executable, self.hcal_path, "1", "2024"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Jan 1 is New Year's Day, should be green (\033[32m)
        # Expected: \033[32m 1\033[0m
        self.assertIn("\033[32m 1\033[0m", result.stdout)

    def test_holiday_color_blue(self):
        """Test that holiday color is blue when configured in .hcalrc."""
        # Create .hcalrc with blue holiday color
        with open(os.path.join(self.test_dir, ".hcalrc"), "w", encoding="utf-8") as f:
            f.write("country=Japan\n")
            f.write("holiday_color=blue\n")

        # Run hcal for Jan 2024
        cmd = [sys.executable, self.hcal_path, "1", "2024"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Jan 1 should be blue (\033[34m)
        self.assertIn("\033[34m 1\033[0m", result.stdout)

    def test_holiday_color_default_red(self):
        """Test that holiday color defaults to red when not configured."""
        # Create .hcalrc without holiday_color (defaults to red)
        with open(os.path.join(self.test_dir, ".hcalrc"), "w", encoding="utf-8") as f:
            f.write("country=Japan\n")

        cmd = [sys.executable, self.hcal_path, "1", "2024"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Jan 1 should be red (\033[31m)
        # Note: Jan 1 2024 is Monday, so it wouldn't be red unless it's a holiday.
        self.assertIn("\033[31m 1\033[0m", result.stdout)

        # Ensure it's not green (previous default)
        self.assertNotIn("\033[32m 1\033[0m", result.stdout)

if __name__ == '__main__':
    unittest.main()
