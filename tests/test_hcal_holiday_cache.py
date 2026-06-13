"""
Tests for the per-year holiday caching in HighlightCalendar.
"""
import calendar
import datetime
import unittest
from unittest import mock

import hcal_util
from hcal_util import HighlightCalendar


class TestHolidayCache(unittest.TestCase):
    """Holidays only depend on the year, so they should be computed once per year."""

    def _make_cal(self):
        return HighlightCalendar(calendar.SUNDAY, today=datetime.date(2024, 1, 1),
                                 country='Japan')

    def test_holidays_computed_once_per_year(self):
        """Rendering all 12 months of a year calls get_holidays only once."""
        cal = self._make_cal()
        with mock.patch.object(hcal_util, 'get_holidays',
                               wraps=hcal_util.get_holidays) as spy:
            for month in range(1, 13):
                cal.formatmonth(2024, month)
            self.assertEqual(spy.call_count, 1)

    def test_distinct_years_computed_separately(self):
        """Different years are each computed once and cached independently."""
        cal = self._make_cal()
        with mock.patch.object(hcal_util, 'get_holidays',
                               wraps=hcal_util.get_holidays) as spy:
            cal.formatmonth(2024, 1)
            cal.formatmonth(2025, 1)
            cal.formatmonth(2024, 2)  # cached, no new call
            self.assertEqual(spy.call_count, 2)

    def test_cached_result_matches_direct_call(self):
        """Caching must not change the holiday set that gets used."""
        cal = self._make_cal()
        cal.formatmonth(2024, 1)
        self.assertEqual(cal.holidays, hcal_util.get_holidays('Japan', 2024))


if __name__ == '__main__':
    unittest.main()
