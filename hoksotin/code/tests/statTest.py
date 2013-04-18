# coding: latin1
"""
Created on Mar 14, 2013

@author: Jaakko Leppäkangas, Atte Rautio
"""
import unittest

from statistic import Statistic

class TestStatistic(unittest.TestCase):
    """
    Unit tests for the Statistic-class.
    """
    sfreq_int = 1
    sfreq_double = 1.5
    sfreq_zero = 0
        
    arr_normal = [0,25,7,5,48,6,84,2,1]
    arr_many_maximums = [0,85,85,5,48,6,85,48]
    arr_chars = ['a','b']
    arr_negatives = [-40, -100, 0, -15]
    arr_const = [2,2,2,2]
    arr_empty = []
        
    tmin_int = 1000
    tmin_double = 1000.5
    tmin_negative = -6000
    tmin_large = 8000
        
    tmax_int = 5000
    tmax_double = 5000.5
    tmax_negative = -1000
    tmax_small = 1000
    
    ex_negative_tmin_tmax = 'Negative values for tmin and tmax not allowed.'
    ex_sfreq_zero = 'Sampling frequency cannot be zero or negative.'
    ex_arr_empty = 'No data found.'
    ex_tmin_greater_than_tmax = 'tmax must be greater than tmin.'
        
    def test_all_normal(self):
        s = Statistic()
        
        self.assertEqual(s.find_maximum(self.sfreq_int, self.arr_normal,
                                        1000, 5000), (48, 4000), 
                                        'Find_maximum normal failed')
        pass
    
    def test_max_freq_double(self):
        s = Statistic()
        
        self.assertEqual(s.find_maximum(self.sfreq_double, self.arr_normal,
                                        1000,5000), (48, 4000),
                                        'Find_maximum frequency double failed')
        pass
    
    def test_max_freq_zero(self):
        s = Statistic()
        
        with self.assertRaises(Exception) as e:
            s.find_maximum(self.sfreq_zero, self.arr_normal, 1000, 5000)
            
        self.assertEqual(e.exception.message, self.ex_sfreq_zero,
                         'Unexpected exception raised.')
            
        pass
    
    def test_max_tmin_double(self):
        s = Statistic()
        
        self.assertEqual(s.find_maximum(self.sfreq_int, self.arr_normal,
                                        self.tmin_double,self.tmax_int),
                                        (48, 4000),
                                         'Find_maximum tmin double failed')
        pass
    
    def test_max_tmin_negative(self):
        s = Statistic()
        
        with self.assertRaises(Exception) as e:
            s.find_maximum(self.sfreq_int, self.arr_normal, 
                           self.tmin_negative, self.tmax_int)
            
        self.assertEqual(e.exception.message, self.ex_negative_tmin_tmax,
                         'Unexpected exception raised.')    
        pass
    
    def test_max_tmax_negative(self):
        s = Statistic()
        
        with self.assertRaises(Exception) as e:
            s.find_maximum(self.sfreq_int, self.arr_normal,
                           self.tmin_int, self.tmax_negative)
            
        self.assertEqual(e.exception.message, self.ex_negative_tmin_tmax,
                         'Unexpected exception raised.')
        pass
    
    def test_max_tmax_smaller_than_tmin(self):
        s = Statistic()
        
        with self.assertRaises(Exception) as e:
            s.find_maximum(self.sfreq_int, self.arr_normal,
                           self.tmin_large, self.tmax_small)
            
        self.assertEqual(e.exception.message, self.ex_tmin_greater_than_tmax,
                         'Unexpected exception raised.')
        pass
        """

    def test_min(self):
        a = [0,25,4,1,5,67,2,4,6,467,7]
        m = np.array([[4,5,6],[1,2,3],[7,8,9]])
        s = Statistic()
        self.assertEqual(s.find_minimum(1, a, 1000, 5000), (1,3000), 'Find_minimum failed')
        self.assertEqual(s.find_minimum2d(1000, m), [(4,0),(1,0),(7,0)], 'Find_minimum2d failed')
        """
    if __name__ == "__main__":
        #import sys;sys.argv = ['', 'TestStatistic.testMax']
        unittest.main()
    