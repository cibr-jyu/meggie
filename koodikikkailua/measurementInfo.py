#!/usr/bin/env python
#coding: utf8 
"""
Created on Mar 6, 2013

@author: Jaakko Leppäkangas
"""
import mne
import datetime

class MeasurementInfo(object):
    """
    classdocs
    """

    def __init__(self, raw):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        """
        if isinstance(raw, mne.fiff.raw.Raw):
            self.raw = raw
            self.info = dict(raw.info)
            
        else:
            raise TypeError('Not a Raw object.')
    
    def get_high_pass(self):
        """
        Returns the online high pass cutoff frequency.
        """
        if self.info.get('highpass') is None:
            raise Exception('Field highpass does not exist.')
        else:
            return str(self.info.get('highpass'))
    
    def get_low_pass(self):
        """
        Returns the online low pass filter cutoff frequency.
        """
        if self.info.get('lowpass') is None:
            raise Exception('Field lowpass does not exist.')
        else:
            return str(self.info.get('lowpass'))
    
    def get_sampling_freq(self):
        """
        Returns the sample frequency.
        """
        if self.info.get('sfreq') is None:
            raise Exception('Field sfreq does not exist.')
        else:
            return str(self.info.get('sfreq'))
            
    def get_mag_channels(self):
        """
        Returns the number of magnetometer channels.
        """
        if mne.fiff.pick_types(self.raw.info, meg='mag', exclude=[]) is None:
            raise Exception('')
        else:
            return str(len(mne.fiff.pick_types(self.raw.info, meg='mag', exclude=[])))
        
    def get_grad_channels(self):
        """
        Returns the number of gradiometer channels.
        """
        if mne.fiff.pick_types(self.raw.info, meg='grad', exclude=[]) is None:
            raise Exception('')
        else:
            return str(len(mne.fiff.pick_types(self.raw.info, meg='grad', exclude=[])))
        
        
    def get_EEG_channels(self):
        """
        Returns the number of EEG channels.
        """
        if mne.fiff.pick_types(self.raw.info, meg=False, eeg=True, exclude=[]) is None:
            raise Exception('')
        else:
            return str(len(mne.fiff.pick_types(self.raw.info, meg=False, eeg=True, exclude=[])))
        
    def get_date(self):
        """
        Returns the date of measurement in form yyyy-mm-dd.
        """
        if self.info.get('meas_date') is None:
            raise Exception('Field meas_date does not exist.')
        else:
            date = datetime.datetime.fromtimestamp(self.info.get('meas_date')[0])
            return date.strftime('%Y-%m-%d')
        
    def get_stim_channel_names(self):
        """
        Returns the names of stimulus channels.
        """
        if self.info.get('ch_names') is None:
            raise Exception('Field ch_names does not exist.')
        else:
            chNames = self.info.get('ch_names')
            return [s for s in chNames if 'STI' in s]
        
    def get_events(self, STIChannel):
        """
        Returns events from a certain stimulus channel.
        
        Keyword arguments:
        STIChannel    -- name of the channel
        """
        if mne.find_events(self.raw, stim_channel=STIChannel) is None:
            raise Exception('')
        else:
            return mne.find_events(self.raw, stim_channel=STIChannel)
        
                