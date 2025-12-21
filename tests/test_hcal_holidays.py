import unittest
from hcal_holidays import get_holidays


class TestJapanHolidays(unittest.TestCase):
    """
    Unit tests for Japan holiday calculations.
    """

    def test_substitute_holiday_simple(self):
        """
        Test simple substitute holiday logic (Sunday holiday -> Monday).
        """
        # Feb 11, 2024 is National Foundation Day and it is a Sunday.
        # So Feb 12, 2024 should be a holiday.
        holidays_2024 = get_holidays('Japan', 2024)
        self.assertIn((2, 11), holidays_2024)
        self.assertIn((2, 12), holidays_2024, "Feb 12, 2024 should be a substitute holiday")

    def test_substitute_holiday_consecutive(self):
        """
        Test consecutive holidays with substitution (Golden Week scenario).
        """
        # May 3, 2020 (Constitution Memorial Day) was a Sunday.
        # May 4 (Greenery Day) is a holiday.
        # May 5 (Children's Day) is a holiday.
        # So May 6 should be the substitute holiday.
        holidays_2020 = get_holidays('Japan', 2020)
        self.assertIn((5, 3), holidays_2020)
        self.assertIn((5, 4), holidays_2020)
        self.assertIn((5, 5), holidays_2020)
        self.assertIn((5, 6), holidays_2020, "May 6, 2020 should be a substitute holiday")

    def test_no_substitute_on_saturday(self):
        """
        Test that no substitute holiday is created for a Saturday holiday.
        """
        # Feb 11, 2023 was a Saturday.
        # No substitute holiday.
        holidays_2023 = get_holidays('Japan', 2023)
        self.assertIn((2, 11), holidays_2023)
        self.assertNotIn((2, 12), holidays_2023)
        self.assertNotIn((2, 13), holidays_2023)

    def test_coming_of_age_day(self):
        """
        Test "Coming of Age Day" (2nd Monday of January).
        """
        # 2024: Jan 1 is Monday. 2nd Monday is Jan 8.
        self.assertIn((1, 8), get_holidays('Japan', 2024))
        # 2025: Jan 1 is Wednesday. 2nd Monday is Jan 13.
        self.assertIn((1, 13), get_holidays('Japan', 2025))
        # 2026: Jan 1 is Thursday. 2nd Monday is Jan 12.
        self.assertIn((1, 12), get_holidays('Japan', 2026))

    def test_emperors_birthday_showa_era(self):
        """
        Test Emperor's Birthday during the Showa era (pre-1989).
        """
        holidays_1980 = get_holidays('Japan', 1980)
        self.assertIn((4, 29), holidays_1980, "April 29 should be Emperor's Birthday in 1980")

    def test_emperors_birthday_heisei_era(self):
        """
        Test Emperor's Birthday during the Heisei era (1989-2018).
        """
        holidays_1995 = get_holidays('Japan', 1995)
        self.assertIn((12, 23), holidays_1995, "December 23 should be Emperor's Birthday in 1995")
        self.assertNotIn((2, 23), holidays_1995, "February 23 should not be Emperor's Birthday in 1995")

    def test_no_emperors_birthday_in_2019(self):
        """
        Test for no Emperor's Birthday in 2019.
        """
        holidays_2019 = get_holidays('Japan', 2019)
        self.assertNotIn((12, 23), holidays_2019, "There should be no Emperor's Birthday in 2019")
        self.assertNotIn((2, 23), holidays_2019, "There should be no Emperor's Birthday in 2019")

    def test_emperors_birthday_reiwa_era(self):
        """
        Test Emperor's Birthday during the Reiwa era (post-2020).
        """
        holidays_2021 = get_holidays('Japan', 2021)
        self.assertIn((2, 23), holidays_2021, "February 23 should be Emperor's Birthday in 2021")
        self.assertNotIn((12, 23), holidays_2021, "December 23 should not be Emperor's Birthday in 2021")


if __name__ == '__main__':
    unittest.main()
