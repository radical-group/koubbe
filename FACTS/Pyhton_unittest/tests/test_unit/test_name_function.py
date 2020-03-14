import unittest
import sys
import os
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__))+'/../../src/')
from name_function import formatted_name

class NamesTestCase(unittest.TestCase):

    def test_first_last_name(self):
        result = formatted_name("pete", "seeger")
        self.assertEqual(result, "Pete Seeger")

    def test_first_last_middle_name(self):
        result = formatted_name("raymond", "reddington", "red")
        self.assertEqual(result, "Raymond Red Reddington")

if __name__ == '__main__':
    unittest.main()