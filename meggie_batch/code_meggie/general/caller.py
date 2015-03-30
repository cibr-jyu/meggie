# coding: latin1
"""
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen
This module contains caller class which calls third party software.
"""

import subprocess
import os
import glob
import traceback
import fnmatch
import re
import shutil

from PyQt4 import QtCore, QtGui

import mne
from mne.time_frequency import induced_power
from mne.layouts import read_layout
from mne.layouts.layout import _pair_grad_sensors_from_ch_names
from mne.layouts.layout import _merge_grad_data
from mne.viz import plot_topo
from mne.viz import iter_topography
from mne.utils import _clean_names
from mne.time_frequency.tfr import tfr_morlet
from mne.time_frequency import compute_raw_psd
# TODO find these or equivalent in mne 0.8
# from mne.viz import plot_topo_power, plot_topo_phase_lock
#from mne.viz import _clean_names

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import subplots_adjust
from os import listdir
from os.path import isfile, join
from subprocess import CalledProcessError
from threading import Thread, Event, activeCount
from multiprocessing.pool import ThreadPool
from time import sleep

from ui.general import messageBoxes
import fileManager
from ui.sourceModeling.holdCoregistrationDialogMain import holdCoregistrationDialog
from ui.sourceModeling.forwardModelSkipDialogMain import ForwardModelSkipDialog
from measurementInfo import MeasurementInfo
from singleton import Singleton
from copy import deepcopy


@Singleton
class Caller(object):
    """
    Class for simple of calling third party software. Includes methods that
    require input from single source (usually a dialog) and produce simple
    output (usually a single matplotlib window). 
    More complicated functionality like epoching can be found in separate
    classes.
    """
    parent = None
    _experiment = None
    e = Event()
    result = None #Used for storing exceptions from threads.
    
    def __init__(self):
        """
        Constructor
        """
        print "Caller created"
        
        
    def setParent(self, parent):
        """
        Keyword arguments:
        parent        -- Parent of this object.
        """
        self.parent = parent

        
    @property
    def experiment(self):
        return self._experiment

    
    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment
        
    
    def activate_subject(self, name):
        """
        Activates the subject.
        Keyword arguments:
        name      -- Name of the subject to activate.
        """
        if name == '':
            return
        pool = ThreadPool(processes=1)

        async_result = pool.apply_async(self.experiment.activate_subject, 
                                        (name,))
        while(True):
            sleep(0.2)
            if self.experiment.is_ready(): break;
            self.parent.update_ui()
            
        return_val = async_result.get()
        pool.terminate()
        if not return_val == 0:
            self.messageBox = messageBoxes.shortMessageBox('Could not set ' + \
                                        name + ' as active subject. ' + \
                                        'Check console.')
            self.messageBox.show()
        

    def call_mne_browse_raw(self, filename):
        """
        Opens mne_browse_raw with the given file as a parameter
        Keyword arguments:
        filename      -- file to open mne_browse_raw with
        Raises an exception if MNE_ROOT is not set.
        """
        print str(self.parent)
        if os.environ.get('MNE_ROOT') is None:
            raise Exception('Environment variable MNE_ROOT not set.')
        
        # TODO: os.path.join
        proc = subprocess.Popen('$MNE_ROOT/bin/mne_browse_raw --cd ' +
                                    filename.rsplit('/', 1)[0] + ' --raw ' +
                                    filename,
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        #retval = proc.wait()
        #print "the program return code was %d" % retval
     
        
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
        self.experiment.save_experiment_settings()
   
        
    def call_ecg_ssp(self, dic):
        """
        Creates ECG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        """
        self.e.clear()
        self.result = None
        self.thread = Thread(target = self._call_ecg_ssp, args=(dic,))
        self.thread.start()
        while True:
            sleep(0.2)
            self.parent.update_ui()
            if self.e.is_set(): break
        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            return -1
        return 0
        
    def _call_ecg_ssp(self, dic):
        """
        Performed in a worker thread.
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
        else:
            prefix, _ = os.path.splitext(raw_in.info.get('filename')) 
        
        ecg_event_fname = prefix + '_ecg-eve.fif'
        
        if comp_ssp:
            ecg_proj_fname = prefix + '_ecg_avg_proj.fif'
        else:
            ecg_proj_fname = prefix + '_ecg_proj.fif'
        
        try:
            projs, events = mne.preprocessing.compute_proj_ecg(raw_in, None,
                            tmin, tmax, grad, mag, eeg,
                            filter_low, filter_high, comp_ssp, taps,
                            njobs, ch_name, reject, flat,
                            bads, eeg_proj, excl_ssp, event_id,
                            ecg_low_freq, ecg_high_freq, start, qrs_threshold)
        except Exception, err:
            self.result = err
            self.e.set()
            return -1
        
        if len(events) == 0:
            self.result = Exception('No ECG events found. Change settings.')
            #message = 'No ECG events found. Change settings.'
            #self.messageBox = messageBoxes.shortMessageBox(message)
            #self.messageBox.show()
            self.e.set()
            return -1
        
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)
        
        print "Writing ECG projections in %s" % ecg_proj_fname
        try:
            mne.write_proj(ecg_proj_fname, projs)
        except Exception as e:
            self.result = e
            self.e.set()
            return -1
        
        print "Writing ECG events in %s" % ecg_event_fname
        try:
            mne.write_events(ecg_event_fname, events)
        except Exception as e:
            self.result = e
            print str(e)
            self.e.set()
            return -1
        
        self.e.set()
        """
        # Write parameter file
        self.parent.experiment.\
        save_parameter_file('mne.preprocessing.compute_proj_ecg',
                            raw_in.info.get('filename'), 
                            ecg_proj_fname, 'ecgproj', dic)
        """
     
        
    def call_eog_ssp(self, dic):
        """
        Creates EOG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        """
        self.e.clear()
        self.result = None
        self.thread = Thread(target = self._call_eog_ssp, args=(dic,))
        self.thread.start()
        while True:
            sleep(0.2)
            self.parent.update_ui()
            if self.e.is_set(): break
        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            return -1
        return 0
        
    def _call_eog_ssp(self, dic):
        """
        Performed in a worker thread.
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
        try:
            projs, events = mne.preprocessing.compute_proj_eog(raw_in, None,
                            tmin, tmax, grad, mag, eeg,
                            filter_low, filter_high, comp_ssp, taps,
                            njobs, reject, flat, bads,
                            eeg_proj, excl_ssp, event_id,
                            eog_low_freq, eog_high_freq, start)
        except Exception as e:
            print 'Exception while computing eog projections.'
            self.result = e
            self.e.set() 
            return;
        # TODO Reading a file
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)
        
        print "Writing EOG projections in %s" % eog_proj_fname
        mne.write_proj(eog_proj_fname, projs)
        
        print "Writing EOG events in %s" % eog_event_fname
        mne.write_events(eog_event_fname, events)
        self.e.set()
        """
        # Write parameter file
        self.parent.experiment.\
        save_parameter_file('mne.preprocessing.compute_proj_eog',
                            raw_in.info.get('filename'),
                            eog_proj_fname, 'eogproj', dic)
        """
        
        
    def apply_ecg(self, raw, directory):
        """
        Applies ECG projections for MEG-data.  
        Keyword arguments:
        raw           -- Data to apply to
        directory     -- Directory of the projection file
        """
        self.e.clear()
        self.result = None
        self.thread = Thread(target = self._apply_ecg, args=(raw, directory))
        self.thread.start()
        while True:
            sleep(0.2)
            self.parent.update_ui()
            if self.e.is_set(): break
        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            self.result = None
            return 1
        else:
            return 0
        
    def _apply_ecg(self, raw, directory):
        """
        Performed in a worker thread.
        """
        # If there already is a file with eog projections applied on it, apply
        # ecg projections on this file instead of current.
        if len(filter(os.path.isfile, 
                      glob.glob(directory + '/*-eog_applied.fif'))) > 0:
            fname = glob.glob(directory + '/*-eog_applied.fif')[0]
        else:
            fname = raw.info.get('filename')
        proj_file = filter(os.path.isfile,
                           glob.glob(directory + '/*_ecg_*proj.fif'))
        if len(proj_file) == 0:
            message = 'There is no proj file.'
            self.result = Exception(message)
            
        #Checks if there is exactly one projection file.
        # TODO: If there is more than one projection file, which one should
        # be added? The newest perhaps.
        if len(proj_file) == 1:
            proj = mne.read_proj(proj_file[0])
            raw.add_proj(proj)
            # If the suffix is shorter or longer than 4, this might
            # create some problems later on when doing checks
            # using the generated filename.
            # appliedfilename = fname[:-4] + '-ecg_applied.fif'
            
            # TODO: ecg_avg_applied.fif if ssp checked 
            appliedfilename = fname.split('.')[-2] + '-ecg_applied.fif'
            raw.save(appliedfilename)
            raw = mne.io.RawFIFF(appliedfilename, preload=True)
        else:
            self.result = Exception('There is more than one ECG projection '+ \
                                    'file to apply. ' + \
                    'Remove all others but the one you want to apply.\n' + \
                    'Projection files are found under subject folder: ' + \
                    self.experiment.active_subject._subject_path)
            self.e.set()
            return
        self.update_experiment_working_file(appliedfilename, raw)
        self.e.set()
        
        
    def apply_eog(self, raw, directory):
        """
        Applies EOG projections for MEG-data.
        Keyword arguments:
        raw           -- Data to apply to
        directory     -- Directory of the projection file
        """
        self.e.clear()
        self.result = None
        self.thread = Thread(target = self._apply_eog, args=(raw, directory))
        self.thread.start()
        while True:
            sleep(0.2)
            self.parent.update_ui()
            if self.e.is_set(): break
        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            self.result = None
            return 1
        else:
            return 0
            
    
    def _apply_eog(self, raw, directory):
        """
        Performed in a worker thread.
        """
        if len(filter(os.path.isfile, 
                      glob.glob(directory + '/*-ecg_applied.fif'))) > 0:
            fname = glob.glob(directory + '/*-ecg_applied.fif')[0]
        else:
            fname = raw.info.get('filename')
        proj_file = filter(os.path.isfile,
                           glob.glob(directory + '/*_eog_*proj.fif'))
        if len(proj_file) == 0:
            self.result = Exception('There is no proj file.')
            self.e.set()
        #Checks if there is exactly one projection file.
        # TODO: If there is more than one projection file, which one should
        # be added? The newest?
        if len(proj_file) == 1:
            proj = mne.read_proj(proj_file[0])
            raw.add_proj(proj)
            # If the suffix is shorter or longer than 4, this might
            # create some problems later on when doing checks
            # using the generated filename.
            #appliedfilename = fname[:-4] + '-eog_applied.fif'
            
            # TODO: eog_avg_applied.fif if ssp checked
            appliedfilename = fname.split('.')[-2] + '-eog_applied.fif'
            raw.save(appliedfilename)
            raw = mne.io.RawFIFF(appliedfilename, preload=True)
        else:
            self.result = Exception('There is more than one EOG projection '+ \
                                    'file to apply. ' + \
                    'Remove all others but the one you want to apply.\n' + \
                    'Projection files are found under subject folder: ' + \
                    self.experiment.active_subject._subject_path) 
            self.e.set()
            return
        self.update_experiment_working_file(appliedfilename, raw)
        self.experiment.save_experiment_settings()
        self.e.set()
 
    
    def average(self, epochs, category):
        """Average epochs.
        
        Average epochs and save the evoked dataset to a file.
        Raise an exception if epochs are not found.
        
        Keyword arguments:
        
        epochs      = Epochs averaged
        """
        
        if epochs is None:
            raise Exception('No epochs found.')
        #self.category = epochs.event_id
        """
        # Creates evoked potentials from the given events (variable 'name' 
        # refers to different categories).
        """
        evokeds = []
        #[epochs._raw[name].average() for name in category.keys()]
        for epoch in epochs: # epoch == single set of epochs
            for name in category.keys():
                if name in epoch._raw.event_id:
                    evokeds.append(epoch._raw[name].average()) #self.category.keys()
        
        saveFolder = os.path.join(self.experiment.active_subject._epochs_directory, 'average')
        
        #Get the name of the raw-data file from the current experiment.
        #rawFileName = os.path.splitext(os.path.split(self.parent.experiment.\
        #                                             raw_data_path)[1])[0]                      
        rawFileName = os.path.splitext(os.path.split(self.experiment.\
        _working_file_names[self.experiment._active_subject_name])[1])[0]
        
        return evokeds
        """
        Saves evoked data to disk. Seems that the written data is a list
        of evoked datasets of different events if more than one chosen when
        creating epochs.
        """
        """
        if os.path.exists(saveFolder) is False:
            try:
                os.mkdir(saveFolder)
            except IOError:
                print 'Writing to selected folder is not allowed.'
            
        try:                
            fiff.write_evoked(saveFolder + rawFileName +\
                              '_auditory_and_visual_eeg-ave' + '.fif',\
                              evokeds)
        except IOError:
            print 'Writing to selected folder is not allowed.'
        """
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
 
                
    def draw_evoked_potentials(self, evokeds, layout):#, category):
        """
        Draws a topography representation of the evoked potentials.
        
        Keyword arguments:
        epochs
        evokeds
        category
        """
        layout = read_layout(layout)

        #layout = read_layout('Vectorview-all')
        
        # Checks if there are whitespaces in evokeds ch_names.
        # If not, whitespaces in layout.names need to be removed.
        #if not ' ' in evokeds[0].ch_names[0]:
            # TODO: add whitespace on evokeds ch_names or remove whitespace
            # from layout names.
            #layout.names = _clean_names(layout.names, remove_whitespace=True)
        #    layout.names = [str(name).replace(' ','') for name in layout.names]
        """
        COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#473C8B', '#458B74',
          '#CD7F32', '#FF4040', '#ADFF2F', '#8E2323', '#FF1493']
        """
        colors = ['y','m','c','r','g','b','w','k']
        """
        colors_events = []
        #i = 0
        for value in category.values():
            if value == 1:
                colors_events.append('w')
                #i += 1
            elif value == 2:
                colors_events.append('b')
                #i += 1
            elif value == 3:
                colors_events.append('r')
                #i += 1
            elif value == 4:
                colors_events.append('c')
                #i += 1
            elif value == 5:
                colors_events.append('m')
                #i += 1
            elif value == 8:
                colors_events.append('g')
                #i += 1
            elif value == 16:
                colors_events.append('y')
                #i += 1
            elif value == 32:
                colors_events.append('#CD7F32')
                #i += 1
        """
        mi = MeasurementInfo(self.experiment.active_subject.working_file)
        
        #title = str(self.category.keys())
        title = mi.subject_name
        fig = plot_topo(evokeds, layout,
                        color=colors[:len(evokeds)], title=title)
        conditions = [e.comment for e in evokeds]
        positions = np.arange(0.025, 0.025+0.04*len(evokeds), 0.04)
        for cond, col, pos in zip(conditions, colors[:len(evokeds)], positions):#np.arange(0.025, len(evokeds) * 0.02 + 0.025, 0.2)):
            plt.figtext(0.775, pos, cond, color=col, fontsize=12)

        #fig = plot_topo(evokeds, layout, color=colors_events, title=title)
        #fig.canvas.set_window_title(mi.subject_name)
        
        # fig.set_rasterized(True) <-- this didn't help with the problem of 
        # drawing figures everytime figure size changes.
        
        # Paint figure background with white color.
        #fig.set_facecolor('w')
        
        fig.show()
        
        # Create a legend to show which color belongs to which event.
        """
        items = []
        for key in category.keys():
            items.append(key)
        fontP = FontProperties()
        fontP.set_size(12)
        """
        #l = plt.legend(items, loc=8, bbox_to_anchor=(-15, 19), ncol=4,\
        #               prop=fontP)
        
        #l.set_frame_on(False)
        # Sets the color of the event names text as white instead of black.
        #for text in l.get_texts():
        #    text.set_color('w')
        # TODO: draggable doesn't work with l.set_frame_on(False)
        # l.draggable(True)
        
        prefix, suffix = os.path.splitext(self.experiment.active_subject.\
                                          _working_file.info.get('filename'))
        
        def onclick(event):
            plt.show(block=False)
            
        fig.canvas.mpl_connect('button_press_event', onclick)
      
        
    def average_channels(self, epochs_name, lobeName, channelSet=None):
        """
        Shows the averages for averaged channels in lobeName, or channelSet
        if it is provided. Only for gradiometer channels.
        
        Keyword arguments:
        epochs_name  -- name of the epochs to average.
        lobename     -- the lobe over which to average.
        channelSet   -- manually input list of channels. 
        """
        self.e.clear()
        self.result = None
        pool = ThreadPool(processes=1)

        async_result = pool.apply_async(self._average_channels, 
                                        (epochs_name, lobeName, channelSet,))
        while(True):
            sleep(0.2)
            if self.e.is_set(): break;
            self.parent.update_ui()

        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            self.result = None
            return 
        averageTitleString, gradDataList, evokeds = async_result.get()
        pool.terminate()
        #averageTitleString = return_val[0]
        #gradDataList = return_val[1]
        #evokeds = return_val[2]
        
        # Plotting:
        plt.clf()
        fig = plt.figure()
        mi = MeasurementInfo(self.experiment.active_subject._working_file)
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
            # TODO Mika yksikko tassa, ja pitaako skaalata?
            ca.set_ylabel('Magnitude / dB')                    
        fig.show()
        
    
    def _average_channels(self, epochs_name, lobeName, channelSet=None):
        """
        Performed in a worker thread.
        """
        epochs = self.experiment.active_subject._epochs[epochs_name].raw
        if not channelSet == None:
            if not isinstance(channelSet, set) or len(channelSet) < 2 or \
                   not channelSet.issubset(set(epochs.ch_names)):
                self.result = ValueError('Please check that you have at least two ' + 
                'channels, the channels are actual channels in the epochs ' +
                'data and they are in the right form')
                self.e.set()
                return           
            channelsToAve = channelSet
            averageTitle = str(channelSet).strip('[]')
        else:
            try:
                channelsToAve = mne.selection.read_selection(lobeName)
            except Exception as e:
                self.result = e
                self.e.set()
                return
            averageTitle = lobeName
        
        # pyPlot doesn't seem to like QStrings, need to convert to string
        averageTitleString = str(averageTitle)
        
        if epochs is None:
            self.result = Exception('No epochs found.')
            self.e.set()
            return
        category = epochs.event_id
        
        # Creates evoked potentials from the given events (variable 'name' 
        # refers to different categories).
        evokeds = [epochs[name].average() for name in category.keys()]
        
        # Channel names in Evoked objects may or may not have whitespaces
        # depending on the measurements settings,
        # need to check and adjust channelsToAve accordingly.
        channelNameString = evokeds[0].info['ch_names'][0]
        if re.match("^MEG[0-9]+", channelNameString):
            channelsToAve = _clean_names(channelsToAve)
        
        gradDataList = []
        for i in range(0, len(evokeds)):
            print "Calculating channel averages for " + averageTitleString + \
                 "\n" + \
                "Channels in evoked set " + str(i) + ":"
            print evokeds[i].info['ch_names']
            
            # TODO: check that channels to ave has whitespace between string
            # and numbers.
            
            # Picks only the desired channels from the evokeds.
            try:
                evokedToAve = mne.pick_channels_evoked(evokeds[i], 
                                                       channelsToAve)
            except Exception as e:
                self.result = e
                self.e.set()
                return
                   
            # Returns channel indices for grad channel pairs in evokedToAve.
            gradsIdxs = _pair_grad_sensors_from_ch_names(evokedToAve.\
                                                         info['ch_names'])
            
            # Merges the grad channel pairs in evokedToAve
            # evokedToChannelAve = mne.fiff.evoked.Evoked(None)
            if len(gradsIdxs) > 0:
                gradData = _merge_grad_data(evokedToAve.data[gradsIdxs])
            
                # Averages the gradData
                averagedGradData = np.mean(gradData, axis=0)
            
                # Links the event name and the corresponding data
                gradDataList.append((evokeds[i].comment, averagedGradData))
            else:
                averagedData = np.mean(evokeds[i].data, axis=0)
                gradDataList.append((evokeds[i].comment, averagedData))
        self.e.set()
        return averageTitleString, gradDataList, evokeds
    
    
    def plot_group_average(self, groups, layout):
        """
        Plots group average of all subjects in the experiment.
        Keyword arguments:
        groups           -- A list of group names.
        """
        self.e.clear()
        self.result = None
        pool = ThreadPool(processes=1)

        async_result = pool.apply_async(self._group_average, 
                                        (groups,))
        while(True):
            sleep(0.2)
            if self.e.is_set(): break;
            self.parent.update_ui()

        if not self.result is None:
            if isinstance(self.result, Warning): #TODO: Maybe should move GUI actions elsewhere.
                QtGui.QApplication.restoreOverrideCursor()
                reply = QtGui.QMessageBox.question(self.parent, 
                            "Evoked responses not found from every subject.",
                            str(self.result) + \
                            "Draw the evoked potentials anyway?",
                            QtGui.QMessageBox.Yes,
                            QtGui.QMessageBox.No)
                self.result = None
                if reply == QtGui.QMessageBox.No:
                    return
                else:
                    QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
            else:
                self.messageBox = messageBoxes.shortMessageBox(str(self.result))
                self.messageBox.show()
                self.result = None
                return
            
        evokeds, groups = async_result.get()

        pool.terminate()
        
        write2file = True
        if write2file: #TODO add option in GUI for this
            exp_path = os.path.join(self.experiment.workspace,
                                    self.experiment.experiment_name)
            if not os.path.isdir(exp_path + '/output'):
                os.mkdir(exp_path + '/output')
            fName = exp_path + '/output/group_average.txt'
            f = open(fName, 'w')
            f.write('Times, ')
            for time in evokeds[0].times:
                f.write(repr(time))
                f.write(', ')
            f.write('\n')
            i = 0
            for evoked in evokeds:
                f.write(repr(groups[i] + '\n'))
                i = i + 1
                for ch_idx in xrange(len(evoked.ch_names)):
                    f.write(repr(evoked.ch_names[ch_idx] + ', '))
                    for j in xrange(len(evoked.data[ch_idx])):
                        f.write(repr(evoked.data[ch_idx][j]))
                        f.write(', ')
                    f.write('\n')
            f.close()
            
        print "Plotting evoked potentials..."
        self.parent.update_ui()
        self.draw_evoked_potentials(evokeds, layout)
        
        
    def _group_average(self, groups):
        """
        Performed in a worker thread.
        """
        chs = self.experiment.active_subject.working_file.info['ch_names']
        evokeds = dict()
        eweights = dict()
        for group in groups:
            evokeds[group] = dict()
            for ch in chs:
                evokeds[group][ch] = []                
            eweights[group] = []
        subjects = self.experiment.get_subjects()
        files2ave = []
        for subject in subjects:
            directory = subject._evokeds_directory
            print directory
            files = [ f for f in listdir(directory)\
                      if isfile(join(directory,f)) and f.endswith('.fif') ]
            for f in files:
                fgroups = re.split('[\[\]]', f) # '1-2-3'
                if not len(fgroups) == 3: 
                    continue 
                fgroups = re.split('[-]', fgroups[1]) # ['1','2','3']
                if sorted(fgroups) == sorted(groups):
                    files2ave.append(directory + '/' + f)
        
        print "Found " + str(len(files2ave)) + " subjects with evoked " + \
                        "responses labeled: " + str(groups)
        if len(files2ave) < len(subjects):
            self.result = Warning("Found only " + str(len(files2ave)) + \
                                  " subjects of " + str(len(subjects)) + \
                                  " with evoked responses labeled: " + \
                                  str(groups) + "!\n")
        
        evokedTmin = 0
        evokedInfo = []
        print files2ave
        for f in files2ave:
            for group in groups:
                try:
                    evoked = mne.read_evokeds(f, condition=group)
                    evokedTmin = evoked.first / evoked.info['sfreq']
                    evokedInfo = evoked.info
                except Exception as e:
                    self.result = e
                    self.e.set()
                    return
                info = evoked.info['ch_names']
                for cidx in xrange(len(info)):
                    evokeds[group][info[cidx]].append(evoked.data[cidx])
                eweights[group].append(evoked.nave)
        evs = []
        usedChannels = []
        bads = []
        for group in groups:
            max_key = max(evokeds[group], key= lambda x: len(evokeds[group][x]))
            length = len(evokeds[group][max_key])
            evokedSet = []
            for ch in chs:
                if len(evokeds[group][ch]) < length:
                    if not ch in bads: bads.append(ch)
                    continue
                try:
                    if not ch in usedChannels: usedChannels.append(ch)
                    data = evokeds[group][ch]
                    w = eweights[group]
                    ave = np.average(data, axis=0, weights=w)
                    evokedSet.append(ave)
                except Exception as e:
                    self.result = e
                    self.e.set()
                    return 
            evs.append(deepcopy(evokedSet))

        print 'Used channels: ' + str(usedChannels)
        print '\nBad channels: ' + str(bads)
        evokedInfo['ch_names'] = usedChannels
        evokedInfo['bads'] = bads
        evokedInfo['nchan'] = len(usedChannels)

        averagedEvokeds = []
        try:
            for groupidx in xrange(len(groups)):
                averagedEvokeds.append(mne.EvokedArray(evs[groupidx], 
                                                    info=evokedInfo,
                                                    tmin=evokedTmin, 
                                                    comment=groups[groupidx]))
        except Exception as e:
            print str(e)
            self.result = e
            self.e.set()
            return
                
        self.e.set()
        return averagedEvokeds, groups
        
    
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
        plt.close()
        self.e.clear()
        self.result = None
        pool = ThreadPool(processes=1)
        
        # Find intervals for given frequency band
        frequencies = np.arange(minfreq, maxfreq, interval)
        
        async_result = pool.apply_async(self._TFR, 
                                        (raw, epochs, ch_index, frequencies, 
                                         ncycles, decim))
        while(True):
            sleep(0.2)
            if self.e.is_set(): break;
            self.parent.update_ui()

        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            self.result = None
            return 
        
        power, phase_lock, times, evoked, evoked_data = async_result.get()
        pool.terminate()

        print 'Plotting TFR...'
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
        
        
    def _TFR(self, raw, epochs, ch_index, frequencies, ncycles, decim):
        """
        Perfromed in a worker thread.
        """
        print 'Computing induced power...'
        evoked = epochs.average()
        data = epochs.get_data()
        times = 1e3 * epochs.times # s to ms
        evoked_data = evoked.data * 1e13
        try:
            data = data[:, ch_index:(ch_index+1), :]
            evoked_data = evoked_data[ch_index:(ch_index+1), :]
        except Exception, err:
            self.result = Exception('Could not find epoch data: ' + str(err))
            self.e.set()
            return
        
        Fs = raw.info['sfreq']
        try:
            power, phase_lock = induced_power(data, Fs=Fs,
                                              frequencies=frequencies,
                                              n_cycles=ncycles, n_jobs=1,
                                              use_fft=False, decim=decim,
                                              zero_mean=True)
        except ValueError, err:
            self.result = err
            self.e.set()
            return
        # baseline corrections with ratio
        power /= np.mean(power[:, :, times[::decim] < 0], axis=2)[:, :, None]
        print 'Done'
        self.e.set()
        return power, phase_lock, times, evoked, evoked_data
        
        
    def TFR_topology(self, raw, epochs, reptype, minfreq, maxfreq, decim, mode,  
                     blstart, blend, interval, ncycles, lout, ch_type='mag'):
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
        layout        -- Layout to use.
        ch_type       -- Determines if the topomap plotting uses eeg or mag.
        """
        plt.close()
        print "Number of threads active", activeCount()
        self.e.clear()
        self.result = None
        pool = ThreadPool(processes=1)
        
        # Find intervals for given frequency band
        frequencies = np.arange(minfreq, maxfreq, interval)
        
        async_result = pool.apply_async(self._TFR_topology, 
                                        (raw, epochs, reptype, mode, 
                                         frequencies, blstart, 
                                         blend, ncycles, decim))
        while(True):
            sleep(0.2)
            if self.e.is_set(): break;
            self.parent.update_ui()

        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            self.result = None
            return 
        
        power, itc = async_result.get()
        pool.terminate()
        self.parent.update_ui()
        layout = read_layout(lout)
        #layout = read_layout('Vectorview-all')
        baseline = (blstart, blend)  # set the baseline for induced power
        print "Plotting..."
        self.parent.update_ui()
        #mode = 'ratio'  # set mode for baseline rescaling
    
        if ( reptype == 'induced' ):
            pass #obsolete?
        elif reptype == 'phase':
            pass #obsolete?
        elif reptype == 'average':
            try:
                fig = power.plot_topomap(fmin=minfreq, fmax=maxfreq, 
                                         ch_type=ch_type, layout=layout,
                                         baseline=baseline, mode=mode,
                                         cmap='Reds', show=False)
                print 'Plotting topology. Please be patient...'
                self.parent.update_ui()
                fig = power.plot_topo(baseline=baseline, mode=mode, 
                                      fmin=minfreq, fmax=maxfreq,
                                      layout=layout,
                                      title='Average power', cmap='Reds')
                #fig.show()
            except Exception as e:
                self.messageBox = messageBoxes.shortMessageBox(str(e))
                self.messageBox.show()
                return
        elif reptype == 'itc':
            try:
                title = 'Inter-Trial coherence'
                fig = itc.plot_topomap(fmin=minfreq, fmax=maxfreq, 
                                         ch_type=ch_type, layout=layout,
                                         baseline=baseline, mode=mode,
                                         cmap='Reds', show=False)
                fig = itc.plot_topo(baseline=baseline, mode=mode, 
                                    fmin=minfreq, fmax=maxfreq, vmin=0.,
                                    vmax=1., layout=layout, 
                                    title=title, cmap='Reds')
                
                #fig = topo.plot_topo_phase_lock(epochs, phase_lock, 
                #                            frequencies, 
                #                            layout, baseline=baseline, 
                #                            mode=mode, decim=decim, 
                #                            title=title)
                fig.show()
            except Exception as e:
                self.messageBox = messageBoxes.shortMessageBox(str(e))
                self.messageBox.show()
                return
        """
        fig = self._TFR_topology(raw, epochs, reptype, mode, 
                                         frequencies, blstart, 
                                         blend, ncycles, decim)
        """    
        def onclick(event):
            pl.show(block=False)
        fig.canvas.mpl_connect('button_press_event', onclick)
             
        
    def _TFR_topology(self, raw, epochs, reptype, mode, frequencies, blstart, 
                      blend, ncycles, decim):
        """
        Performed in a worker thread.
        """
        
        # TODO: Let the user define the title of the figure.
        #data = epochs.get_data()
        
        # Find intervals for given frequency band
        #Fs = raw.info['sfreq']
        
        try:
            #http://martinos.org/mne/stable/auto_examples/time_frequency/plot_time_frequency_sensors.html?highlight=tfr_morlet
            power, itc = tfr_morlet(epochs, freqs=frequencies, n_cycles=ncycles, use_fft=False,
                        return_itc=True, decim=decim, n_jobs=3)
            
            """
            power, phase_lock = induced_power(data, Fs=Fs,
                                              frequencies=frequencies,
                                              n_cycles=ncycles, n_jobs=3,
                                              use_fft=False, decim=decim,
                                              zero_mean=True)"""
        except ValueError as err:
            self.result = err
            self.e.set()
            return
        except Exception as e:
            self.result = e
            self.e.set()
            return
        """
        layout = read_layout('Vectorview-all')
        baseline = (blstart, blend)  # set the baseline for induced power
        #mode = 'ratio'  # set mode for baseline rescaling
        if ( reptype == 'induced' ):
            title='TFR topology: ' + 'Induced power'
            try:
                power.plot_topo(baseline=baseline, mode=mode, title='Average power')
                fig = power.plot_topomap(fmin=frequencies[0], fmax=frequencies[-1], layout=layout,
                            baseline=baseline, mode=mode,
                            title=title)
            except Exception as e:
                self.result = e
                self.e.set()
                return
        else: 
            title = 'TFR topology: ' + 'Phase locking'
            try:
                fig = topo.plot_topo_phase_lock(epochs, phase_lock, 
                                            frequencies, 
                                            layout, baseline=baseline, 
                                            mode=mode, decim=decim, 
                                            title=title)
            except Exception as e:
                self.result = e
                self.e.set()
                return
        self.e.set()
        return fig
        """
        self.e.set()
        return power, itc
    
    
    def plot_power_spectrum(self, params, colors, channelColors):
        
        try:
            lout = mne.layouts.read_layout(params['lout'], 
                                           scale=True)
        except Exception:
            message = 'Could not read layout information.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        raw = self.experiment.active_subject.working_file
        #self.computeSpectrum(params)
        self.e.clear()
        self.result = None
        pool = ThreadPool(processes=1)
        
        async_result = pool.apply_async(self._compute_spectrum, 
                                        (raw, params,))
        while(True):
            sleep(0.2)
            if self.e.is_set(): break;
            self.parent.update_ui()

        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            self.result = None
            return 
        
        psds = async_result.get()
        pool.terminate()
        print "Plotting power spectrum..."
        print raw.info['projs']
        self.parent.update_ui()
        
        def my_callback(ax, ch_idx):
            """
            Callback for the interactive plot.
            Opens a channel specific plot.
            """
            for i in xrange(len(psds)):
                color = colors[i]
                ax.plot(psds[i][1], psds[i][0][ch_idx], color=color)
            plt.xlabel('Frequency (Hz)')
            if params['log']:
                plt.ylabel('Power (dB)')
            else:
                plt.ylabel('(uV)')
            plt.show()
           
        # draw topography
        for ax, idx in iter_topography(raw.info,
                            fig_facecolor='white', axis_spinecolor='white', 
                            axis_facecolor='white', layout=lout, 
                            on_pick=my_callback):
            for i in xrange(len(psds)):
                channel = raw.info['ch_names'][idx]
                if (channel in channelColors[i][1]):
                    ax.plot(psds[i][0][idx], 
                            color=channelColors[i][0], linewidth=0.2)
                else:
                    ax.plot(psds[i][0][idx], color=colors[i],
                            linewidth=0.2)
        plt.show()
    
    def _compute_spectrum(self, raw, params):
        """
        Performed in a worker thread.
        """
        times = params['times']
        fmin = params['fmin']
        fmax = params['fmax']
        nfft = params['nfft']
        try:
            if params['ch'] == 'meg':
                picks = mne.pick_types(raw.info, meg=True, eeg=False, 
                                       exclude=[])
            elif params['ch'] == 'eeg':
                picks = mne.pick_types(raw.info, meg=False, eeg=True, 
                                       exclude=[])
        except Exception as e:
            self.result = e
            self.e.set()
            return
        psdList = []    
        for time in times:
            try:
                psds, freqs = compute_raw_psd(raw, tmin=time[0], tmax=time[1], 
                              fmin=fmin, fmax=fmax, n_fft=nfft, 
                              picks=picks, proj=True, verbose=True)
            except Exception as e:
                self.result = e
                self.e.set()
                return
            if params['log']:
                psds = 10 * np.log10(psds)
            psdList.append((psds, freqs))
        self.e.set()
        return psdList
        """
        try:
            psds = self.computePowerSpectrum(params['times'], params['fmin'],
                                             params['fmax'], params['nfft'],
                                             params['log'])
        except Exception as e:
            self.result = e
            self.e.set()
            return
        print "Done"
        self.e.set()
        return psds
        """
            
    def magnitude_spectrum(self, raw, ch_index):
        """
        Replaced by plot_power_spectrum.
        CURRENTLY NOT IN USE!
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
       
                            
    def filter(self, dataToFilter, info, samplerate, dic):
        """
        Filters the data array in place according to parameters in paramDict.
        Depending on the parameters, the filter is one or more of
        lowpass, highpass and bandstop (notch) filter.
        
        Keyword arguments:
        
        dataToFilter         -- array of data to filter
        info                 -- info for the data file to filter
        samplerate           -- intended samplerate of the array
        dic                  -- Dictionary with filtering parameters
        
        Returns the filtered array.
        """
        self.e.clear()
        self.result = None
        pool = ThreadPool(processes=1)

        async_result = pool.apply_async(self._filter, 
                                        (dataToFilter, info, samplerate, dic,))
        while(True):
            sleep(0.2)
            if self.e.is_set(): break;
            self.parent.update_ui()

        if not self.result is None:
            self.messageBox = messageBoxes.shortMessageBox(str(self.result))
            self.messageBox.show()
            self.result = None
            return dataToFilter
        filteredData = async_result.get()
        pool.terminate()
        return filteredData
        
    def _filter(self, dataToFilter, info, samplerate, dic):
        """
        Performed in a working thread.
        """
        # Exclude non-data and bad channels from filtering with picks.
        picks = mne.pick_types(info, meg=True, eeg=True, stim=False, eog=False, 
        ecg=False, emg=False, ref_meg='auto', misc=False, resp=False, 
        chpi=False, exci=False, ias=False, syst=False, include=[], 
        exclude='bads', selection=None)
        
        # TODO: check if this holds for mne.filter
        # n_jobs is 2 because of the increasing memory requirements for 
        # multicore filtering, see 
        # http://martinos.org/mne/stable/generated/mne.io.RawFIFF.html#mne.io.RawFIFF.filter
        try:
            if dic.get('lowpass') == True:
                print "Low-pass filtering..."
                dataToFilter = mne.filter.low_pass_filter(dataToFilter, samplerate, 
                            dic.get('low_cutoff_freq'), dic.get('low_length'),
                            dic.get('low_trans_bandwidth'),'fft', None, picks=picks,
                            n_jobs=2, copy=True)
                
            if dic.get('highpass') == True:
                print "High-pass filtering..."
                dataToFilter = mne.filter.high_pass_filter(dataToFilter, samplerate, 
                            dic.get('high_cutoff_freq'), dic.get('high_length'),
                            dic.get('high_trans_bandwidth'),'fft', None, 
                            picks=picks, n_jobs=3, copy=True)
            
            if dic.get('bandstop1') == True:
                print "Band-stop filtering..."
                dataToFilter = mne.filter.band_stop_filter(dataToFilter, samplerate,
                            dic.get('bandstop1_l_freq'), 
                            dic.get('bandstop1_h_freq'), 
                            dic.get('bandstop1_length'), 
                            dic.get('bandstop1_trans_bandwidth'),
                            dic.get('bandstop1_trans_bandwidth'),picks=picks,
                            n_jobs=2, copy=True)
                
            if dic.get('bandstop2') == True:
                print "Band-stop filtering..."
                dataToFilter = mne.filter.band_stop_filter(dataToFilter, samplerate,
                            dic.get('bandstop2_l_freq'), 
                            dic.get('bandstop2_h_freq'), 
                            dic.get('bandstop2_length'), 
                            dic.get('bandstop2_trans_bandwidth'),
                            dic.get('bandstop2_trans_bandwidth'), picks=picks,
                            n_jobs=2, copy=True)
        except Exception as e:
            self.result = e
            self.e.set()
            return dataToFilter
        print "Done"
        self.e.set()
        return dataToFilter
    
### Methods needed for source modeling ###    

    def convert_mri_to_mne(self):
        """
        Uses mne_setup_mri to active subject recon directory to create Neuromag
        slices and sets (to be input later to do_forward_solution).
        
        Return True if creation successful, False if there was an error. 
        """
        
        sourceAnalDir = self.experiment.active_subject.\
                            _source_analysis_directory
        
        
        # Hack the SUBJECT_DIR and SUBJECT variables to right location 
        # (mne_setup_mri searches for reconstructed files from mri directory
        # under the SUBJECT)
        os.environ['SUBJECTS_DIR'] = sourceAnalDir
        os.environ['SUBJECT'] = 'reconFiles'
        
        try:
            subprocess.check_output("$MNE_ROOT/bin/mne_setup_mri", shell=True)
            return True
        except CalledProcessError as e:
            message = 'mne_setup_mri output: \n' \
            + str(e.output)
            title = 'Problem setting mri images'
            self.messagebox = messageBoxes.longMessageBox(title, message)
            self.messagebox.show()
            return False
        
        
    def create_forward_model(self, fmdict):
        """
        Creates a single forward model and saves it to an appropriate directory.
        The steps taken are the following:
         
        - Run mne_setup_source_space to handle various steps of source space
        creation
        - Use mne_watershed_bem to create bem model meshes
        - Create BEM model with mne_setup_forward_model
        - Copy the bem files to the directory named according to fmname
        
        Keyword arguments:
        
        fmdict        -- dictionary, including in three dictionaries, the
                         parameters for three separate mne scripts run
                         in the forward model creation.
        """
        activeSubject = self.experiment._active_subject
    
        # Set env variables to point to appropriate directories. 
        os.environ['SUBJECTS_DIR'] = activeSubject._source_analysis_directory
        os.environ['SUBJECT'] = 'reconFiles'
        
        # The scripts call scripts themselves and need environ for path etc.
        env = os.environ
        
        # Some test files for whether setup_source_space has and watershed
        # have already been run. MNE scripts delete these if something fails,
        # so it should be save to base tests on these.
        bemDir = os.path.join(activeSubject._reconFiles_directory, 'bem/')
        fmDir = activeSubject._forwardModels_directory
                
        # Should have the source space description file.
        sourceSpaceSetupTestList = glob.glob(bemDir + '*src.fif') 
        
        waterShedDir = os.path.join(bemDir, 'watershed/')
        waterShedSurfaceTestFile = os.path.join(waterShedDir, 
                                                'reconFiles_brain_surface')
        wsCorTestFile = os.path.join(waterShedDir, 'ws/', 'COR-.info')
        
        fmname = fmdict['fmname']
        (setupSourceSpaceArgs, waterShedArgs, setupFModelArgs)  = \
        fileManager.convertFModelParamDictToCmdlineParamTuple(fmdict)
        
        # Check if source space is already setup and watershed calculated, and
        # offer to skip them and only perform setup_forward_model.
        reply = 'computeAll'
        if len(sourceSpaceSetupTestList) > 0 and \
        os.path.exists(waterShedSurfaceTestFile) and \
        os.path.exists(wsCorTestFile):
        
            try: 
                sSpaceDict = fileManager.unpickle(os.path.join(fmDir, 
                                                  'setupSourceSpace.param'))
            except Exception:
                sSpaceDict = dict()
                
            try:
                wshedDict = fileManager.unpickle(os.path.join(fmDir, 
                                                              'wshed.param'))
            except Exception:
                wshedDict = dict()
        
            fModelSkipDialog = ForwardModelSkipDialog(self, sSpaceDict,
                                                      wshedDict)
            
            fModelSkipDialog.exec_()
            reply = fModelSkipDialog.get_return_value()
            
        
        if reply == 'cancel':
            # To keep forward model dialog open
            return False
        
        if reply == 'bemOnly':
            # Need to do this to get triangulation files to right place and
            # naming for mne_setup_forward_model.
            fileManager.link_triang_files(activeSubject)
            self._call_mne_setup_forward_model(setupFModelArgs, env)
        
            try:
                fileManager.create_fModel_directory(fmname, activeSubject)          
                fileManager.write_forward_model_parameters(fmname,
                    activeSubject, None, None, fmdict['sfmodelArgs'])
                
                # These should always exist, should be safe to unpickle.
                sspaceParamFile = os.path.join(fmDir, 'setupSourceSpace.param')
                wshedParamFile = os.path.join(fmDir, 'wshed.param')
                sspaceArgsDict = fileManager.unpickle(sspaceParamFile)
                wshedArgsDict = fileManager.unpickle(wshedParamFile)
                     
                mergedDict = dict([('fmname', fmname)] + \
                                  sspaceArgsDict.items() + \
                                  wshedArgsDict.items() + \
                                  fmdict['sfmodelArgs'].items() + \
                                  [('coregistered', 'no')] + \
                                  [('fsolution', 'no')])
                
                fmlist = self.parent.forwardModelModel.\
                         fmodel_dict_to_list(mergedDict)
                self.parent.forwardModelModel.add_fmodel(fmlist)
            except Exception:
                tb = traceback.format_exc()
                message = 'There was a problem creating forward model files. ' + \
                      'Please copy the following to your bug report:\n\n' + \
                      str(tb)
                self.messageBox = messageBoxes.longMessageBox('Error', message)
                self.messageBox.show()
        
        if reply == 'computeAll':
            # To make overwriting unnecessary
            if os.path.isdir(bemDir):
                shutil.rmtree(bemDir)
            self._call_mne_setup_source_space(setupSourceSpaceArgs, env)
            self._call_mne_watershed_bem(waterShedArgs, env)
            
            # Right name and place for triang files, see above.
            fileManager.link_triang_files(activeSubject)
            self._call_mne_setup_forward_model(setupFModelArgs, env)    
        
            try:
                fileManager.create_fModel_directory(fmname, activeSubject)          
                fileManager.write_forward_model_parameters(fmname, activeSubject,
                    fmdict['sspaceArgs'], fmdict['wsshedArgs'],
                    fmdict['sfmodelArgs'])
                mergedDict = dict([('fmname', fmname)] + \
                                  fmdict['sspaceArgs'].items() + \
                                  fmdict['wsshedArgs'].items() + \
                                  fmdict['sfmodelArgs'].items() + \
                                  [('coregistered', 'no')] + \
                                  [('fsolution', 'no')])
                
                fmlist = self.parent.forwardModelModel.\
                         fmodel_dict_to_list(mergedDict)
                self.parent.forwardModelModel.add_fmodel(fmlist)             
            except Exception:
                tb = traceback.format_exc()
                message = 'There was a problem creating forward model files. ' + \
                      'Please copy the following to your bug report:\n\n' + \
                       str(tb)
                self.messageBox = messageBoxes.longMessageBox('Error', message)
                self.messageBox.show()
            
    
    def _call_mne_setup_source_space(self, setupSourceSpaceArgs, env):
        try:
            # TODO: this actually has an MNE-Python counterpart, which doesn't
            # help much, as the others don't (11.10.2014).
            mne_setup_source_space_commandList = \
            ['$MNE_ROOT/bin/mne_setup_source_space'] + \
            setupSourceSpaceArgs
            mne_setup_source_spaceCommand = ' '.join(
                                            mne_setup_source_space_commandList)
            setupSSproc = subprocess.check_output(mne_setup_source_spaceCommand,
                                    shell=True, env=env)
            self.parent.processes.append(setupSSproc)
        except CalledProcessError as e:
            title = 'Problem with forward model creation'
            message= 'There was a problem with mne_setup_source_space. ' + \
                     'Script output: \n' + e.output
            self.messageBox = messageBoxes.longMessageBox(title, message)
            self.messageBox.exec_()
            return
        except Exception as e:
            message = 'There was a problem with mne_setup_source_space: ' + \
                      str(e) + \
                      ' (Are you sure you have your MNE_ROOT set right ' + \
                      'in Meggie preferences?)'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return
        
        
    def _call_mne_watershed_bem(self, waterShedArgs, env):
        try:
            mne_watershed_bem_commandList = ['$MNE_ROOT/bin/mne_watershed_bem'] + \
                                    waterShedArgs
            mne_watershed_bemCommand = ' '.join(mne_watershed_bem_commandList)
            wsProc = subprocess.check_output(mne_watershed_bemCommand,
                                    shell=True, env=env)
            self.parent.processes.append(wsProc)
        except CalledProcessError as e:
            title = 'Problem with forward model creation'
            message= 'There was a problem with mne_watershed_bem. ' + \
                     'Script output: \n' + e.output
            self.messageBox = messageBoxes.longMessageBox(title, message)
            self.messageBox.exec_()
            return
        except Exception as e:
            message = 'There was a problem with mne_watershed_bem: ' + \
                      str(e) + \
                      ' (Are you sure you have your MNE_ROOT set right ' + \
                      'in Meggie preferences?)'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return
        
        
    def _call_mne_setup_forward_model(self, setupFModelArgs, env):
        try:
            mne_setup_forward_modelCommandList = \
                ['$MNE_ROOT/bin/mne_setup_forward_model'] + setupFModelArgs
            mne_setup_forward_modelCommand = ' '.join(
                                        mne_setup_forward_modelCommandList)
            setupFModelProc = subprocess.check_output(mne_setup_forward_modelCommand, shell=True,
                                    env=env)
            self.parent.processes.append(setupFModelProc)
        except CalledProcessError as e:    
            title = 'Problem with forward model creation'
            message= 'There was a problem with mne_setup_forward_model. ' + \
                     'Script output: \n' + e.output
            self.messageBox = messageBoxes.longMessageBox(title, message)
            self.messageBox.exec_()
            return
        except Exception as e:
            message = 'There was a problem with mne_setup_forward_model: ' + \
                      str(e) + \
                      ' (Are you sure you have your MNE_ROOT set right ' + \
                      'in Meggie preferences?)'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return


    def coregister_with_mne_gui_coregistration(self):
        """
        Uses mne.gui.coregistration for head coordinate coregistration.
        """
        
        activeSubject = self.parent._experiment._active_subject
        tableView = self.parent.ui.tableViewFModelsForCoregistration
        
        # Selection for the view is SingleSelection / SelectRows, so this
        # should return indexes for single row.
        selectedRowIndexes = tableView.selectedIndexes()
        selectedFmodelName = selectedRowIndexes[0].data() 
                             
        subjects_dir = os.path.join(activeSubject._forwardModels_directory,
                               selectedFmodelName)
        subject = 'reconFiles'
        rawPath = os.path.join(activeSubject.subject_path, 
                  self.experiment._working_file_names[self.parent.\
                  experiment._active_subject_name])
        
        mne.gui.coregistration(tabbed=True, split=True, scene_width=300, 
                               raw=rawPath, subject=subject,
                               subjects_dir=subjects_dir)
        QtCore.QCoreApplication.processEvents()
        
        # Needed for copying the resulting trans file to the right location.
        self.coregHowtoDialog = holdCoregistrationDialog(self, activeSubject,
                                                         selectedFmodelName) 
        self.coregHowtoDialog.ui.labelTransFileWarning.hide()   
        self.coregHowtoDialog.show()
        

    def create_forward_solution(self, fsdict):
        """
        Creates a forward solution based on parameters given in fsdict.
        
        Keyword arguments:
        
        fsdict    -- dictionary of parameters for forward solution creation.
        """
        
        activeSubject = self.parent._experiment._active_subject 
        rawInfo = activeSubject._working_file.info
        
        tableView = self.parent.ui.tableViewFModelsForSolution
        selectedRowIndexes = tableView.selectedIndexes()
        selectedFmodelName = selectedRowIndexes[0].data()
        
        fmdir = os.path.join(activeSubject._forwardModels_directory,
                               selectedFmodelName) 
        transFilePath = os.path.join(fmdir, 'reconFiles',
                                     'reconFiles-trans.fif')
        
        srcFileDir = os.path.join(fmdir, 'reconFiles', 'bem')
        srcFilePath = None
        for f in os.listdir(srcFileDir):
            if fnmatch.fnmatch(f, 'reconFiles*src.fif'):
                srcFilePath = os.path.join(srcFileDir, f)
        
        bemSolFilePath = None
        for f in os.listdir(srcFileDir):
            if fnmatch.fnmatch(f, 'reconFiles*bem-sol.fif'):
                bemSolFilePath = os.path.join(srcFileDir, f)
        
        targetFileName = os.path.join(fmdir, 'reconFiles', 'reconFiles-fwd.fif')
    
        try:
            mne.make_forward_solution(rawInfo, transFilePath, srcFilePath, 
                                  bemSolFilePath, targetFileName,
                                  fsdict['includeMEG'], fsdict['includeEEG'],
                                  fsdict['mindist'], fsdict ['ignoreref'], True,
                                  fsdict['njobs'])
            fileManager.write_forward_solution_parameters(fmdir, fsdict)
            self.parent.forwardModelModel.initialize_model()
        except Exception as e:
            title = 'Error'
            message = 'There was a problem with forward solution. The ' + \
            'MNE-Python message was: \n\n' + str(e)
            self.messageBox = messageBoxes.longMessageBox(title, message)
            self.messageBox.show()
        

    def create_covariance_from_raw(self, cvdict):
        """
        Computes a covariance matrix based on raw file and saves it to the 
        approriate location under the subject.
        
        Keyword arguments:
        
        cvdict        -- dictionary containing parameters for covariance
                         computation
        """
        subjectName = cvdict['rawsubjectname']
        fileNameToWrite = ''
        try:
            if subjectName != None:
                if subjectName == self.experiment.active_subject_name:
                    fileNameToWrite = subjectName + '-cov.fif'
                    raw = self.experiment.active_subject.working_file
                else:
                    fileNameToWrite = subjectName + '-cov.fif'
                    raw = self.experiment.get_subject_working_file(
                                                        subjectName) 
            else:
                raw = fileManager.open_raw(cvdict['rawfilepath'], True)
                basename = os.path.basename(cvdict['rawfilepath'])
                fileNameToWrite = os.path.splitext(basename)[0] + '-cov.fif'
        except Exception:
            raise
        
        tmin = cvdict['starttime']
        tmax = cvdict['endtime']
        tstep = cvdict['tstep']
        
        reject = cvdict['reject']
        flat = cvdict['flat']
        picks = cvdict['picks']
        
        try:
            cov = mne.compute_raw_data_covariance(raw, tmin, tmax, tstep,
                  reject, flat, picks)
        except ValueError:
            raise
        
        sourceAnalysisDir = self.experiment.active_subject. \
                            _source_analysis_directory
        
        # Remove previous covariance file before creating a new one.
        fileManager.remove_files_with_regex(sourceAnalysisDir,'.*-cov.fif')
        
        filePathToWrite = os.path.join(sourceAnalysisDir, fileNameToWrite)
        try:
            mne.write_cov(filePathToWrite, cov)
        except IOError as err:
            err.message = 'Could not write covariance file. ' + \
            'The error message was: \n\n' + err.message 
            raise
        
        # Delete previous and write a new parameter file.
        try:
            fileManager.remove_files_with_regex(sourceAnalysisDir,
                                                'covariance.param')
            cvparamFile = os.path.join(sourceAnalysisDir, 'covariance.param')
            fileManager.pickleObjectToFile(cvdict,cvparamFile)
            
        except Exception:
            fileManager.remove_files_with_regex(sourceAnalysisDir,
                                                '*-cov.fif')
            raise
        
        # Update ui.
        self.parent.update_covariance_info_box()


    def update_experiment_working_file(self, fname, raw):
        """
        Changes the current working file for the experiment the caller relates
        to.
        fname    -- name of the new working file
        raw      -- working file data
        """
        self.experiment.update_working_file(fname)
        self.experiment.active_subject_raw_path = fname
        self.experiment.active_subject.working_file = raw
        status = "Current working file: " + \
        os.path.basename(self.experiment.active_subject_raw_path)
        self.parent.statusLabel.setText(status)