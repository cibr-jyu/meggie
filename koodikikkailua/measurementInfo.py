'''
Created on Mar 6, 2013

@author: Jaakko Leppäkangas
'''
import mne
import datetime

class MeasurementInfo(object):
    '''
    classdocs
    '''

    def __init__(self, raw):
        '''
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        '''
        if isinstance(raw, mne.fiff.raw.Raw):
            self.raw = raw
            self.info = dict(raw.info)
            return self
        else:
            raise TypeError('Not a Raw object.')
    
    def getHighFreq(self):
        '''
        Returns the high pass filter value of the measured data.
        '''
        if self.info.get('highpass') is None:
            raise Exception('Field highpass does not exist.')
        else:
            return self.info.get('highpass')
    
    def getLowPass(self):
        '''
        Returns the low pass filter value of the measured data.
        '''
        if self.info.get('lowpass') is None:
            raise Exception('Field lowpass does not exist.')
        else:
            return self.info.get('lowpass')
    
    def getSampleFreq(self):
        '''
        Returns the sample frequency of the measured data.
        '''
        if self.info.get('sfreq') is None:
            raise Exception('Field sfreq does not exist.')
        else:
            return self.info.get('sfreq')
            
    def getMagChannels(self):
        '''
        Returns the number of magnetometer channels.
        '''
        if mne.fiff.pick_types(self.raw.info, meg='mag') is None:
            raise Exception('')
        else:
            return len(mne.fiff.pick_types(self.raw.info, meg='mag'))
        
    def getGradChannels(self):
        '''
        Returns the number of gradiometer channels.
        '''
        if mne.fiff.pick_types(self.raw.info, meg='grad') is None:
            raise Exception('')
        else:
            return len(mne.fiff.pick_types(self.raw.info, meg='grad'))
        
        
    def getEEGChannels(self):
        '''
        Returns the number of EEG channels.
        '''
        if mne.fiff.pick_types(self.raw.info, meg=False, eeg=True) is None:
            raise Exception('')
        else:
            return len(mne.fiff.pick_types(self.raw.info, meg=False, eeg=True))
        
    def getMeasurementDate(self):
        '''
        Returns the date of measurement in form yyyy-mm-dd.
        '''
        if self.info.get('meas_date') is None:
            raise Exception('Field meas_date does not exist.')
        else:
            date = datetime.datetime.fromtimestamp(self.info.get('meas_date')[0])
            return date.strftime('%Y-%m-%d')
        
    def getStimulusChannelNames(self):
        '''
        Returns the names of stimulus channels.
        '''
        if self.info.get('ch_names') is None:
            raise Exception('Field ch_names does not exist.')
        else:
            chNames = self.info.get('ch_names')
            return [s for s in chNames if 'STI' in s]
        
    def getEvents(self, STIChannel):
        '''
        Returns events from a certain stimulus channel.
        
        Keyword arguments:
        STIChannel    -- name of the channel
        '''
        if mne.find_events(self.raw, stim_channel=STIChannel) is None:
            raise Exception('')
        else:
            return mne.find_events(self.raw, stim_channel=STIChannel)
        
                