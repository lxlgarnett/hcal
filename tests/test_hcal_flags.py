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

    def test_illegal_month_exits_with_error(self):
        """Test that an out-of-range month fails cleanly instead of tracebacking."""
        result = self.run_hcal("0", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("illegal month value", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_no_color_when_not_a_terminal(self):
        """Test that color is disabled by default when stdout is not a tty."""
        now = datetime.datetime.now()
        # force_color=False -> rely on default --color=auto in a piped subprocess
        result = self.run_hcal(str(now.month), str(now.year), force_color=False)

        self.assertNotIn("\033[", result.stdout,
                         "ANSI codes should be absent when output is not a terminal")

    def test_color_never_disables_color(self):
        """Test that --color=never suppresses all ANSI codes."""
        result = self.run_hcal("--color=never", "12", "2025", force_color=False)

        self.assertNotIn("\033[", result.stdout,
                         "ANSI codes should be absent with --color=never")

    def test_color_always_enables_color(self):
        """Test that --color=always emits ANSI codes even when piped."""
        result = self.run_hcal("--color=always", "12", "2025", force_color=False)

        self.assertIn("\033[", result.stdout,
                      "ANSI codes should be present with --color=always")


if __name__ == "__main__":
    unittest.main()
