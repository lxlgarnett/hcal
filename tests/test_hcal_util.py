import unittest
from hcal_util import get_specific_monday

class TestHcalUtil(unittest.TestCase):
    def test_get_specific_monday(self):
        # 2023 January: 1st is Sunday.
        # 1st Monday: 2nd
        # 2nd Monday: 9th
        self.assertEqual(get_specific_monday(2023, 1, 1), 2)
        self.assertEqual(get_specific_monday(2023, 1, 2), 9)

        # 2023 October: 1st is Sunday.
        # 1st Monday: 2nd
        # 2nd Monday: 9th
        self.assertEqual(get_specific_monday(2023, 10, 2), 9)
        
        # 2024 January: 1st is Monday.
        # 1st Monday: 1st
        # 2nd Monday: 8th
        self.assertEqual(get_specific_monday(2024, 1, 1), 1)
        self.assertEqual(get_specific_monday(2024, 1, 2), 8)

if __name__ == '__main__':
    unittest.main()
