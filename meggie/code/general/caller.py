# coding: latin1
from matplotlib.pyplot import subplots_adjust

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
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen
This module contains caller class which calls third party software.
"""
import subprocess
import os
import glob
from copy import deepcopy
from sets import Set

import mne
from mne import fiff
from mne.fiff import evoked
from mne.time_frequency import induced_power
from mne.layouts import read_layout
from mne import filter

from mne.layouts.layout import _pair_grad_sensors
from mne.layouts.layout import _pair_grad_sensors_from_ch_names
from mne.layouts.layout import _merge_grad_data

from mne.viz import plot_topo
from mne.viz import plot_topo_power, plot_topo_phase_lock
from mne.viz import _clean_names

from measurementInfo import MeasurementInfo

from xlrd import open_workbook
from xlwt import Workbook, XFStyle
import csv

import numpy as np
import pylab as pl
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

class Caller(object):
    """
    Class for calling third party software.
    """
    def __init__(self, parent):
        """
        Constructor
        Keyword arguments:
        parent        -- Parent of this object.
        """
        self.parent = parent
    
    def call_mne_browse_raw(self, filename):
        """
        Opens mne_browse_raw with the given file as a parameter
        Keyword arguments:
        filename      -- file to open mne_browse_raw with
        Raises an exception if MNE_ROOT is not set.
        """
        if os.environ.get('MNE_ROOT') is None:
            raise Exception('Environment variable MNE_ROOT not set.')
        proc = subprocess.Popen('$MNE_ROOT/bin/mne_browse_raw --cd ' +
                                    filename.rsplit('/', 1)[0] + ' --raw ' +
                                    filename,
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()
        print "the program return code was %d" % retval
        
    def call_maxfilter(self, dic, custom):
        """
        Performs maxfiltering with the given parameters.
        Keyword arguments:
        dic           -- Dictionary of parameters
        custom        -- Additional parameters as a string
        """
        if os.environ.get('NEUROMAG_ROOT') is None:
            os.environ['NEUROMAG_ROOT'] = '/neuro'
        bs = '$NEUROMAG_ROOT/bin/util/maxfilter '
        for i in range(len(dic)):
            bs += dic.keys()[i] + ' ' + str(dic.values()[i]) + ' '
        # Add user defined parameters from the "custom" tab
        bs += custom
        print bs
        proc = subprocess.Popen(bs, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()      
        
        print "the program return code was %d" % retval
        
        outputfile = dic.get('-o')
        self.update_experiment_working_file(outputfile)
        
        """ 
        TODO Write parameter file. Implement after the actual MaxFilter
        calling has been tested. 
        self.experiment.save_parameter_file('maxfilter', raw, , dic)
        """
        self.parent.experiment.save_experiment_settings()
        
    def call_ecg_ssp(self, dic):
        """
        Creates ECG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        """
        raw_in = dic.get('i')
        tmin = dic.get('tmin')
        tmax = dic.get('tmax')
        event_id = dic.get('event-id')
        ecg_low_freq = dic.get('ecg-l-freq')
        ecg_high_freq = dic.get('ecg-h-freq')
        grad = dic.get('n-grad')
        mag = dic.get('n-mag')
        eeg = dic.get('n-eeg')
        filter_low = dic.get('l-freq')
        filter_high = dic.get('h-freq')
        
        rej_grad = dic.get('rej-grad')
        rej_mag = dic.get('rej-mag')
        rej_eeg = dic.get('rej-eeg')
        rej_eog = dic.get('rej-eog')
        
        reject = dict(grad=1e-13 * float(rej_grad),
                  mag=1e-15 * float(rej_mag),
                  eeg=1e-6 * float(rej_eeg),
                  eog=1e-6 * float(rej_eog))
        qrs_threshold = dic.get('qrs')
        flat = None
        bads = dic.get('bads')
        if bads is None:
            bads = []

        start = dic.get('tstart')
        taps = dic.get('filtersize')
        njobs = dic.get('n-jobs')
        eeg_proj = dic.get('avg-ref')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        preload = True #TODO File
        ch_name = dic.get('ch_name')
        
        if raw_in.info.get('filename').endswith('_raw.fif') or \
        raw_in.info.get('filename').endswith('-raw.fif'):
            prefix = raw_in.info.get('filename')[:-8]
            suffix = '.fif'
        else:
            prefix, suffix = os.path.splitext(raw_in.info.get('filename')) 
        
        ecg_event_fname = prefix + '_ecg-eve' + suffix
        
        if comp_ssp:
            ecg_proj_fname = prefix + '_ecg_avg_proj' + suffix
        else:
            ecg_proj_fname = prefix + '_ecg_proj' + suffix
        
        try:
            projs, events = mne.preprocessing.compute_proj_ecg(raw_in, None,
                            tmin, tmax, grad, mag, eeg,
                            filter_low, filter_high, comp_ssp, taps,
                            njobs, ch_name, reject, flat,
                            bads, eeg_proj, excl_ssp, event_id,
                            ecg_low_freq, ecg_high_freq, start, qrs_threshold)
        except Exception, err:
            raise Exception(err)
        
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)
        
        print "Writing ECG projections in %s" % ecg_proj_fname
        mne.write_proj(ecg_proj_fname, projs)
        
        print "Writing ECG events in %s" % ecg_event_fname
        mne.write_events(ecg_event_fname, events)
        
        # Write parameter file
        self.parent.experiment.\
        save_parameter_file('mne.preprocessing.compute_proj_ecg',
                            raw_in.info.get('filename'), 
                            ecg_proj_fname, 'ecgproj', dic)
        
    def call_eog_ssp(self, dic):
        """
        Creates EOG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        """
        raw_in = dic.get('i')
        tmin = dic.get('tmin')
        tmax = dic.get('tmax')
        event_id = dic.get('event-id')
        eog_low_freq = dic.get('eog-l-freq')
        eog_high_freq = dic.get('eog-h-freq')
        grad = dic.get('n-grad')
        mag = dic.get('n-mag')
        eeg = dic.get('n-eeg')
        filter_low = dic.get('l-freq')
        filter_high = dic.get('h-freq')
        
        rej_grad = dic.get('rej-grad')
        rej_mag = dic.get('rej-mag')
        rej_eeg = dic.get('rej-eeg')
        rej_eog = dic.get('rej-eog')
        
        flat = None
        bads = dic.get('bads')
        if bads is None:
            bads = []
        start = dic.get('tstart')
        taps = dic.get('filtersize')
        njobs = dic.get('n-jobs')
        eeg_proj = dic.get('avg-ref')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        preload = True #TODO File
        reject = dict(grad=1e-13 * float(rej_grad), mag=1e-15 * float(rej_mag),
                      eeg=1e-6 * float(rej_eeg), eog=1e-6 * float(rej_eog))
        
        if (raw_in.info.get('filename').endswith('_raw.fif') 
        or raw_in.info.get('filename').endswith('-raw.fif')):
            prefix = raw_in.info.get('filename')[:-8]
        else:
            prefix = raw_in.info.get('filename')[:-4]
            
        eog_event_fname = prefix + '_eog-eve.fif'
        
        if comp_ssp:
            eog_proj_fname = prefix + '_eog_avg_proj.fif'
        else:
            eog_proj_fname = prefix + '_eog_proj.fif'
            
        projs, events = mne.preprocessing.compute_proj_eog(raw_in, None,
                            tmin, tmax, grad, mag, eeg,
                            filter_low, filter_high, comp_ssp, taps,
                            njobs, reject, flat, bads,
                            eeg_proj, excl_ssp, event_id,
                            eog_low_freq, eog_high_freq, start)
        
        # TODO Reading a file
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)
        
        print "Writing EOG projections in %s" % eog_proj_fname
        mne.write_proj(eog_proj_fname, projs)
        
        print "Writing EOG events in %s" % eog_event_fname
        mne.write_events(eog_event_fname, events)
        
        # Write parameter file
        self.parent.experiment.save_parameter_file
        ('mne.preprocessing.compute_proj_eog', raw_in.info.get('filename'),
          eog_proj_fname, 'eogproj', dic)
        
    def apply_ecg(self, raw, directory):
        """
        Applies ECG projections for MEG-data.  
        Keyword arguments:
        raw           -- Data to apply to
        directory     -- Directory of the projection file
        """
        
        
        # If there already is a file with eog projections applied on it, apply
        # ecg projections on this file instead of current.
        if len(filter(os.path.isfile, 
                      glob.glob(directory + '*-eog_applied.fif'))) > 0:
            fname = glob.glob(directory + '*-eog_applied.fif')[0]
        else:
            fname = raw.info.get('filename')
        proj_file = filter(os.path.isfile,
                           glob.glob(directory + '*_ecg_proj.fif'))
        #Checks if there is exactly one projection file
        if len(proj_file) == 1:
            proj = mne.read_proj(proj_file[0])
            raw.add_proj(proj)
            appliedfilename = fname[:-4] + '-ecg_applied.fif'
            raw.save(appliedfilename)
            raw = mne.fiff.Raw(appliedfilename, preload=True)
            
        self.update_experiment_working_file(appliedfilename)
        
        self.parent.experiment.save_experiment_settings()
        
    def apply_eog(self, raw, directory):
        """
        Applies EOG projections for MEG-data.
        Keyword arguments:
        raw           -- Data to apply to
        directory     -- Directory of the projection file
        """
        if len(filter(os.path.isfile, 
                      glob.glob(directory + '*-ecg_applied.fif'))) > 0:
            fname = glob.glob(directory + '*-ecg_applied.fif')[0]
        else:
            fname = raw.info.get('filename')
        proj_file = filter(os.path.isfile,
                           glob.glob(directory + '*_eog_proj.fif'))
        # Checks if there is exactly one projection file
        if len(proj_file) == 1:
            proj = mne.read_proj(proj_file[0])
            raw.add_proj(proj)
            appliedfilename = fname[:-4] + '-eog_applied.fif'
            raw.save(appliedfilename)
            raw = mne.fiff.Raw(appliedfilename, preload=True)
        self.update_experiment_working_file(appliedfilename)
        
        self.parent.experiment.save_experiment_settings()
    
    def average(self, epochs):
        """Average epochs.
        
        Average epochs and save the evoked dataset to a file.
        Raise an exception if epochs are not found.
        
        Keyword arguments:
        
        epochs      = Epochs averaged
        """
        if epochs is None:
            raise Exception('No epochs found.')
        self.category = epochs.event_id
        """
        # Creates evoked potentials from the given events (variable 'name' 
        # refers to different categories).
        """
        self.evokeds = [epochs[name].average() for name in self.\
                        category.keys()]
        
        saveFolder = self.parent.experiment.epochs_directory + 'average/'
        
        #Get the name of the raw-data file from the current experiment.
        rawFileName = os.path.splitext(os.path.split(self.parent.experiment.\
                                                     raw_data_path)[1])[0]                      
        
        """
        Saves evoked data to disk. Seems that the written data is a list
        of evoked datasets of different events if more than one chosen when
        creating epochs.
        """
        if os.path.exists(saveFolder) is False:
            try:
                os.mkdir(saveFolder)
            except IOError:
                print 'Writing to selected folder is not allowed.'
            
        try:                
            fiff.write_evoked(saveFolder + rawFileName +\
                              '_auditory_and_visual_eeg-ave' + '.fif',\
                              self.evokeds)
        except IOError:
            print 'Writing to selected folder is not allowed.'
        
        """
        #Reading a written evoked dataset and saving it to disk.
        #TODO: setno names must be set if more than one event category.
        #fiff.Evoked can read only one dataset at a time.
        """
        #read_evoked = fiff.Evoked(prefix + '_auditory_and_visual_eeg-ave' + suffix) #setno=?)
        
        """
        Saving an evoked dataset. Can save only one dataset at a time.
        """
        #read_evoked.save(prefix + '_audvis_eeg-ave' + suffix)
                
    def draw_evoked_potentials(self, epochs):
        """
        Draws a topography representation of the evoked potentials.
        
        Keyword arguments:
        epochs
        evokeds
        category
        """
        layout = read_layout('Vectorview-all')
        
        
        
        
        """
        COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#473C8B', '#458B74',
          '#CD7F32', '#FF4040', '#ADFF2F', '#8E2323', '#FF1493']
        """
        
        
        
        
        
        #colors = ['y','m','c','r','g','b','w','k']
        colors_events = []
        i = 0
        for value in self.category.values():
            if value == 1:
                colors_events.append('w')
                #i += 1
            if value == 2:
                colors_events.append('b')
                #i += 1
            if value == 3:
                colors_events.append('r')
                #i += 1
            if value == 4:
                colors_events.append('c')
                #i += 1
            if value == 5:
                colors_events.append('m')
                #i += 1
            if value == 8:
                colors_events.append('g')
                #i += 1
            if value == 16:
                colors_events.append('y')
                #i += 1
            if value == 32:
                colors_events.append('#CD7F32')
                #i += 1
        
        self.mi = MeasurementInfo(self.parent.experiment.raw_data)
        
        #title = str(self.category.keys())
        title = ''
        fig = plot_topo(self.evokeds, layout, color=colors_events, title=title)
        fig.canvas.set_window_title(self.mi.subject_name)
        fig.show()
        
        # Create a legend to show which color belongs to which event.
        items = []
        for key in self.category.keys():
            items.append(key)
        fontP = FontProperties()
        fontP.set_size(12)
        l = pl.legend(items, loc=8, bbox_to_anchor=(-15, 19), ncol=4,\
                       prop=fontP)
        
        l.set_frame_on(False)
        # Sets the color of the event names text as white instead of black.
        for text in l.get_texts():
            text.set_color('w')
        # TODO: draggable doesn't work with l.set_frame_on(False)
        # l.draggable(True)
        
        prefix, suffix = os.path.splitext(self.parent.experiment.\
                                          raw_data.info.get('filename'))
        
        def onclick(event):
            pl.show(block=False)
            
        fig.canvas.mpl_connect('button_press_event', onclick)
        
    def average_channels(self, epochs, lobeName, channelSet=None):
        """
        Shows the averages for averaged channels in lobeName, or channelSet
        if it is provided. Only for gradiometer channels.
        
        Keyword arguments:
        epochs       -- epochs to average.
        lobename     -- the lobe over which to average.
        channelSet   -- manually input list of channels. 
        """
        
        if not channelSet == None:
            if not isinstance(channelSet, set) or len(channelSet) < 2 or \
                   not channelSet.issubset(set(epochs.ch_names)):
                raise ValueError('Please check that you have at least two ' + 
                'channels, the channels are actual channels in the epochs ' +
                'data and they are in the right form')
                return           
            channelsToAve = channelSet
            averageTitle = str(channelSet).strip('[]')
        else:
            channelsToAve = mne.selection.read_selection(lobeName)
            averageTitle = lobeName
        
        # pyPlot doesn't seem to like QStrings, need to convert to string
        averageTitleString = str(averageTitle)
        
        # Remove whitespaces from channel names (channel names in Evoked
        # objects are without whitespaces)    
        channelsToAve = _clean_names(channelsToAve)
        
        if epochs is None:
            raise Exception('No epochs found.')
        category = epochs.event_id
        
        # Creates evoked potentials from the given events (variable 'name' 
        # refers to different categories).
        evokeds = [epochs[name].average() for name in category.keys()]
        
        gradDataList = []
        for i in range(0, len(evokeds)):
            # Picks only the desired channels from the evokeds.
            evokedToAve = mne.fiff.pick_channels_evoked(evokeds[i],
                                                        channelsToAve)
                   
            # Returns channel indices for grad channel pairs in evokedToAve.
            gradsIdxs = _pair_grad_sensors_from_ch_names(evokedToAve.\
                                                         info['ch_names'])
            
            # Merges the grad channel pairs in evokedToAve
            # evokedToChannelAve = mne.fiff.evoked.Evoked(None)
            gradData = _merge_grad_data(evokedToAve.data[gradsIdxs])
            
            # Averages the gradData
            averagedGradData = np.mean(gradData, axis=0)
            
            # Links the event name and the corresponding data
            gradDataList.append((evokeds[i].comment, averagedGradData))
                
        plt.clf()
        fig = plt.figure()
        mi = MeasurementInfo(self.parent.experiment.raw_data)
        fig.canvas.set_window_title(mi.subject_name + 
             '-- channel average for ' + averageTitleString)
        fig.suptitle('Channel average for ' + averageTitleString)
        subplots_adjust(hspace=1)
                
        # Draw a separate plot for each event type
        for index, (eventName, data) in enumerate(gradDataList):
            ca = fig.add_subplot(len(gradDataList), 1, index+1) 
            ca.set_title(eventName)
            # Times information is the same as in original evokeds
            ca.plot(evokeds[0].times , data)
            
            ca.set_xlabel('Time (s)')
            # TODO Mikä yksikkö tässä, ja pitääkö skaalata?
            ca.set_ylabel('Magnitude / dB')                    
        fig.show()
    
    def TFR(self, raw, epochs, ch_index, minfreq, maxfreq, interval, ncycles,
            decim):
        """
        Plots a time-frequency representation of the data for a selected
        channel. Modified from example by Alexandre Gramfort.
        TODO should use dictionary like most other dialogs.
        Keyword arguments:
        raw           -- A raw object.
        epochs        -- Epochs extracted from the data.
        ch_index      -- Index of the channel to be used.
        minfreq       -- Starting frequency for the representation.
        maxfreq       -- Ending frequency for the representation.
        interval      -- Interval to use for the frequencies of interest.
        ncycles       -- Value used to count the number of cycles.
        decim         -- Temporal decimation factor.
        """
        evoked = epochs.average()
        data = epochs.get_data()
        times = 1e3 * epochs.times # s to ms
        evoked_data = evoked.data * 1e13
        try:
            data = data[:, ch_index:(ch_index+1), :]
            evoked_data = evoked_data[ch_index:(ch_index+1), :]
        except Exception, err:
            raise Exception('Could not find epoch data: ' + str(err))
        # Find intervals for given frequency band
        frequencies = np.arange(minfreq, maxfreq, interval)
        
        Fs = raw.info['sfreq']
        try:
            power, phase_lock = induced_power(data, Fs=Fs,
                                              frequencies=frequencies,
                                              n_cycles=ncycles, n_jobs=1,
                                              use_fft=False, decim=decim,
                                              zero_mean=True)
        except ValueError, err:
            raise ValueError(err)
        # baseline corrections with ratio
        power /= np.mean(power[:, :, times[::decim] < 0], axis=2)[:, :, None]
        fig = pl.figure()
        #pl.clf()
        pl.subplots_adjust(0.1, 0.08, 0.96, 0.94, 0.2, 0.63)
        pl.subplot(3, 1, 1)
        pl.plot(times, evoked_data.T)
        pl.title('Evoked response (%s)' % evoked.ch_names[ch_index])
        pl.xlabel('time (ms)')
        if str(evoked.ch_names[ch_index]).endswith('1'):
            pl.ylabel('Magnetic Field (fT)')
        else:
            pl.ylabel('Magnetic Field (fT/cm)')
        pl.xlim(times[0], times[-1])
        #pl.ylim(-150, 300)
        
        pl.subplot(3, 1, 2)
        pl.imshow(20 * np.log10(power[0]), extent=[times[0], times[-1],
                                                   frequencies[0],
                                                   frequencies[-1]],
                  aspect='auto', origin='lower')
        pl.xlabel('Time (ms)')
        pl.ylabel('Frequency (Hz)')
        pl.title('Induced power (%s)' % evoked.ch_names[ch_index])
        pl.colorbar()
        
        pl.subplot(3, 1, 3)
        pl.imshow(phase_lock[0], extent=[times[0], times[-1],
                                         frequencies[0], frequencies[-1]],
                  aspect='auto', origin='lower')
        pl.xlabel('Time (ms)')
        pl.ylabel('Frequency (Hz)')
        pl.title('Phase-lock (%s)' % evoked.ch_names[ch_index])
        pl.colorbar()
        fig.show()
        
        
    def TFR_topology(self, raw, epochs, reptype, minfreq, maxfreq, decim, mode,  
                     blstart, blend, interval, ncycles):
        """
        Plots time-frequency representations on topographies for MEG sensors.
        Modified from example by Alexandre Gramfort and Denis Engemann.
        TODO should use dictionary like most other dialogs.
        Keyword arguments:
        raw           -- A raw object.
        epochs        -- Epochs extracted from the data.
        reptype       -- Type of representation (induced or phase).
        minfreq       -- Starting frequency for the representation.
        maxfreq       -- Ending frequency for the representation.
        decim         -- Temporal decimation factor.
        mode          -- Rescaling mode (logratio | ratio | zscore |
                         mean | percent).
        blstart       -- Starting point for baseline correction.
        blend         -- Ending point for baseline correction.
        interval      -- Interval to use for the frequencies of interest.
        ncycles       -- Value used to count the number of cycles.
        """
        # TODO: Let the user define the title of the figure.
        data = epochs.get_data()
        
        # Find intervals for given frequency band
        frequencies = np.arange(minfreq, maxfreq, interval)
        Fs = raw.info['sfreq']
        decim = 3
        
        try:
            power, phase_lock = induced_power(data, Fs=Fs,
                                              frequencies=frequencies,
                                              n_cycles=ncycles, n_jobs=3,
                                              use_fft=False, decim=decim,
                                              zero_mean=True)
        except ValueError, err:
            raise ValueError(err)
        layout = read_layout('Vectorview-all')
        baseline = (blstart, blend)  # set the baseline for induced power
        #mode = 'ratio'  # set mode for baseline rescaling
        
        if ( reptype == 'induced' ):
            title='TFR topology: ' + 'Induced power'
            fig = plot_topo_power(epochs, power, frequencies, layout,
                            baseline=baseline, mode=mode, decim=decim, 
                            vmin=0., vmax=14, title=title)
            fig.show()
        else: 
            title = 'TFR topology: ' + 'Phase locking'
            fig = plot_topo_phase_lock(epochs, phase_lock, frequencies, layout,
                     baseline=baseline, mode=mode, decim=decim, title=title)
            fig.show()  
            
        def onclick(event):
            pl.show(block=False)
        
        fig.canvas.mpl_connect('button_press_event', onclick)
        
    def magnitude_spectrum(self, raw, ch_index):
        """
        Plots magnitude spectrum of the selected channel.
        Keyword arguments:
        raw           -- A raw object.
        ch_index      -- Index of the channel to be used.
        """
        #data, times = raw[ch_index,:]
        data = raw[ch_index,:][0]
        data = np.squeeze(data)
        ch_fft = np.fft.fft(data)
        ffta = np.absolute(ch_fft)
        logdata = 20*np.log10(ffta)
        hlogdata = logdata[0:int(len(logdata) / 2)]
        fs = raw.info.get('sfreq')
        f = np.linspace(0, fs/2, len(hlogdata))
        pl.plot(f, hlogdata)
        pl.ylabel('Magnitude / dB')
        pl.xlabel('Hz')
        pl.show()
                            
    def filter(self, dataToFilter, samplerate, dic):
        """
        Filters the data array in place according to parameters in paramDict.
        Depending on the parameters, the filter is lowpass, highpass or
        bandstop (notch) filter.
        
        Keyword arguments:
        
        dataToFilter         -- array of data to filter
        samplerate           -- intended samplerate of the array
        dic                  -- Dictionary with filtering parameters
        
        """
        
        
        if dic.get('lowpass') == True:
            filteredData = filter.low_pass_filter(dataToFilter, samplerate, 
                        dic.get('low_cutoff_freq'), dic.get('low_length'),
                        dic.get('low_trans_bandwidth'),'fft', None, None, 3, 
                        True)
        
        if dic.get('highpass') == True:
            filteredData = filter.high_pass_filter(dataToFilter, samplerate, 
                        dic.get('high_cutoff_freq'), dic.get('high_length'),
                        dic.get('high_trans_bandwidth'),'fft', None, None, 3, 
                        True)
        
        return filteredData
                          
    def update_experiment_working_file(self, fname):
        """
        Changes the current working file for the experiment the caller relates
        to.
        fname    -- name of the new working file 
        """
        self.parent.experiment.working_file = fname        

    def write_events(self, events):
        """
        Saves the events into an Excel file (.xls). 
        Keyword arguments:
        events           -- Events to be saved
        """
        wbs = Workbook()
        ws = wbs.add_sheet('Events')
        styleNumber = XFStyle()
        styleNumber.num_format_str = 'general'
        sizex = events.shape[0]
        sizey = events.shape[1]
                
        path_to_save = self.parent.experiment.subject_directory
        
        # Saves events to csv file for easier modification with text editors.
        csv_file = open(path_to_save + '/events.csv', 'w')
        csv_file_writer = csv.writer(csv_file)
        csv_file_writer.writerows(events)
        csv_file.close()

        for i in range(sizex):
            for j in range(sizey):
                ws.write(i, j, events[i][j], styleNumber)
        wbs.save(path_to_save + '/events.xls')
        #TODO: muuta filename kayttajan maarittelyn mukaiseksi

    def read_events(self, filename):
        """
        Reads the events from a chosen excel file.
        Keyword arguments:
        filename      -- File to read from.
        """
        wbr = open_workbook(filename)
        sheet = wbr.sheet_by_index(0)
        return sheet
    
