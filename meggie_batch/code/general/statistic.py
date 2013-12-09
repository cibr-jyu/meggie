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

from PyQt4 import QtCore

class Statistic(QtCore.QObject):
    """
    A class for statistical operations.
    """

    def __init__(self):
        QtCore.QObject.__init__(self)
          
    def calculate_averages(self, sample_arr):
        """Calculate the average values of a 2d array.
        
        Keyword arguments:
        
        sample_arr -- A 2d array containing integers or floats.
        
        return an array containing the averaged values.
        """
        average_arr = []
        for i in range(len(sample_arr[0])):
            average = 0
            for j in range(len(sample_arr)):
                try:
                    average += sample_arr[j][i]
                
                except IndexError:
                    break
            average /= len(sample_arr)
            average_arr.append(average)
            
        return average_arr                
    
    def find_minimum(self, sample_arr):
        """
        Return the minimum value and its index in sample_arr.
        
        Keyword arguments:
        
        sample_arr -- An array containing integers or floats
        """        
        min = np.min(sample_arr)
        index = np.where(sample_arr==min)[0]
        return min, index[0]
        
    def find_minimum2d(self, sample_arr):
        """
        Return minimums and their indexes in a 2d array.
        
        Keyword arguments:
        
        sample_arr -- A 2d array containing integers or floats
        
        return an array of tuples. The array's indexes correspond the first
        indexes of sample_arr. The tuples contain the return values of
        find_minimum(self, sample_arr) for the second indexes of sample_arr. 
        """
        return [self.find_minimum(row) for row in sample_arr]
        
    def find_maximum(self, sample_arr):
        """
        Return the maximum value and its index in sample_arr.
        
        Keyword arguments:
        
        sample_arr -- An array containing integers or floats
        """        
        max = np.max(sample_arr)
        index = np.where(sample_arr==max)[0]
        return max, index[0]
    
    def find_maximum2d(self, sample_arr):
        """"
        Return maximums and their indexes in a 2d array.
        
        Keyword arguments:
        
        sample_arr -- A 2d array containing integers or floats
        
        return an array of tuples. The array's indexes correspond the first
        indexes of sample_arr. The tuples contain the return values of
        find_maximum(self, sample_arr) for the second indexes of sample_arr. 
        """
        return [self.find_maximum(row) for row in sample_arr]
    
    def find_half_maximum(self, sample_arr):
        """
        Returns the 2 closest half maximums and their indexes for sample_arr.
        
        Keyword arguments:
        
        sample_arr -- a 1d array containing integers or floats
        
        Return a list containing the half_max value, its index before the max
        and its index after the max.
        """
        half_max_arr = []
        max, max_index = self.find_maximum(sample_arr)
        half_max = max/2
        half_max_arr.append(half_max)
        
        #First find the half_max_index before the max value.
        i = max_index
        while i >= 0 and sample_arr[i] > half_max:
            i -= 1
        else:
            if i < 0:
                half_max_index_minus = -1
            
            else: half_max_index_minus = i
            half_max_arr.append(half_max_index_minus)
        
        #Then find the half_max_index after the max value.
        i = max_index
        while i <= len(sample_arr) - 1 and sample_arr[i] > half_max:
            i += 1
        else:
            if i >= len(sample_arr):
                half_max_index_plus = -1
            else:
                half_max_index_plus = i
            half_max_arr.append(half_max_index_plus)                
        
        return half_max_arr
    
    def find_half_maximum2d(self, sample_arr):
        """
        Returns half maximums for sample_arr.
        
        Keyword arguments:
        
        sample_arr -- An array containing integers or floats.
        """
        return [self.find_half_maximum(row) for row in sample_arr]
    
    def integrate(self, sample_arr, start, stop):
        """Calculate the integral in sample_arr from start to stop.
        
        Keyword arguments:
        
        sample_arr -- An array containing ints or floats
        start      -- The start index of the integral
        stop       -- The last index of the integral.
        
        return the integral between start and stop.
        """
        i = start
        integral = 0
        while i <= stop and i < len(sample_arr):
            integral += sample_arr[i]
            i += 1
            
        return integral
    
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
        #I have no idea, how valid this method is...
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