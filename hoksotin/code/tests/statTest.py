"""
Created on Mar 14, 2013

@author: jaeilepp
"""
import unittest
import numpy as np
from statistic import Statistic

class Test(unittest.TestCase):


    def test_max(self):
        """
        Tests for find_maximum
        """
        a = [0,25,7,5,48,6,84,2,1]
        s = Statistic()
        self.assertEqual(s.find_maximum(0.5, a, 1000, 5000), (84, 12000), 'Find_maximum failed')
        self.assertEqual(s.find_maximum(1000, a), (84, 6), 'Find_maximum failed')
        self.assertEqual(s.find_half_maximum(1000, a), (42, 6), 'Find_maximum failed')
        a = [0,0,0,0,0,0,0]
        self.assertEqual(s.find_maximum(0.5, a, 1000, 5000), (0,4000), 'Find_maximum failed')
        pass

    def test_min(self):
        a = [0,25,4,1,5,67,2,4,6,467,7]
        m = np.array([[4,5,6],[1,2,3],[7,8,9]])
        s = Statistic()
        self.assertEqual(s.find_minimum(1, a, 1000, 5000), (1,3000), 'Find_minimum failed')
        self.assertEqual(s.find_minimum2d(1000, m), [(4,0),(1,0),(7,0)], 'Find_minimum2d failed')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMax']
    unittest.main()