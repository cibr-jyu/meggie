# coding: utf-8

"""
"""
import numpy as np
import scipy.stats as stats

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
        minimum = np.min(sample_arr)
        index = np.where(sample_arr==minimum)[0]
        return minimum, index[0]

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
        maximum = np.max(sample_arr)
        index = np.where(sample_arr==maximum)[0]
        return maximum, index[0]
    
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
        maximum, max_index = self.find_maximum(sample_arr)
        half_max = maximum/2
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

    def integrate(self, sample_arr, times, start, stop):
        """Calculate the integral in sample_arr from start to stop.

        Keyword arguments:

        sample_arr -- An array containing ints or floats
        start      -- The start index of the integral
        stop       -- The last index of the integral.

        return the integral between start and stop.
        """
        return np.trapz(sample_arr[start:stop], x=times[start:stop])
        #i = start
        #integral = 0.
        #while i <= stop and i < len(sample_arr):
        #    integral += sample_arr[i]
        #    i += 1
        #
        #return integral

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

        # Goes through the original matrix and finds the window with highest
        # intensity.
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
        return maximum, xcoord, ycoord


class SpectrumStatistics(object):

    def __init__(self, freqs, psds, log_transformed):

        self.freqs = freqs

        # ensure that we dont have log transformed data, so that
        # things make sense
        self.log_transformed = log_transformed
        if log_transformed:
            self.psds = 10**(psds.copy() / 10.0)
        else:
            self.psds = psds

        self._alpha_power = None
        self._alpha_peak = None
        self._alpha_frequency = None

    def _get_power_law(self, x, y):
        """ fits power law to given curve """

        # interpolate zeros
        mask = y == 0
        y[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), y[~mask])

        # then do log-log transform
        x_log = np.log10(x)
        y_log = np.log10(y)

        # estimate slope and intercept with linear regression
        slope, intercept, _, _, _ = stats.linregress(x_log, y_log)
        y_log_fitted = intercept + slope*x_log

        # transform the model back to original space
        y_fitted = 10**y_log_fitted

        return y_fitted

    def _calculate_alpha_peak(self):
        """ smart alpha peak finding.  """

        freqs = self.freqs
        psds = self.psds

        peak_freqs = []
        peak_ampls = []

        # find argmax in area from 7 to 13
        start = np.where(freqs >= 7)[0][0]
        end = np.where(freqs <= 13)[0][-1]

        # subtract power law out of psds to find argmax,
        # but then find the extract the amplitude from original
        for idx in range(len(psds)):
            psd = psds[idx]

            psd_powerlawless = psd - self._get_power_law(freqs, psd)

            argmax_ = np.argmax(psd_powerlawless[start:end])

            peak_freqs.append(freqs[start + argmax_])
            peak_ampls.append(psd[start + argmax_])

        self._alpha_peak = np.array(peak_ampls)
        self._alpha_frequency = np.array(peak_freqs)
        

    def _calculate_alpha_power(self):
        """ gets alpha power as integral over frequencies from 7.5 to 12.5 """
        psds = self.psds
        freqs = self.freqs

        sel = np.where((freqs >= 7.5) & (freqs <= 12.5))[0]

        power = []
        for psd in psds:
            power.append(np.trapz(psd[sel], freqs[sel]))

        self._alpha_power = np.array(power)

    @property
    def alpha_peak(self):
        if self._alpha_peak is None:
            self._calculate_alpha_peak()

        # return peak as original log transformed version
        if self.log_transformed:
            return 10 * np.log10(self._alpha_peak)

        return self._alpha_peak

    @property
    def alpha_frequency(self):
        if self._alpha_frequency is None:
            self._calculate_alpha_peak()

        return self._alpha_frequency

    @property
    def alpha_power(self):
        if self._alpha_power is None:
            self._calculate_alpha_power()

        return self._alpha_power

