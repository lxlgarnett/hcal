"""
Tests for the --version flag and -m (Monday-start) option.
"""
import unittest

from tests.hcal_test_base import HcalTestCase


class TestVersionAndMonday(HcalTestCase):
    """Test cases for --version and -m."""

    def test_version_flag(self):
        """--version prints the program version and exits 0."""
        result = self.run_hcal("--version", check=False)

        self.assertEqual(result.returncode, 0)
        self.assertRegex(result.stdout, r"^hcal \d+\.\d+\.\d+")

    def test_default_week_starts_on_sunday(self):
        """Without -m, the weekday header starts with Sunday."""
        result = self.run_hcal("12", "2025")
        header = self.strip_ansi(result.stdout).split("\n")[1]

        self.assertTrue(header.strip().startswith("Su"), header)

    def test_monday_flag_starts_week_on_monday(self):
        """-m makes the weekday header start with Monday."""
        result = self.run_hcal("-m", "12", "2025")
        header = self.strip_ansi(result.stdout).split("\n")[1]

        self.assertTrue(header.strip().startswith("Mo"), header)

    def test_monday_flag_keeps_weekend_colors(self):
        """Weekend coloring follows the actual weekday regardless of -m.

        Dec 6 2025 is a Saturday (blue, \\033[34m) and Dec 7 is a Sunday
        (red, \\033[31m); both must stay colored when weeks start on Monday.
        """
        result = self.run_hcal("-m", "12", "2025")

        self.assertIn("\033[34m 6\033[0m", result.stdout)
        self.assertIn("\033[31m 7\033[0m", result.stdout)


if __name__ == "__main__":
    unittest.main()
