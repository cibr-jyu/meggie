# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
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
Created on Mar 6, 2013

@author: Kari Aliranta, Jaakko Leppakangas
Contains the MeasurementInfo-class used for collecting information from
MEG-measurement raw files.
"""
import mne
from mne.externals.six import string_types

import datetime
import re

class MeasurementInfo(object):
    """
    A class for collecting information from MEG-measurement raw files.
    """

    def __init__(self, raw):
        """
        Constructor

        Keyword arguments:
        raw           -- Raw object
        Raises a TypeError if the raw object is not of type mne.io.Raw.
        """
        if isinstance(raw, mne.io.Raw):
            self._raw = raw
            self._info = raw.info
        else:
            raise TypeError('Not a Raw object.')

    @property
    def high_pass(self):
        """
        Returns the online high pass cutoff frequency in Hz.
        Raises an exception if the field highpass does not exist.
        """
        if self._info.get('highpass') is None:
            raise Exception('Field highpass does not exist.')
        else:
            return round(self._info.get('highpass'),2)

    @property
    def low_pass(self):
        """
        Returns the online low pass filter cutoff frequency.
        Raises an exception if the field lowpass does not exist.
        """
        if self._info.get('lowpass') is None:
            raise Exception('Field lowpass does not exist.')
        else:
            return round(self._info.get('lowpass'),2)

    @property
    def sampling_freq(self):
        """
        Returns the sampling frequency.
        Raises an exception if the field sfreq does not exist.
        """
        if self._info.get('sfreq') is None:
            raise Exception('Field sfreq does not exist.')
        else:
            return round(self._info.get('sfreq'),2)

    @property
    def mag_channels(self):
        """
        Returns the number of magnetometer channels.
        Raises an exception if an error occurs while picking types.
        """
        if mne.pick_types(self._info, meg='mag', exclude=[]) is None:
            raise Exception('Could not find magnetometers.')
        else:
            return len(mne.pick_types(self._info, meg='mag',
                                           exclude=[]))

    @property    
    def grad_channels(self):
        """
        Returns the number of gradiometer channels.
        Raises an exception if an error occurs while picking types.
        """
        if mne.pick_types(self._info, meg='grad', exclude=[]) is None:
            raise Exception('Could not find gradiometers.')
        else:
            return len(mne.pick_types(self._info, meg='grad',
                                           exclude=[]))

    @property    
    def EEG_channels(self):
        """
        Returns the number of EEG channels.
        Raises an exception if an error occurs while picking types.
        """
        if mne.pick_types(self._info, meg=False,
                               eeg=True, exclude=[]) is None:
            raise Exception('Could not find EEG channels.')
        else:
            return len(mne.pick_types(self._info, meg=False,
                                           eeg=True, exclude=[]))

    @property
    def date(self):
        """
        Returns the date of measurement in form yyyy-mm-dd.
        Raises an Exception if field meas_date does not exist.
        Raises an Exception if no valid timestamp is found.
        """
        if self._info.get('meas_date') is None:
            raise Exception('Field meas_date does not exist.')
        elif not isinstance(datetime.datetime.fromtimestamp\
                        (self._info.get('meas_date')[0]), datetime.datetime):
            raise TypeError('Field meas_date is not a valid timestamp.')
        else:
            d = datetime.datetime.fromtimestamp(self._info.get('meas_date')[0])
            return d.strftime('%Y-%m-%d')

    @property    
    def stim_channel_names(self):
        """
        Returns the names of stimulus channels.
        Raises an exception if the field ch_names does not exist.
        """
        if self._info.get('ch_names') is None:
            raise Exception('Field ch_names does not exist.')
        else:
            chNames = self._info.get('ch_names')
            return [s for s in chNames if 'STI' in s]

    @property    
    def MEG_channel_names(self):
        """
        Returns the names of MEG channels.
        Raises an exception if the field ch_names does not exist.
        """
        if self._info.get('ch_names') is None:
            raise Exception('Field ch_names does not exist.')
        else:
            chNames = self._info.get('ch_names')
            return [s for s in chNames if not 'STI' in s]

    @property    
    def subject_name(self):
        """
        Returns the subjects name. If some of the name fields are nonexistent
        or empty, substitutes information with emptry strings.
        """
        try:
            subj_info = mne.io.show_fiff(self._info.get('filename'))
        except:
            subj_info = ''
        if not isinstance(subj_info, string_types) or subj_info == '':
            raise TypeError('Personal info not found.')
        last_name_result = re.search('FIFF_SUBJ_LAST_NAME (.*)...', subj_info)
        middle_name_result = re.search('FIFF_SUBJ_MIDDLE_NAME (.*)...',
                                        subj_info)
        first_name_result = re.search('FIFF_SUBJ_FIRST_NAME (.*)...', 
                                      subj_info)

        # If the file has no name fields set, don't crash
        # TODO: test with empty strings as names
        if ( last_name_result == None or last_name_result.group(1) == None ):
            last_name = ''
        else:  
            last_name_table = last_name_result.group(1).split(' ') 
            last_name = last_name_table[2]

        if ( middle_name_result == None or
            middle_name_result.group(1) == None ):
            middle_name = ''
        else: 
            middle_name_table = middle_name_result.group(1).split(' ')
            middle_name = middle_name_table[2]

        if ( first_name_result == None or first_name_result.group(1) == None ):
            first_name = ''
        else: 
            first_name_table = first_name_result.group(1).split(' ')
            first_name = first_name_table[2]

        return last_name + ' ' + first_name + ' ' + middle_name
