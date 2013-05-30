# coding: latin1

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

@author: Jaakko LeppÄkangas, Atte Rautio
Contains the Statistic-class used for statistical operations.
"""
import numpy as np
import sys

from IntegralImage import IntegralImage

class Statistic(object):
    """
    A class for statistical operations.
    """
    # TODO: How to handle doubles in sfreq?

    def __init__(self):
        pass
    
    def initialize_variables(self, sfreq, arr, tmin, tmax):
        """
        Initializes the variables used in find_minimum and find_maximum and
        raises appropriate exceptions for inappropriate inputs.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        
        Raises a general Exception, when:
        
        - tmin or tmax are negative
        - tmin is greater than tmax
        - sfreq is equal to or lower than zero.
        - arr is empty
        
        Also raises a TypeError if arr contains something other than integers
        or doubles.
        Returns the time window in samples and the start time.
        """
        # TODO: Are negatives allowed or not?
        if tmin <= 0 or tmax <= 0:
            raise Exception('Negative values for tmin and tmax not allowed.')
        if tmin >= tmax:
            raise Exception('tmax must be greater than tmin.')
        if sfreq <= 0:
            raise Exception('Sampling frequency cannot be zero or negative.')
        if arr == []:
            raise Exception('No data found.')
        
        try:    
            twindow, start = self.timewindow_to_samplewindow(sfreq, arr,
                                                             tmin, tmax)
        except TypeError:
            return
        
        return twindow, start        
        
    def find_minimum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns the last minimum and its time for a
        one dimensional numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds (default = 0)
        tmax          -- End of the time window in milliseconds
        """        
        twindow, start = self.initialize_variables(sfreq, arr, tmin, tmax)
        time = (np.argmin(twindow)+ start) * 1000 / sfreq
        return np.min(twindow), time
        
    def find_minimum2d(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns an array of last minimums for a 2d array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_minimum(sfreq, row, tmin, tmax) for row in arr]
        
    def find_maximum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns the first maximum and its time for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        twindow, start = self.initialize_variables(sfreq, arr, tmin, tmax)
        time = (np.argmax(twindow) + start) * 1000 / sfreq 
        return np.max(twindow), time
    
    def find_maximum2d(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns an array of maximums for a 2d array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_maximum(sfreq, row, tmin, tmax) for row in arr]
    
    def find_half_maximum(self, sfreq, arr, tmin=0.0,
                          tmax=sys.float_info.max):
        """
        Returns half maximum for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        (maximum, time) = self.find_maximum(sfreq, arr, tmin, tmax)
        return (maximum/2, time)
    
    def find_half_maximum2d(self, sfreq, arr, tmin=0.0,
                            tmax=sys.float_info.max):
        """
        Returns half maximums for a 2d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_maximum(sfreq, row, tmin, tmax)/2 for row in arr]
    
    def find_maximum_intensity(self, mat, w, h):
        """
        Takes a matrix and finds the coordinates of a 
        window for maximum intensity. In case of many
        equal maximums, the first one is returned.
        
        Keyword arguments:
        mat           -- A matrix
        w             -- Width of the window
        h             -- Height of the window
        """
        if w > len(mat[0]) or h > len(mat):
            raise Exception('Out of bounds.')
        maximum = 0
        xcoord = 0
        ycoord = 0
        i = IntegralImage()
        """
        Goes through the original matrix and finds the window with highest
        intensity.
        """
        for y in range(len(mat) - h+1):
            for x in range((len(mat[0]) - w)+1):
                """create a new matrix with the size of the window"""
                newmat = mat[y:h+y,x:w+x]
                """temporary variable to help finding the maximum"""
                a = i.sum_over_rectangular_area((0,0), (w-1,h-1), newmat)
                """ Save coordinates if a new maximum is found """
                if a > maximum:
                    xcoord = x
                    ycoord = y
                    maximum = a
        print maximum
        return maximum, xcoord, ycoord
    
    def timewindow_to_samplewindow(self, sfreq, arr, tmin, tmax):
        """
        Converts time window in milliseconds to samples.
        Returns the time window in samples and the starting sample.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        start = int(round((tmin/1000)*sfreq))
        stop = int(round((tmax/1000)*sfreq))+1
        return arr[start:stop], start
    