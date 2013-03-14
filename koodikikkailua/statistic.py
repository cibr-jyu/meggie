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
        
    def find_minimum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns a minimum for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        
        if sfreq <= 0:
            raise Exception('Sampling frequency cannot be zero.')
        if arr == []:
            raise Exception('No data found.')
        twindow = arr[int(round((tmin/1000)/sfreq)):int(round(tmax/sfreq))+1]
        return np.min(twindow)
        
    def find_minimum2d(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns an array of minimums for a 2d array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_minimum(sfreq, row, tmin, tmax) for row in arr]
        
    def find_maximum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns a maximum for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        if sfreq <= 0:
            raise Exception('Sampling frequency cannot be zero.')
        if arr == []:
            raise Exception('No data found.')
        twindow = arr[int(round((tmin/1000)/sfreq)):int(round(tmax/sfreq))+1]
        return np.max(twindow)
    
    def find_maximum2d(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns an array of maximums for a 2d array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_maximum(sfreq, row, tmin, tmax) for row in arr]
    
    def find_half_maximum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns half maximum for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return self.find_maximum(sfreq, arr, tmin, tmax)/2
    
    
    def find_half_maximum2d(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns half maximums for a 2d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_maximum(sfreq, row, tmin, tmax)/2 for row in arr]
    
    def find_maximum_intensity(self, mat, h, w):
        """
        Takes a matrix and finds the coordinates of a window for maximum intensity.
        
        Keyword arguments:
        mat           -- A matrix
        h             -- Height of the window
        w             -- Width of the window
        """
        max = 0
        xcoord = 0
        ycoord = 0
        for y in range(len(mat) - h+1):
            for x in range((len(mat[0]) - w)+1):
                newmat = mat[y:h+y,x:w+x]
                #a = calculate_integral(newmat)
                print newmat
                #if a > max:
                    #xcoord = x
                    #ycoord = y
        #TODO: palauta koordinaatit
        return max
    
