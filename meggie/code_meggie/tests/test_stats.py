# coding: utf-8

"""
"""

import unittest

from meggie.code_meggie.general.statistic import Statistic

class TestStatistic(unittest.TestCase):
    """
    Unit tests for the Statistic-class. Tests are created for find-maximum
    and find_minimum methods.
    """
    arr_normal = [0,25,7,5,48,6,84,2,1]
    arr_many_maximums = [0,85,85,5,48,6,85,48]
    arr_chars = ['a','b']
    arr_negatives = [-40, -100, -10, -15]
    arr_empty = []
        
    s = Statistic()
        
    def test_all_normal(self):
        """
        Test with all parameters having a normal value.        
        If this test fails, something is seriously wrong.
        """
        
        self.assertEqual(self.s.find_maximum(self.arr_normal), (84, 6), 
                         'Find_maximum normal failed')
        
        self.assertEqual(self.s.find_minimum(self.arr_normal), (0,0), 
                         'Find_minimum_normal failed.')
    
    def test_arr_many_maximums(self):
        """
        Should return the first instance of the maximum and the time it
        occurred.
        """
        self.assertEqual(self.s.find_maximum(self.arr_many_maximums), (85, 1), 
                         'Find_maximum with many maximums failed.')
        
    def test_arr_chars(self):
        """
        since numpy arrays should only contain numbers, a TypeError is raised.
        """
        with self.assertRaises(TypeError):
            self.s.find_maximum(self.arr_chars)                  
    
    def test_arr_negatives(self):
        """ Should work fine with negative values """

        self.assertEqual(self.s.find_maximum(self.arr_negatives), (-10, 2), 
                         'Find_maximum negative array failed.')
        
        self.assertEqual(self.s.find_minimum(self.arr_negatives), (-100, 1), 
                         'Find_minimum with negative array failed.')
        
    def test_arr_empty(self):
        """
        Empty array is not allowed. Raises an exception.
        """
        with self.assertRaises(ValueError):
            self.s.find_maximum(self.arr_empty)
        

if __name__ == "__main__":
    unittest.main()
