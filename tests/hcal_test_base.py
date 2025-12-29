"""
Common utilities for hcal tests.
"""
import re
import subprocess
import sys
import unittest

class HcalTestCase(unittest.TestCase):
    """Base class for hcal tests with common helpers."""

    @staticmethod
    def strip_ansi(text):
        """Helper to strip ANSI escape codes."""
        ansi_escape = re.compile(r'(?:\x1B[@-Z\\-_]|\x1B\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def run_hcal(self, *args, check=True):
        """Runs hcal with the given arguments and returns the result."""
        cmd = [sys.executable, "./hcal"] + list(args)
        return subprocess.run(cmd, capture_output=True, text=True, check=check)

    def assert_visual_length(self, line, expected_length):
        """Asserts that a line has a certain visual length (excluding ANSI codes)."""
        vis_len = len(self.strip_ansi(line))
        self.assertEqual(vis_len, expected_length,
                         f"Line length {vis_len} != {expected_length}: '{line}'")

    def assert_months_in_output(self, output, months):
        """Asserts that the specified months are present in the output."""
        for month in months:
            self.assertIn(month, output)

    def assert_months_row_alignment(self, output, first_month, other_months, row_contains=True):
        """Asserts that months are in the same row as the first month."""
        lines = output.split('\n')
        title_line = next((line for line in lines if first_month in line), "")
        for month in other_months:
            if row_contains:
                self.assertIn(month, title_line)
            else:
                self.assertNotIn(month, title_line)

    def verify_four_months_output(self, output, months_list):
        """Verifies output for 4 months (3 in first row, 1 in second)."""
        self.assert_months_in_output(output, months_list)
        # Assuming months_list[0:3] in row 1, months_list[3] in row 2
        self.assert_months_row_alignment(output, months_list[0], months_list[1:3])
        self.assert_months_row_alignment(output, months_list[0], [months_list[3]],
                                         row_contains=False)
        self.assert_months_row_alignment(output, months_list[3], [months_list[3]])
