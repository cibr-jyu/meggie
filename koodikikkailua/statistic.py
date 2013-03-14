#!/usr/bin/env python
#coding: utf8 
"""
Created on Mar 14, 2013

@author: jaeilepp
"""
import numpy as np
import sys

class Statistic(object):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor
        """
        
        
    def find_maximum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns a maximum for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 1d numpy array
        tmin          -- Start of the time window
        tmax          -- End of the time window
        """
        if sfreq <= 0:
            raise Exception('Sampling frequency cannot be zero.')
        twindow = arr[int(round(tmin/sfreq)):int(round(tmax/sfreq))+1]
        return np.max(twindow)
    
    def find_maximum2d(self, sfreq, arr, tmin=0.0, tmax=0.0):
        """
        Returns maximums for a 2d array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 2d numpy array
        tmin          -- Start of the time window
        tmax          -- End of the time window
        """
        return [self.find_maximum(sfreq, row, tmin, tmax) for row in arr]
    
    def find_half_maximum(self, sfreq, arr, tmin=0.0, tmax=0.0):
        """
        Returns half maximum for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 1d numpy array
        tmin          -- Start of the time window
        tmax          -- End of the time window
        """
        return self.find_maximum(sfreq, arr, tmin, tmax)/2
    
    
    def find_half_maximum2d(self, sfreq, arr, tmin=0.0, tmax=0.0):
        """
        Returns half maximums for a 2d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 2d numpy array
        tmin          -- Start of the time window
        tmax          -- End of the time window
        """
        return [self.find_maximum(sfreq, row, tmin, tmax)/2 for row in arr]
    
    def find_maximum_intensity(self, mat, h, w):
        """
        """
        for y in range(len(mat[0]) - h):
            for x in range(len(mat) - w+1):
                newmat = mat[x][y:h]
                print newmat
                #calculate_integral(newmat)
        
    
def main():
    #TODO: yksikkötesti tmin < 0
    m = np.empty((3,3))
    a = [0,25,7,5,48,6,84,2,1]
    s = Statistic()
    print m
    print s.find_maximum(5.5, a, 0.5, 100.4)
    print (sys.float_info.max +1000000000000000)
    print s.find_half_maximum2d(1, m, 1, 2)
    m = np.array([[1, 2, 3],[4, 5, 6],[7, 8, 9]])
    print m[0][0:2]
    s.find_maximum_intensity(m, 2, 2)

if __name__ == "__main__":
    main()