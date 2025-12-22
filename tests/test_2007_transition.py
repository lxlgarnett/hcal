import unittest
from hcal_holidays import get_holidays

class Test2007Transition(unittest.TestCase):
    def test_2007_holidays(self):
        holidays_2007 = get_holidays('Japan', 2007)
        
        # April 29 should be Showa Day
        self.assertIn((4, 29), holidays_2007, "Apr 29 should be a holiday (Showa Day) in 2007")
        
        # May 4 should be Greenery Day
        self.assertIn((5, 4), holidays_2007, "May 4 should be a holiday (Greenery Day) in 2007")

    def test_2006_holidays(self):
        holidays_2006 = get_holidays('Japan', 2006)
        # April 29 was Greenery Day
        self.assertIn((4, 29), holidays_2006, "Apr 29 should be a holiday (Greenery Day) in 2006")
        # May 4 was Citizens' Holiday
        self.assertIn((5, 4), holidays_2006, "May 4 should be a holiday (Citizens' Holiday) in 2006")

    def test_1986_holidays(self):
        holidays_1986 = get_holidays('Japan', 1986)
        # May 4 should be a holiday (first year of sandwich rule)
        # May 3 (Sat), May 4 (Sun? no), May 5 (Mon)
        # Wait, May 4, 1986:
        # 1986-05-01 is Thursday
        # 1986-05-03 is Saturday
        # 1986-05-04 is Sunday
        # 1986-05-05 is Monday
        # If May 4 is Sunday, it's not a Citizens' Holiday (it's Sunday).
        # Let's check 1987.
        # 1987-05-04 is Monday. Between May 3 (Sun) and May 5 (Tue).
        # In 1987, May 3 is Sunday, so May 4 is already a substitute holiday?
        # Let's check 1988.
        # 1988-05-04 is Wednesday. Between May 3 (Tue) and May 5 (Thu).
        # 1988-05-04 should be a Citizens' Holiday.
        holidays_1988 = get_holidays('Japan', 1988)
        self.assertIn((5, 4), holidays_1988, "May 4 should be a holiday (Citizens' Holiday) in 1988")


if __name__ == '__main__':
    unittest.main()
