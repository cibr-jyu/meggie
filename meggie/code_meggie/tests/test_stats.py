# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 14, 2013

@author: Jaakko Leppakangas, Atte Rautio
Contains unit tests for the Statistic class.
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
