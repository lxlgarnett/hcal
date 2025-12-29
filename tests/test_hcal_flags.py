"""
Tests for hcal command-line flags.
"""
import datetime
import unittest
from tests.hcal_test_base import HcalTestCase

class TestHcalFlags(HcalTestCase):
    """
    Test cases for hcal flags.
    """
    def test_hcal_help_flag(self):
        """
        Test that --help displays the help message.
        """
        result = self.run_hcal("--help", check=False)

        # Check output for usage info
        self.assertIn("usage: hcal", result.stdout)
        self.assertIn("Show calendar on terminal", result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_hcal_no_highlight_flag(self):
        """
        Test that -h disables today's highlighting.
        """
        now = datetime.datetime.now()
        month = now.month
        year = now.year

        # Run hcal with -h for current month/year
        result = self.run_hcal("-h", str(month), str(year))
        output = result.stdout

        # The highlight code is \033[47;30m
        ansi_highlight = "\033[47;30m"

        self.assertNotIn(ansi_highlight, output,
                         "Highlight code found but should be disabled by -h")

        self.assertIn(str(year), output)
        # Check for weekend color (Red or Blue) to ensure colors are generally working
        # Red: \033[31m, Blue: \033[34m
        self.assertTrue("\033[31m" in output or "\033[34m" in output,
                        "Weekend colors should still be present")

if __name__ == "__main__":
    unittest.main()
