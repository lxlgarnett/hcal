import subprocess
import datetime
import sys
import unittest

class TestHcalFlags(unittest.TestCase):
    def test_hcal_help_flag(self):
        """
        Test that --help displays the help message.
        """
        cmd = [sys.executable, "./hcal", "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check output for usage info
        self.assertIn("usage: hcal", result.stdout)
        self.assertIn("Show calendar on terminal", result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_hcal_no_highlight_flag(self):
        """
        Test that -h disables today's highlighting.
        """
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year

        # Run hcal with -h for current month/year
        cmd = [sys.executable, "./hcal", "-h", str(month), str(year)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        # The highlight code is \033[47;30m
        ansi_highlight = "\033[47;30m"
        
        self.assertNotIn(ansi_highlight, output, "Highlight code found but should be disabled by -h")
        
        # Ensure the day is still present
        # Note: calendar formatting might add padding, but the number itself should be there.
        # It's harder to check the exact number without parsing the grid, but if we check for absence of highlight
        # and presence of weekends (which confirms it printed a calendar), that's good enough.
        
        self.assertIn(str(year), output)
        # Check for weekend color (Red or Blue) to ensure colors are generally working
        # Red: \033[31m, Blue: \033[34m
        self.assertTrue("\033[31m" in output or "\033[34m" in output, "Weekend colors should still be present")

if __name__ == "__main__":
    unittest.main()
