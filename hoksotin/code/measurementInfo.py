# coding: latin1
"""
Created on Mar 6, 2013

@author: Jaakko Leppäkangas
"""
import mne

import datetime
import re

class MeasurementInfo(object):
    """
    A class for collecting information from MEG-measurements.
    """


    def __init__(self, raw):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        Raises a TypeError if the raw object is not of type mne.fiff.Raw.
        """
        if isinstance(raw, mne.fiff.raw.Raw):
            self._raw = raw
            self._info = dict(raw.info)
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
        if mne.fiff.pick_types(self._info, meg='mag', exclude=[]) is None:
            raise Exception('Could not find magnetometers.')
        else:
            return len(mne.fiff.pick_types(self._info, meg='mag',
                                           exclude=[]))
    @property    
    def grad_channels(self):
        """
        Returns the number of gradiometer channels.
        Raises an exception if an error occurs while picking types.
        """
        if mne.fiff.pick_types(self._info, meg='grad', exclude=[]) is None:
            raise Exception('Could not find gradiometers.')
        else:
            return len(mne.fiff.pick_types(self._info, meg='grad',
                                           exclude=[]))
        
    @property    
    def EEG_channels(self):
        """
        Returns the number of EEG channels.
        Raises an exception if an error occurs while picking types.
        """
        if mne.fiff.pick_types(self._info, meg=False,
                               eeg=True, exclude=[]) is None:
            raise Exception('Could not find EEG channels.')
        else:
            return len(mne.fiff.pick_types(self._info, meg=False,
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
    def events(self, STIChannel):
        """
        Returns events from a certain stimulus channel.
        
        Keyword arguments:
        STIChannel    -- name of the channel
        Raises an exception if an error occurs while finding events.
        """
        if mne.find_events(self._raw, stim_channel=STIChannel) is None:
            raise Exception('No stimulus channel found.')
        else:
            return mne.find_events(self._raw, stim_channel=STIChannel)
    
    @property    
    def subject_name(self):
        """
        Returns the subjects name
        Raises an exception if the personal data is not a string.
        Raises an exception if the personal data is malformed.
        """
        subj_info = mne.fiff.show_fiff(self._info.get('filename'))
        if not isinstance(subj_info, str):
            raise TypeError('Personal info not found.')
        name_result = re.search('FIFF_SUBJ_LAST_NAME (.*)...', subj_info)
        if name_result == None:
            return 'Unknown'
        last_name = name_result.group(1).split(' ')
        name_result = re.search('FIFF_SUBJ_FIRST_NAME (.*)...', subj_info)
        first_name = name_result.group(1).split(' ')
        name_result = re.search('FIFF_SUBJ_MIDDLE_NAME (.*)...', subj_info)
        middle_name = name_result.group(1).split(' ')
        if len(last_name) < 3 or len(first_name) < 3 or len(middle_name) < 3:
            raise Exception('An error occurred while fetching subjects name.')
        return last_name[2] + ' ' + first_name[2] + ' ' + middle_name[2]