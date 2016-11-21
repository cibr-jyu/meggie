# coding: utf-8
"""
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen
This module contains caller class which calls third party software.
"""

import subprocess
import os
import glob
import fnmatch
import re
import shutil
import copy
import math
from functools import partial
from collections import OrderedDict

from PyQt4 import QtCore, QtGui

import mne
from mne import make_fixed_length_events, compute_proj_evoked
from mne.channels.layout import read_layout
from mne.channels.layout import _pair_grad_sensors_from_ch_names
from mne.channels.layout import _merge_grad_data
from mne.viz import plot_evoked_topo
from mne.viz import iter_topography
from mne.utils import _clean_names
from mne.time_frequency.tfr import tfr_morlet
from mne.time_frequency import psd_welch
from mne.preprocessing import compute_proj_ecg, compute_proj_eog, find_eog_events

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

from os.path import isfile, join
from subprocess import CalledProcessError
from copy import deepcopy

from meggie.ui.sourceModeling.holdCoregistrationDialogMain import holdCoregistrationDialog
from meggie.ui.sourceModeling.forwardModelSkipDialogMain import ForwardModelSkipDialog
from meggie.ui.utils.decorators import threaded

from meggie.code_meggie.general.wrapper import wrap_mne_call
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.epoching.events import Events
from meggie.code_meggie.general.measurementInfo import MeasurementInfo
from meggie.code_meggie.general.singleton import Singleton
from astropy.units import Tmin


@Singleton
class Caller(object):
    """
    Class for calling third party software. Includes methods that
    require input from single source (usually a dialog) and produce simple
    output (usually a single matplotlib window). 
    More complicated functionality like epoching can be found in separate
    classes.
    """
    parent = None
    _experiment = None

    def setParent(self, parent):
        """
        Keyword arguments:
        parent        -- Parent of this object. Reference is stored for
                         updating the ui and keeping it responsive.
        """
        self.parent = parent
        
    @property
    def experiment(self):
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment

    @threaded
    def activate_subject(self, name):
        """
        Activates the subject.
        Keyword arguments:
        name      -- Name of the subject to activate.
        """
        if name == '':
            return

        self.experiment.activate_subject(name)
    
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
                                filename, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()
        print "the program return code was %d" % retval

    @threaded
    def call_maxfilter(self, params, custom):
        """
        Performs maxfiltering with the given parameters.
        Keyword arguments:
        raw    -- Raw object.
        params -- Dictionary of parameters
        custom -- Additional parameters as a string
        """
        self._call_maxfilter(params, custom)

    def _call_maxfilter(self, params, custom):
        """Aux function for maxfiltering data. """
        if os.environ.get('NEUROMAG_ROOT') is None:
            os.environ['NEUROMAG_ROOT'] = '/neuro'
        bs = '$NEUROMAG_ROOT/bin/util/maxfilter '
        for i in range(len(params)):
            bs += params.keys()[i] + ' ' + str(params.values()[i]) + ' '
        # Add user defined parameters from the "custom" tab
        bs += custom
        print bs
        proc = subprocess.Popen(bs, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        while True:
            line = proc.stdout.readline()
            if not line: 
                break
            print line
        retval = proc.wait()      

        print "the program return code was %d" % retval
        if retval != 0:
            print 'Error while maxfiltering data!'
            raise RuntimeError('Error while maxfiltering the data. '
                               'Check console.')

        outputfile = params.get('-o')
        # TODO: log mne call
        #self.experiment.action_logger.log_mne_func_call_decorated(wrap_mne_call(self.experiment, mne.io.Raw, outputfile, preload=True))
        raw = mne.io.Raw(outputfile, preload=True)

        self.experiment.active_subject.set_working_file(raw)

        self.experiment.save_experiment_settings()

    def call_ecg_ssp(self, dic, subject):
        """
        Creates ECG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        subject       -- The subject to perform the action on.
        """
        self._call_ecg_ssp(dic, subject, do_meanwhile=self.parent.update_ui)

    @threaded
    def _call_ecg_ssp(self, dic, subject):
        """Performed in a worker thread."""
        raw_in = subject.get_working_file()
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
        if bads is None or bads == ['']:
            bads = []

        start = dic.get('tstart')
        taps = dic.get('filtersize')
        eeg_proj = dic.get('avg-ref')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        preload = True  # TODO File
        ch_name = dic.get('ch_name')

        prefix = os.path.join(subject.subject_path, subject.subject_name)

        ecg_event_fname = prefix + '_ecg-eve.fif'

        if comp_ssp:
            ecg_proj_fname = prefix + '_ecg_avg_proj.fif'
        else:
            ecg_proj_fname = prefix + '_ecg_proj.fif'

        n_jobs = self.parent.preferencesHandler.n_jobs
        projs, events = wrap_mne_call(self.experiment, 
                                      compute_proj_ecg, 
                                      raw_in, None, tmin, tmax, grad,
                                      mag, eeg, filter_low, filter_high,
                                      comp_ssp, taps, n_jobs, ch_name,
                                      reject, flat, bads, eeg_proj,
                                      excl_ssp, event_id, ecg_low_freq,
                                      ecg_high_freq, start,
                                      qrs_threshold)

        if len(events) == 0:
            raise Exception('No ECG events found. Change settings.')

        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)

        print "Writing ECG projections in %s" % ecg_proj_fname
        wrap_mne_call(self.experiment, mne.write_proj, ecg_proj_fname, projs)

        print "Writing ECG events in %s" % ecg_event_fname
        wrap_mne_call(self.experiment, mne.write_events, ecg_event_fname, events)

    def call_eog_ssp(self, dic, subject):
        """
        Creates EOG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        subject       -- The subject to perform action on.
        """
        self._call_eog_ssp(dic, subject, do_meanwhile=self.parent.update_ui)

    @threaded
    def _call_eog_ssp(self, dic, subject):
        """Performed in a worker thread."""
        raw_in = subject.get_working_file()
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
        if bads is None or bads == ['']:
            bads = []
        start = dic.get('tstart')
        taps = dic.get('filtersize')
        eeg_proj = dic.get('avg-ref')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        preload = True  # TODO File
        reject = dict(grad=1e-13 * float(rej_grad), mag=1e-15 * float(rej_mag),
                      eeg=1e-6 * float(rej_eeg), eog=1e-6 * float(rej_eog))

        prefix = os.path.join(subject.subject_path, subject.subject_name) 
        eog_event_fname = prefix + '_eog-eve.fif'

        if comp_ssp:
            eog_proj_fname = prefix + '_eog_avg_proj.fif'
        else:
            eog_proj_fname = prefix + '_eog_proj.fif'

        n_jobs = self.parent.preferencesHandler.n_jobs
        projs, events = wrap_mne_call(self.experiment, compute_proj_eog,
                                      raw_in, None, tmin, tmax, grad,
                                      mag, eeg, filter_low, filter_high,
                                      comp_ssp, taps, n_jobs, reject,
                                      flat, bads, eeg_proj, excl_ssp,
                                      event_id, eog_low_freq,
                                      eog_high_freq, start)


        # TODO Reading a file
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)

        print "Writing EOG projections in %s" % eog_proj_fname
        wrap_mne_call(self.experiment, mne.write_proj, eog_proj_fname, projs)

        print "Writing EOG events in %s" % eog_event_fname
        wrap_mne_call(self.experiment, mne.write_events, eog_event_fname, events)

    def call_eeg_ssp(self, dic, subject):
        """
        Creates EEG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        subject       -- The subject to perform action on.
        """
        self._call_eeg_ssp(dic, subject, do_meanwhile=self.parent.update_ui)
        
    @threaded
    def _call_eeg_ssp(self, dic, subject):
        raw = subject.get_working_file()
        events = dic['events']
        tmin = dic['tmin']
        tmax = dic['tmax']
        n_eeg = dic['n_eeg']
        #eog_epochs = mne.Epochs(raw, events, event_id=event_id,
        #                tmin=tmin, tmax=tmax)
        #events = np.array(events)
        
        eog_epochs = wrap_mne_call(self.experiment, mne.epochs.Epochs,
            raw, events, tmin=tmin, tmax=tmax)
        
        
        # Average EOG epochs
        eog_evoked = eog_epochs.average()
        
        # Compute SSPs
        projs = wrap_mne_call(self.experiment, compute_proj_evoked, eog_evoked, n_eeg=n_eeg)

        prefix = os.path.join(subject.subject_path, subject.subject_name) 
        eeg_event_fname = prefix + '_eeg-eve.fif'
        eeg_proj_fname = prefix + '_eeg_proj.fif'
        
        print "Writing EOG projections in %s" % eeg_proj_fname
        wrap_mne_call(self.experiment, mne.write_proj, eeg_proj_fname, projs)

        print "Writing EOG events in %s" % eeg_event_fname
        wrap_mne_call(self.experiment, mne.write_events, eeg_event_fname, events)
        #TODO: self.raw.add_proj(proj) in apply_exg method

    def apply_exg(self, kind, raw, directory, projs, applied):
        """
        Applies ECG or EOG projections for MEG-data.  
        Keyword arguments:
        kind          -- String to indicate type of projectors ('eog, or 'ecg')
        raw           -- Data to apply to
        directory     -- Directory of the projection file
        projs         -- List of projectors.
        applied       -- Boolean mask (list) of projectors to add to raw.
                         Trues are added to the object and Falses are not
        """

        if len(applied) != len(projs):
            raise Exception('Error while adding projectors. Check selection.')

        self._apply_exg(kind, raw, directory, projs, applied,
                        do_meanwhile=self.parent.update_ui)
        self.experiment.save_experiment_settings()
        return True

    @threaded
    def _apply_exg(self, kind, raw, directory, projs, applied):
        """Performed in a worker thread."""
        fname = os.path.join(directory, self.experiment.active_subject.working_file_name)
        if kind == 'ecg':
            if '-ecg_applied' not in fname:
                fname = fname.split('.')[0] + '-ecg_applied.fif'
        if kind == 'eog':
            if '-eog_applied' not in fname:
                fname = fname.split('.')[0] + '-eog_applied.fif'
        if kind == 'eeg':
            if '-eeg_applied' not in fname:
                fname = fname.split('.')[0] + '-eeg_applied.fif'

        for new_proj in projs:  # first remove projs
            for idx, proj in enumerate(raw.info['projs']):
                if str(new_proj) == str(proj):
                    raw.info['projs'].pop(idx)
                    break

        if not isinstance(projs, np.ndarray):
            projs = np.array(projs)
        if not isinstance(applied, np.ndarray):
            applied = np.array(applied)

        wrap_mne_call(self.experiment, raw.add_proj, projs[applied])  # then add selected
        
        if kind == 'eeg':
            projs = raw.info['projs']
            for idx, proj in enumerate(projs):
                names = ['ECG', 'EOG', 'EEG']
                if filter(lambda x: x in proj['desc'], names):
                    continue
                #if 'ECG' in proj['desc']:
                #    continue
                #if 'EOG' in proj['desc']:
                #    continue
                #if 'EEG' in proj['desc']:
                #    continue
                raw.info['projs'][idx]['desc'] = 'Ocular-' + proj['desc'] 
        
        #Removes older raw files with applied projs
        directory = os.path.dirname(fname)
        files = glob.glob(directory + '/*e*g_applied.fif')
    
        for f in files:
            if f == fname:
                continue
            fileManager.delete_file_at(directory, f)
            print 'Removed previous working file: ' + f
        
        fileManager.save_raw(self.experiment, raw, fname, overwrite=True)

    def plot_average_epochs(self, events, tmin, tmax):
        """
        Method for plotting average epochs.
        """
        raw = self.experiment.active_subject.get_working_file()
        print "Plotting averages...\n"
        eog_epochs = mne.Epochs(raw, events,
                        tmin=tmin, tmax=tmax)
        
        # Average EOG epochs
        eog_evoked = eog_epochs.average()
        eog_evoked.plot()
        print "Finished\n"

    def plot_events(self, events):
        """
        Method for plotting the event locations in mne_browse_raw.
        Parameters:
        events - A list of events
        """
        raw = self.experiment.active_subject.get_working_file()
        print "Plotting events...\n"
        raw.plot(events=events, scalings=dict(eeg=40e-6))
        plt.show()
        print "Finished"


    def plot_projs_topomap(self, raw):
        wrap_mne_call(self.experiment, raw.plot_projs_topomap)

    @threaded
    def find_eog_events(self, params):
        raw = self.experiment.active_subject.get_working_file()
        eog_events = wrap_mne_call(self.experiment, find_eog_events, raw,
                        l_freq=params['l_freq'], h_freq=params['h_freq'],
                        filter_length=params['filter_length'],
                        ch_name=params['ch_name'], verbose=True,
                        tstart=params['tstart'])
        return eog_events

    def create_epochs(self, params, subject):
        """ Epochs are created in a way that one collection consists of such 
        things that belong together. We wanted multiple collections because 
        MNE Epochs don't allow multiple id's for one event name, so doing 
        subselections for averaging and visualizing purposes from one collection
        is not feasible.
        """
        params_copy = copy.deepcopy(params)
        reject_data = params_copy['reject']
        
        if 'grad' in reject_data:
            reject_data['grad'] *= 1e-13
        if 'mag' in reject_data:
            reject_data['mag'] *= 1e-15
        if 'eeg' in reject_data:
            reject_data['eeg'] *= 1e-6
        if 'eog' in reject_data:
            reject_data['eog'] *= 1e-6
        
        raw = subject.get_working_file()
             
        events = []
        event_params = params_copy['events']
        fixed_length_event_params = params_copy['fixed_length_events']
       
        category = {}

        # event_id should not matter after epochs are created.
        # counter is used so that no collisions would happen.
        event_id_counter = 0

        if len(event_params) > 0:
            for event_params_dic in event_params:
                event_id = event_params_dic['event_id']
                
                category_id = 'id_' + str(event_id)
                if event_params_dic['mask']:
                    category_id += '_mask_' + str(event_params_dic['mask'])
                
                category[category_id] = event_id_counter
                new_events = np.array(self.create_eventlist(event_params_dic,
                                                            subject))
                if len(new_events) == 0:
                    raise ValueError('No events found with selected id.')
                
                new_events[:, 2] = event_id_counter
                events.extend([event for event in new_events])
                event_id_counter += 1
                

        if len(fixed_length_event_params) > 0:
            for idx, event_params_dic in enumerate(fixed_length_event_params):
                category['fixed_' + str(idx + 1)] = event_id_counter
                event_params_dic['event_id'] = event_id_counter
                events.extend(make_fixed_length_events(raw, 
                    event_params_dic['event_id'],
                    event_params_dic['tmin'],
                    event_params_dic['tmax'], 
                    event_params_dic['interval']
                ))
                event_id_counter += 1

        if len(events) == 0:
            raise ValueError('Could not create epochs for subject: No events found with given params.')

        if not isinstance(raw, mne.io.Raw):
            raise TypeError('Not a Raw object')

        if params_copy['mag'] and params_copy['grad']:
            params_copy['meg'] = True
        elif params_copy['mag']:
            params_copy['meg'] = 'mag'
        elif params_copy['grad']:
            params_copy['meg'] = 'grad'
        else:
            params_copy['meg'] = False
        
        # find all proper picks
        picks = mne.pick_types(raw.info, meg=params_copy['meg'],
            eeg=params_copy['eeg'], eog=params_copy['eog'])
        
        if len(picks) == 0:
            raise ValueError('Picks cannot be empty. Select picks by ' + 
                             'checking the checkboxes.')

        epochs = wrap_mne_call(self.experiment, mne.epochs.Epochs,
            raw, np.array(events), category, params_copy['tmin'], params_copy['tmax'], 
            picks=picks, reject=params_copy['reject'])
            
        if len(epochs.get_data()) == 0:
            raise ValueError('Could not find any data. Perhaps the ' + 
                             'rejection thresholds are too strict...')
        
        epochs_object = Epochs(params['collection_name'], subject, params, epochs)
        fileManager.save_epoch(epochs_object, overwrite=True)
        subject.add_epochs(epochs_object)
        
        #event info for batch
        events = epochs.event_id
        events_str = ''
        for event_name, event_id in events.items():
            events_str += event_name + ' [' + str(len(epochs[event_name])) + ' events found]\n'
        
        return subject.subject_name + ', ' + params['collection_name'] + ':\n' + events_str

    def create_eventlist(self, params, subject):
        """
        Pick desired events from the raw data.
        """
        stim_channel = subject.find_stim_channel()
        raw = subject.get_working_file()
        e = Events(raw, stim_channel, params['mask'], params['event_id'])
        return e.events

    def read_layout(self, layout):
        if not layout or layout == "Infer from data":
            return None
        
        import pkg_resources
        path_mne = pkg_resources.resource_filename('mne', 'channels/data/layouts')
        path_meggie = pkg_resources.resource_filename('meggie', 'data/layouts')
        
        if os.path.exists(os.path.join(path_mne, layout)):
            return read_layout(layout, path_mne)
        
        if os.path.exists(os.path.join(path_meggie, layout)):
            return read_layout(layout, path_meggie)


    def draw_evoked_potentials(self, evokeds):
        """
        Draws a topography representation of the evoked potentials.

        Keyword arguments:
        evokeds  - Evoked object or list of evokeds.
        layout   - The desired layout as a string.
        """
        layout = self.read_layout(self.experiment.active_subject.layout)
        colors = self.colors(len(evokeds))
        title = self.experiment.active_subject.subject_name
            
        fig = wrap_mne_call(self.experiment, plot_evoked_topo, evokeds, layout,
                            color=colors, title=title)

        conditions = [e.comment for e in evokeds]
        positions = np.arange(0.025, 0.025 + 0.04 * len(evokeds), 0.04)
        
        for cond, col, pos in zip(conditions, colors, positions):
            plt.figtext(0.775, pos, cond, color=col, fontsize=12)

        fig.show()
        
        # TODO: log info about the clicked channels
        def onclick(event):
            plt.show(block=False)

        fig.canvas.mpl_connect('button_press_event', onclick)

    def average_channels(self, instance, lobeName, channelSet=[]):
        """
        Shows the averages for averaged channels in lobeName, or channelSet
        if it is provided.

        Keyword arguments:
        epochs     -- epochs to average, evoked object or list of
                        evoked objects.
        lobename     -- the lobe over which to average.
        channelSet   -- manually input list of channels. 
        """
        
        if channelSet:
            channels = channelSet
            title = 'selected set of channels.'
        else:
            channels = wrap_mne_call(
                self.experiment, mne.selection.read_selection, lobeName)
            title = lobeName
            
        print "Calculating channel averages for " + title

        dataList = self._average_channels(
            instance, channels, do_meanwhile=self.parent.update_ui)

        # Plotting:
        plt.clf()
        fig = plt.figure()
        mi = MeasurementInfo(self.experiment.active_subject.get_working_file())
        fig.canvas.set_window_title(mi.subject_name + 
             '-- channel average for ' + title)
        fig.suptitle('Channel average for ' + title, y=1.0025)

        # Draw a separate plot for each event type
        for index, (times, eventName, data) in enumerate(dataList):
            ca = fig.add_subplot(len(dataList), 1, index + 1) 
            ca.set_title(eventName)
            # Times information is the same as in original evokeds
            if eventName.endswith('grad'):
                label = ('fT/cm')
                data *= 1e13
            elif eventName.endswith('mag'):
                label = ('fT')
                data *= 1e15
            elif eventName.endswith('eeg'):
                label = ('uV')
                data *= 1e6

            ca.plot(times, data)
            ca.set_xlabel('Time (s)')
            ca.set_ylabel(label)
        plt.tight_layout()
        fig.show()

    @threaded
    def _average_channels(self, instance, channelsToAve):
        """Performed in a worker thread."""
        if isinstance(instance, str):  # epoch name
            epochs = self.experiment.active_subject.epochs.get(instance).raw
            if epochs is None:
                raise Exception('No epochs found.')

            category = epochs.event_id

            # Creates evoked potentials from the given events (variable 'name' 
            # refers to different categories).
            evokeds = [epochs[name].average() for name in category.keys()]
        elif isinstance(instance, mne.Evoked):
            evokeds = [instance]
        elif isinstance(instance, list) or isinstance(instance, np.ndarray):
            evokeds = instance
        
        # Channel names in Evoked objects may or may not have whitespaces
        # depending on the measurements settings,
        # need to check and adjust channelsToAve accordingly.
        
        channelNameString = evokeds[0].info['ch_names'][0]
        if re.match("^MEG[0-9]+", channelNameString):
            channelsToAve = _clean_names(channelsToAve, remove_whitespace=True)

        dataList = []
        # Picks only the desired channels from the evokeds.
        for evoked in evokeds:
            evokedToAve = wrap_mne_call(
                self.experiment,
                mne.pick_channels_evoked, evoked,
                list(channelsToAve)
            )
            # TODO: log something from below?
            # Returns channel indices for grad channel pairs in evokedToAve.
            ch_names = evokedToAve.ch_names
            gradsIdxs = _pair_grad_sensors_from_ch_names(ch_names)
    
            magsIdxs = mne.pick_channels_regexp(ch_names, regexp='MEG.{3,4}1$')
    
            eegIdxs = mne.pick_types(evokedToAve.info, meg=False, eeg=True,
                                       ref_meg=False)

            # Merges the grad channel pairs in evokedToAve
            if len(gradsIdxs) > 0:
                gradData = _merge_grad_data(evokedToAve.data[gradsIdxs])

                # Averages the gradData
                averagedGradData = np.mean(gradData, axis=0)

                # Links the event name and the corresponding data
                dataList.append((
                    evokedToAve.times, 
                    evokedToAve.comment + '_grad',
                    averagedGradData
                ))
            if len(magsIdxs) > 0:
                mag_data = evokedToAve.data[magsIdxs]
                averagedMagData = np.mean(mag_data, axis=0)
                dataList.append((
                    evokedToAve.times,
                    evokedToAve.comment + '_mag', 
                    averagedMagData
                ))
            if len(eegIdxs) > 0:
                eeg_data = evokedToAve.data[eegIdxs]
                averagedEegData = np.mean(eeg_data, axis=0)
                dataList.append((
                    evokedToAve.times,
                    evokedToAve.comment + '_eeg', 
                    averagedEegData
                ))

        return dataList

    def group_average(self, evoked_name, layout):
        """
        Plots group average of all subjects in the experiment. Also saves group
        average data to ``output`` folder.
        Keyword arguments:
        evoked_name        -- name of the evoked objects
        layout        -- Layout used for plotting channels.
        """
        #subjects_averaged = []
        count = 0
        group_info = {}
        for subject in self.experiment.subjects.values():
            if subject.evokeds.get(evoked_name):
                count += 1
                #subjects_averaged.append(subject.subject_name)
                evoked = subject.evokeds.get(evoked_name)
                group_info[subject.subject_name] = evoked.info

        if count == 0:
            raise ValueError('No evoked responses found from any subject.')
        if count > 0 and count < len(self.experiment.subjects):
            reply = QtGui.QMessageBox.question(
                self.parent, 
                "Evoked responses not found",
                "Evoked responses not found from every subject. "
                "(" + str(count) + " responses found.) "
                "Draw the evoked potentials anyway?",
                QtGui.QMessageBox.Yes,
                QtGui.QMessageBox.No
            )
            if reply == QtGui.QMessageBox.No:
                return
        
        evokeds = self._group_average(
           evoked_name, do_meanwhile=self.parent.update_ui
        )

        return evokeds, group_info #subjects_averaged, group_info

    @threaded
    def _group_average(self, evoked_name):
        """Performed in a worker thread."""

        subjects = self.experiment.subjects.values()
        responses = [subject.evokeds.get(evoked_name) for subject in subjects]
        responses = filter(bool, responses)

        # assumme all have same same amount of evokeds
        evoked_groups = {}
        
        for response in responses:
            for key, value in response.mne_evokeds.items():
                if evoked_groups.get(key):
                    evoked_groups[key].append(value)
                else:
                    evoked_groups[key] = [value]

        grand_averages = {}

        for key, evokeds in evoked_groups.items():
            grand_averaged = mne.grand_average(evokeds)
            grand_averaged.comment = key
            grand_averages[key] = grand_averaged

        return grand_averages

    def TFR(self, epochs, ch_index, minfreq, maxfreq, interval, ncycles,
            decim, color_map='auto'):
        """
        Plots a time-frequency representation of the data for a selected
        channel. Modified from example by Alexandre Gramfort.
        TODO should use dictionary like most other dialogs.
        Keyword arguments:
        epochs        -- Epochs extracted from the data.
        ch_index      -- Index of the channel to be used.
        minfreq       -- Starting frequency for the representation.
        maxfreq       -- Ending frequency for the representation.
        interval      -- Interval to use for the frequencies of interest.
        ncycles       -- Value used to count the number of cycles.
        decim         -- Temporal decimation factor.
        color_map     -- Matplotlib color map to use. Defaults to ``auto``, in
                         which case ``RdBu_r`` is used or ``Reds`` if only
                         positive values exist in the data.
        """
        plt.close()

        # Find intervals for given frequency band
        freqs = np.arange(minfreq, maxfreq, interval)
        n_jobs = self.parent.preferencesHandler.n_jobs
        
        @threaded
        def calculate_tfrs():
            power, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=ncycles, 
                                    decim=decim, n_jobs=n_jobs)
            evoked = epochs.average()
            return power, itc, evoked
            
        power, itc, evoked = calculate_tfrs()
        
        evoked_data = evoked.data[ch_index:(ch_index+1), :]
        evoked_times = 1e3 * evoked.times

        print 'Plotting TFR...'
        fig = plt.figure()

        plt.subplot2grid((3, 15), (0, 0), colspan=14)
        ch_type = mne.channels.channels.channel_type(evoked.info, ch_index)
        if ch_type == 'grad':
            plt.ylabel('Magnetic Field (fT/cm)')
            evoked_data *= 1e13
        elif ch_type == 'mag':
            plt.ylabel('Magnetic Field (fT)')
            evoked_data *= 1e15
        elif ch_type == 'eeg' or type == 'eog':
            plt.ylabel('Evoked potential (uV)')
            evoked_data *= 1e6
        else:
            raise TypeError('TFR plotting for %s channels not supported.' % 
                            ch_type)

        plt.plot(evoked_times, evoked_data.T)
        plt.title('Evoked response (%s)' % evoked.ch_names[ch_index])
        plt.xlabel('Time (ms)')
        plt.xlim(evoked_times[0], evoked_times[-1])

        data = power.data[0]

        if color_map == 'auto':
            cmap = 'RdBu_r' if np.min(data < 0) else 'Reds'
        else:
            cmap = color_map    

        plt.subplot2grid((3, 15), (1, 0), colspan=14)
        img = plt.imshow(data, extent=[evoked_times[0], evoked_times[-1],
            freqs[0], freqs[-1]], aspect='auto', origin='lower', cmap=cmap)
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Induced power (%s)' % evoked.ch_names[ch_index])
        plt.colorbar(cax=plt.subplot2grid((3, 15), (1, 14)), mappable=img)

        data = itc.data[0]

        if color_map == 'auto':
            cmap = 'RdBu_r' if np.min(data < 0) else 'Reds'
        plt.subplot2grid((3, 15), (2, 0), colspan=14)
        img = plt.imshow(data, extent=[evoked_times[0], evoked_times[-1],
            freqs[0], freqs[-1]], aspect='auto', origin='lower', cmap=cmap)
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Phase-lock (%s)' % evoked.ch_names[ch_index])
        plt.colorbar(cax=plt.subplot2grid((3, 15), (2, 14)), mappable=img)

        plt.tight_layout()
        fig.show()


    def TFR_topology(self, inst, reptype, freqs, decim, mode, blstart, blend,
                     ncycles, ch_type, scalp, color_map='auto'):
        """
        Plots time-frequency representations on topographies for MEG sensors.
        Modified from example by Alexandre Gramfort and Denis Engemann.
        Keyword arguments:
        inst          -- Epochs extracted from the data or previously computed
                         AverageTFR object to plot.
        reptype       -- Type of representation (average or itc).
        freqs         -- Frequencies for the representation as a numpy array.
        decim         -- Temporal decimation factor.
        mode          -- Rescaling mode (logratio | ratio | zscore |
                         mean | percent).
        blstart       -- Starting point for baseline correction.
        blend         -- Ending point for baseline correction.
        ncycles       -- Value used to count the number of cycles.
        layout        -- Layout to use.
        ch_type       -- Channel type (mag | grad | eeg).
        scalp         -- Parameter dictionary for scalp plot. If None, no scalp
                         plot is drawn.
        color_map     -- Matplotlib color map to use. Defaults to ``auto``, in
                         which case ``RdBu_r`` is used or ``Reds`` if only
                         positive values exist in the data.
        """

        plt.close()
        if isinstance(inst, mne.epochs._BaseEpochs):  # TFR from epochs
            power, itc = self._TFR_topology(inst, freqs, ncycles, decim,
                                            do_meanwhile=self.parent.update_ui)

        elif reptype == 'average':  # TFR from averageTFR
            power = inst
        elif reptype == 'itc':  # TFR from averageTFR
            itc = inst

        layout = self.read_layout(self.experiment.active_subject.layout)
        
        if blstart is None and blend is None:
            baseline = None
        else:
            baseline = (blstart, blend)

        print "Plotting..."
        #self.parent.update_ui()
        if reptype == 'average':  # induced
            if color_map == 'auto':
                cmap = 'RdBu_r' if np.min(power.data < 0) else 'Reds'
            else:
                cmap = color_map

            if scalp is not None:
                fig = wrap_mne_call(self.experiment,
                                    power.plot_topomap,
                                    tmin=scalp['tmin'],
                                    tmax=scalp['tmax'],
                                    fmin=scalp['fmin'],
                                    fmax=scalp['fmax'],
                                    ch_type=ch_type, layout=layout,
                                    baseline=baseline, mode=mode,
                                    show=False, cmap=cmap)

            print 'Plotting topology. Please be patient...'
            #self.parent.update_ui()
           
            fig = wrap_mne_call(self.experiment, power.plot_topo,
                                baseline=baseline, mode=mode, fmin=freqs[0],
                                fmax=freqs[-1], layout=layout, cmap=cmap,
                                title='Average power')

        elif reptype == 'itc':  # phase locked
            if color_map == 'auto':
                cmap = 'RdBu_r' if np.min(itc.data < 0) else 'Reds'
            else:
                cmap = color_map

            print 'Plotting topology. Please be patient...'
            title = 'Inter-Trial coherence'
            if scalp is not None:
                fig = wrap_mne_call(self.experiment, itc.plot_topomap,
                                    tmin=scalp['tmin'], tmax=scalp['tmax'],
                                    fmin=scalp['fmin'], fmax=scalp['fmax'],
                                    ch_type=ch_type, layout=layout,
                                    baseline=baseline, mode=mode,
                                    show=False)
                
            fig = wrap_mne_call(self.experiment, itc.plot_topo,
                                baseline=baseline, mode=mode, fmin=freqs[0],
                                fmax=freqs[-1], layout=layout, cmap=cmap,
                                title=title)

            fig.show()

        def onclick(event):
            pl.show(block=False)

        fig.canvas.mpl_connect('button_press_event', onclick)

    @threaded
    def _TFR_topology(self, epochs, frequencies, ncycles, decim):
        """
        Performed in a worker thread.
        """
        n_jobs = self.parent.preferencesHandler.n_jobs
        power, itc = wrap_mne_call(self.experiment, tfr_morlet, epochs,
                                   freqs=frequencies, n_cycles=ncycles,
                                   use_fft=False, return_itc=True,
                                   decim=decim, n_jobs=n_jobs)

        return power, itc

    def TFR_average(self, epochs_name, reptype, color_map, mode, minfreq,
                    maxfreq, interval, blstart, blend, ncycles, decim,
                    selected_channels, form, dpi, save_topo, save_plot,
                    save_max):
        """
        Method for computing average TFR over all subjects in the experiment.
        Creates data and picture files to output folder of the experiment.
        """
        layout = self.read_layout(self.experiment.active_subject.layout)

        frequencies = np.arange(minfreq, maxfreq, interval)

        power, itc = self._TFR_average(epochs_name, selected_channels, reptype,
                                       frequencies, ncycles, decim, save_max,
                                       do_meanwhile=self.parent.update_ui)

        if blstart is None and blend is None:
            baseline = None
        else:
            baseline = (blstart, blend)

        print 'Plotting topology...'
        if reptype == 'average':
            title = 'Average power ' + epochs_name
            self._plot_TFR_topology(power, baseline, mode, minfreq, maxfreq,
                                    layout, title, save_topo, save_plot,
                                    selected_channels, dpi, form, epochs_name,
                                    color_map)
        elif reptype == 'itc':
            title = 'Inter-trial coherence ' + epochs_name
            self._plot_TFR_topology(itc, baseline, mode, minfreq, maxfreq,
                                    layout, title, save_topo, save_plot,
                                    selected_channels, dpi, form, epochs_name,
                                    color_map)

    @threaded
    def _TFR_average(self, epochs_name, selected_channels, reptype,
                     frequencies, ncycles, decim, save_max=False):
        """Performed in a working thread."""
        chs = self.experiment.active_subject.get_working_file().info['ch_names']
        subjects = self.experiment.subjects.values()
        directory = ''
        files2ave = []
        for subject in subjects:
            directory = subject._epochs_directory
            fName = join(directory, epochs_name + '.fif')
            if isfile(fName):
                files2ave.append(fName)

        print ('Found ' + str(len(files2ave)) + ' subjects with epochs ' + 
               'labeled ' + epochs_name + '.')
        if len(files2ave) < len(subjects):
            raise Warning("Found only " + str(len(files2ave)) +
                          " subjects of " + str(len(subjects)) +
                          " with epochs labeled: " +
                          epochs_name + "!\n")
        powers = []
        itcs = []
        weights = []
        bads = []
        if save_max:
            exp_path = os.path.join(self.experiment.workspace,
                                    self.experiment.experiment_name)
            max_file = open(exp_path + '/output/' + save_max + '_maxima.txt',
                            'w')
        for f in files2ave:
            epochs = mne.read_epochs(join(directory, f))
            bads = bads + list(set(epochs.info['bads']) - set(bads))
            n_jobs = self.parent.preferencesHandler.n_jobs
            power, itc = wrap_mne_call(self.experiment, tfr_morlet, epochs,
                                       freqs=frequencies, n_cycles=ncycles,
                                       use_fft=False, return_itc=True,
                                       decim=decim, n_jobs=n_jobs)

            if save_max is not None:
                # Write file for maxima
                p = None
                if save_max == 'itc':
                    p = itc
                elif save_max == 'average':
                    p = power
                max_file.write(f)
                max_file.write('\n')
                for ch in selected_channels:
                    max_file.write(ch + '\n')
                    idx = p.ch_names.index(ch)
                    ch_data = p.data[idx]
                    i = np.argmax(ch_data)
                    f = i / len(ch_data[0])
                    t = i % len(ch_data[0])
                    f = p.freqs[f]
                    t = p.times[t]
                    string = 'freq: ' + str(f) + '; time: ' + str(t) + '\n'
                    max_file.write(string)
                max_file.write('\n')
            powers.append(power)
            itcs.append(itc)
            weights.append(len(epochs))

        if save_max:
            print 'Closing file'
            max_file.close()

        bads = set(bads)
        usedPowers = dict()
        usedItcs = dict()
        usedChannels = []

        print 'Populating the dictionaries'
        for ch in chs:
            if ch in bads:
                continue
            elif ch not in powers[0].ch_names:
                continue
            else:
                usedChannels.append(ch)
            if not usedPowers.has_key(ch):
                usedPowers[ch] = []
                usedItcs[ch] = []
            for i in xrange(len(powers)):
                cidx = powers[i].ch_names.index(ch)
                usedPowers[ch].append(powers[i].data[cidx])
                usedItcs[ch].append(itcs[i].data[cidx])
        averagePower = []
        averageItc = []

        print 'Averaging the values'
        for ch in usedChannels:
            averagePower.append(np.average(usedPowers[ch], axis=0,
                                           weights=weights))
            averageItc.append(np.average(usedItcs[ch], axis=0,
                                         weights=weights))

        ch_names = [x[:3] + ' ' + x[3:] 
                    if ' ' not in x 
                    else x for x in usedChannels]  # pre-set layouts have spaces
        ch_types = list()
        for name in ch_names:
            if name.startswith('MEG'):
                if name.endswith('1'):
                    ch_types.append('mag')
                else:
                    ch_types.append('grad')
            else:
                ch_types.append('eeg')

        #log mne call
        info = wrap_mne_call(self.experiment, mne.create_info,
                             ch_names=ch_names, ch_types=ch_types,
                             sfreq=powers[0].info['sfreq'])

        times = powers[0].times
        nave = sum(weights)
        averagePower = np.array(averagePower)
        averageItc = np.array(averageItc)

        power = wrap_mne_call(self.experiment,
                              mne.time_frequency.AverageTFR, info,
                              averagePower, times, frequencies, nave)

        itc = wrap_mne_call(self.experiment, mne.time_frequency.AverageTFR,
                            info, averageItc, times, frequencies, nave)

        return power, itc

    def _plot_TFR_topology(self, power, baseline, mode, fmin, fmax, layout,
                           title, save_topo=False, save_plot=False,
                           channels=[], dpi=200, form='png', epoch_name='',
                           color_map='auto'):
        """
        Convenience method for plotting TFR topologies.
        Parameters:
        power     - Average or itc power for plotting.
        baseline  - Baseline for the image.
        mode      -
        fmin      - Minimum frequency of interest.
        fmax      - Maximum frequency of interest.
        layout    - Layout for the image.
        title     - Title to show on the plot.
        save_topo - Boolean to indicate whether the figure is to be saved.
        save_plot -
        channels  - Channels of interest.
        dpi       - Dots per inch for the figures.
        form      - File format for the figures.
        epoch_name- Name of the epochs used for the TFR
        color_map - 
        """
        if color_map == 'auto':
            cmap = 'RdBu_r' if np.min(power.data < 0) else 'Reds'
        else:
            cmap = color_map
        exp_path = os.path.join(self.experiment.workspace,
                                self.experiment.experiment_name)
        if not os.path.isdir(exp_path + '/output'):
            os.mkdir(exp_path + '/output')
        if save_plot:
            for channel in channels:
                if not channel in power.ch_names:
                    print 'Channel ' + channel + ' not found!'
                    continue
                print ('Saving channel ' + channel + ' figure to ' + exp_path + 
                       '/output...')
                self.parent.update_ui()
                plt.clf()
                idx = power.ch_names.index(channel)
                try:
                    power.plot([idx], baseline=baseline, mode=mode, show=False)
                    plt.savefig(exp_path + '/output/average_tfr_channel_' + 
                                channel + '_' + epoch_name + '.' + form,
                                dpi=dpi, format=form)
                except Exception as e:
                    print 'Error while saving figure for channel ' + channel
                finally:
                    plt.close()

        plt.clf()
        fig = wrap_mne_call(self.experiment, power.plot_topo,
                            baseline=baseline, mode=mode, fmin=fmin,
                            fmax=fmax, layout=layout, title=title,
                            show=False, cmap=cmap)
        if save_topo:
            print 'Saving topology figure to  ' + exp_path + '/output...'
            fig_title= ''
            if title.startswith('Inter-trial'):
                fig_title = "".join([
                    exp_path, '/output/group_tfr_', epoch_name, '_itc.', form
                ])
            elif title.startswith('Average'):
                fig_title = "".join([
                    exp_path, '/output/group_tfr_', epoch_name, '_average.', 
                    form
                ])
            plt.savefig(fig_title, dpi=dpi, format=form)
            plt.close()
        else:
            def onclick(event):
                plt.show(block=False)
            fig.canvas.mpl_connect('button_press_event', onclick)
            plt.show()

    def TFR_raw(self, wsize, tstep, channel, fmin, fmax):
        lout = self.read_layout(self.experiment.active_subject.layout)
        
        raw = self.experiment.active_subject.get_working_file()
        
        raw = raw.copy()
        raw.apply_proj()
        
        tfr = np.abs(mne.time_frequency.stft(raw._data, wsize, tstep=tstep))
        freqs = mne.time_frequency.stftfreq(wsize, sfreq=raw.info['sfreq'])
        times = np.arange(tfr.shape[2]) * tstep / raw.info['sfreq']
        
        tfr_ = mne.time_frequency.AverageTFR(raw.info, tfr, times, freqs, 1)
        
        if (not fmin and raw.info['highpass'] and 
                not math.isnan(raw.info['highpass'])):
            fmin = raw.info['highpass']

        if (not fmax and raw.info['lowpass'] and 
                not math.isnan(raw.info['lowpass'])):
            fmax = raw.info['lowpass']
        
        tfr_.plot(picks=[channel], fmin=fmin, fmax=fmax,
                  layout=lout, mode='logratio')


    def plot_power_spectrum(self, params, save_data, epoch_groups, basename='raw'):
        """
        Method for plotting power spectrum.
        Parameters:
        params         - Dictionary containing the parameters.
        save_data      - Boolean indicating whether to save psd data to files.
                         Only data from channels of interest is saved.
        """
        lout = self.read_layout(self.experiment.active_subject.layout)
            
        for epochs in epoch_groups.values():
            info = epochs[0].info
            break
            
        picks = mne.pick_types(info, meg=True, eeg=True,
                               exclude=[])
        params['picks'] = picks
        psd_groups = self._compute_spectrum(epoch_groups, params,
                                            do_meanwhile=self.parent.update_ui)
    
        for psd_list in psd_groups.values():
            freqs = psd_list[0][1]
            break
        
        psds = []
        for psd_list in psd_groups.values():
            psds.append(np.mean([psds_ for psds_, freqs in psd_list], axis=0))
            
        colors = self.colors(len(psds))

        if save_data:
            subject_name = self.experiment.active_subject.subject_name
            for idx, psd in enumerate(psds):
                filename = ''.join([subject_name, '_', basename, '_',
                    'spectrum', '_', str(psd_groups.keys()[idx]), '.txt'])
                fileManager.save_np_array(self.experiment, filename, 
                                          freqs, psd, info)

        print "Plotting power spectrum..."

        def my_callback(ax, ch_idx):
            """
            Callback for the interactive plot.
            Opens a channel specific plot.
            """
            conditions = [str(key) for key in psd_groups]
            positions = np.arange(0.025, 0.025 + 0.04 * len(conditions), 0.04)
            
            for cond, col, pos in zip(conditions, colors, positions):
                ax.figtext(0.775, pos, cond, color=col, fontsize=12)

            color_idx = 0
            for psd in psds:
                ax.plot(freqs, psd[ch_idx], color=colors[color_idx])
                color_idx += 1
            
            plt.xlabel('Frequency (Hz)')
            if params['log']:
                plt.ylabel('Power (dB)')
            else:
                plt.ylabel('(uV)')
            plt.show()

        info = deepcopy(info)
        info['ch_names'] = [ch for idx, ch in enumerate(info['ch_names'])
                            if idx in picks]

        for ax, idx in iter_topography(info, fig_facecolor='white',
                                       axis_spinecolor='white',
                                       axis_facecolor='white', layout=lout,
                                       on_pick=my_callback):
            
            color_idx = 0
            for psd in psds:
                ax.plot(psd[idx], linewidth=0.2, color=colors[color_idx])
                color_idx += 1
        plt.show()

    @threaded
    def _compute_spectrum(self, epoch_groups, params):
        """Performed in a worker thread."""
        fmin = params['fmin']
        fmax = params['fmax']
        nfft = params['nfft']
        overlap = params['overlap']
        picks = params['picks']

        psd_groups = OrderedDict()
        n_jobs = self.parent.preferencesHandler.n_jobs
        
        for key, epochs in epoch_groups.items():
            for epoch in epochs:
                psds, freqs = wrap_mne_call(self.experiment, psd_welch,
                                            epoch, fmin=fmin, fmax=fmax, 
                                            n_fft=nfft, n_overlap=overlap, 
                                            picks=picks, proj=True, verbose=True,
                                            n_jobs=n_jobs)
                psds = np.average(psds, axis=0)
                if params['log']:
                    psds = 10 * np.log10(psds)
                
                if key not in psd_groups:
                    psd_groups[key] = []
                psd_groups[key].append((psds, freqs))
        return psd_groups

    @threaded
    def filter(self, dic, subject, preview=False):
        """
        Filters the data array in place according to parameters in paramDict.
        Depending on the parameters, the filter is one or more of
        lowpass, highpass and bandstop (notch) filter.

        Keyword arguments:

        dataToFilter         -- a raw object
        info                 -- info for the data file to filter
        dic                  -- Dictionary with filtering parameters

        Returns the filtered array.
        """
        return self._filter(dic, subject, preview)
    
    def _filter(self, dic, subject, preview):
        """Performed in a working thread."""
        dataToFilter = subject.get_working_file()
        
        if preview:
            dataToFilter = dataToFilter.copy()
            
        info = dataToFilter.info
        hfreq = dic['low_cutoff_freq'] if dic['lowpass'] else None
        lfreq = dic['high_cutoff_freq'] if dic['highpass'] else None
        length = dic['length']
        trans_bw = dic['trans_bw']
        n_jobs = self.parent.preferencesHandler.n_jobs

        print "Filtering..."
        wrap_mne_call(self.experiment, dataToFilter.filter,
                      l_freq=lfreq, h_freq=hfreq, filter_length=length,
                      l_trans_bandwidth=trans_bw,
                      h_trans_bandwidth=trans_bw, n_jobs=n_jobs,
                      method='fft', verbose=True)

        freqs = list()
        if dic['bandstop1']:
            freqs.append(dic['bandstop1_freq'])
        if dic['bandstop2']:
            freqs.append(dic['bandstop2_freq'])
        if len(freqs) > 0:
            length = dic['bandstop_length']
            trans_bw = dic['bandstop_transbw']

            print "Band-stop filtering..."
            wrap_mne_call(self.experiment, dataToFilter.notch_filter,
                          freqs, picks=None, filter_length=length,
                          notch_widths=dic['bandstop_bw'],
                          trans_bandwidth=trans_bw, n_jobs=n_jobs,
                          verbose=True)
           
        if not preview:
            print 'Saving to file...'
            fileManager.save_raw(self.experiment, dataToFilter, info['filename'], overwrite=True)
        
        return dataToFilter

### Methods needed for source modeling ###    

    def convert_mri_to_mne(self):
        """
        Uses mne_setup_mri to active subject recon directory to create Neuromag
        slices and sets (to be input later to do_forward_solution).
        
        Return True if creation successful, False if there was an error. 
        """
        # TODO: log created Neuromag files?
        sourceAnalDir = self.experiment.active_subject.\
                            _source_analysis_directory
        
        
        # Hack the SUBJECT_DIR and SUBJECT variables to right location 
        # (mne_setup_mri searches for reconstructed files from mri directory
        # under the SUBJECT)
        os.environ['SUBJECTS_DIR'] = sourceAnalDir
        os.environ['SUBJECT'] = 'reconFiles'
        
        subprocess.check_output("$MNE_ROOT/bin/mne_setup_mri", shell=True)

    def create_forward_model(self, fmdict):
        """
        Creates a single forward model and saves it to an appropriate
        directory.
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
        (setupSourceSpaceArgs, waterShedArgs, setupFModelArgs) = \
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
                wshedDict = fileManager.unpickle(os.path.join(fmDir,
                                                              'wshed.param'))

                fModelSkipDialog = ForwardModelSkipDialog(self, sSpaceDict,
                                                          wshedDict)
            
                fModelSkipDialog.exec_()
                reply = fModelSkipDialog.get_return_value()
            except:
                # On error compute all.
                reply = 'computeAll'
        
        if reply == 'cancel':
            # To keep forward model dialog open
            return False
        
        elif reply == 'bemOnly':
            # Need to do this to get triangulation files to right place and
            # naming for mne_setup_forward_model.
            fileManager.link_triang_files(activeSubject)
            self._call_mne_setup_forward_model(setupFModelArgs, env)
        
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
        
        elif reply == 'computeAll':
            # To make overwriting unnecessary
            if os.path.isdir(bemDir):
                shutil.rmtree(bemDir)
            self._call_mne_setup_source_space(setupSourceSpaceArgs, env)
            self._call_mne_watershed_bem(waterShedArgs, env)
            
            # Right name and place for triang files, see above.
            fileManager.link_triang_files(activeSubject)
            self._call_mne_setup_forward_model(setupFModelArgs, env)    
        
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

        return True

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
            raise Exception('There was a problem with mne_setup_source_space. Script '
                            'output: \n' + e.output)
        except Exception as e:
            message = 'There was a problem with mne_setup_source_space: ' + \
                      str(e) + \
                      ' (Are you sure you have your MNE_ROOT set right ' + \
                      'in Meggie preferences?)'
            raise Exception(message)

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
            message = 'There was a problem with mne_watershed_bem. ' + \
                      'Script output: \n' + e.output
            raise Exception(message)

        except Exception as e:
            message = 'There was a problem with mne_watershed_bem: ' + \
                      str(e) + \
                      ' (Are you sure you have your MNE_ROOT set right ' + \
                      'in Meggie preferences?)'
            raise Exception(message)

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
            message = 'There was a problem with mne_setup_forward_model. ' + \
                     'Script output: \n' + e.output
            raise Exception(message)
        except Exception as e:
            message = 'There was a problem with mne_setup_forward_model: ' + \
                      str(e) + \
                      ' (Are you sure you have your MNE_ROOT set right ' + \
                      'in Meggie preferences?)'
            raise Exception(message)

    def coregister_with_mne_gui_coregistration(self):
        """
        Uses mne.gui.coregistration for head coordinate coregistration.
        """
        activeSubject = self.experiment.active_subject
        tableView = self.parent.ui.tableViewFModelsForCoregistration
        
        # Selection for the view is SingleSelection / SelectRows, so this
        # should return indexes for single row.
        selectedRowIndexes = tableView.selectedIndexes()
        selectedFmodelName = selectedRowIndexes[0].data() 
                             
        subjects_dir = os.path.join(activeSubject._forwardModels_directory,
                                    selectedFmodelName)
        subject = 'reconFiles'
        rawPath = os.path.join(activeSubject.subject_path,
                               self.experiment.active_subject.working_file_name)

        gui = mne.gui.coregistration(tabbed=True, split=True, scene_width=300,
                                     inst=rawPath, subject=subject,
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
        activeSubject = self.experiment._active_subject
        rawInfo = activeSubject.get_working_file().info

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

        targetFileName = os.path.join(fmdir, 'reconFiles',
                                      'reconFiles-fwd.fif')
        n_jobs = self.parent.preferencesHandler.n_jobs

        try:
            mne.make_forward_solution(rawInfo, transFilePath, srcFilePath,
                                      bemSolFilePath, targetFileName,
                                      fsdict['includeMEG'],
                                      fsdict['includeEEG'], fsdict['mindist'],
                                      fsdict['ignoreref'], True,
                                      n_jobs)
            fileManager.write_forward_solution_parameters(fmdir, fsdict)
            self.parent.forwardModelModel.initialize_model()
        except Exception as e:
            msg = ('There was a problem with forward solution. The MNE-Python '
                   'message was: \n\n' + str(e))
            raise Exception(msg)

    def compute_inverse(self, fwd_name):
        """Computes an inverse operator for the forward solution and saves it
        to the source_analysis directory.
        Keyword arguments:
            fwd: The forward operator name.

        Returns:
            The inverse operator
        """
        subject = self.experiment.active_subject
        info = subject.get_working_file().info
        sa_dir = subject._source_analysis_directory
        fwd_file = os.path.join(subject._forwardModels_directory, fwd_name,
                                'reconFiles', 'reconFiles-fwd.fif')
        if os.path.isfile(fwd_file):
            print 'Reading forward solution...'
        else:
            raise IOError('Could not find forward solution with name %s.' %
                          fwd_file)
        fwd = mne.read_forward_solution(fwd_file)
        cov = subject.get_cov()
        inv = mne.minimum_norm.make_inverse_operator(info, fwd, cov)
        inv_fname = os.path.join(sa_dir, subject.subject_name + '-inv.fif')
        try:
            mne.minimum_norm.write_inverse_operator(inv_fname, inv)
        except Exception as e:
            msg = ('Exception while computing inverse operator:\n\n' + str(e))
            raise Exception(msg)
        return inv

    def create_covariance_from_raw(self, cvdict):
        """
        Computes a covariance matrix based on raw file and saves it to the
        approriate location under the subject.

        Keyword arguments:

        cvdict        -- dictionary containing parameters for covariance
                         computation
        """
        subject_name = cvdict['rawsubjectname']
        if subject_name is not None:
            subject = self.experiment.subjects[subject_name]
            raw = subject.get_working_file()
            name = os.path.basename(subject.working_file_name)
            filename_to_write = name[:-4] + '-cov.fif'
        else:
            raw = fileManager.open_raw(cvdict['rawfilepath'], True)
            basename = os.path.basename(cvdict['rawfilepath'])[0]
            filename_to_write = os.path.splitext(basename)[:-4] + '-cov.fif'

        tmin = cvdict['starttime']
        tmax = cvdict['endtime']
        tstep = cvdict['tstep']

        reject = cvdict['reject']
        flat = cvdict['flat']
        picks = cvdict['picks']

        try:
            cov = mne.cov.compute_raw_covariance(raw, tmin, tmax, tstep,
                                                 reject, flat, picks)
        except ValueError as e:
            raise ValueError('Error while computing covariance. ' + str(e))

        self._save_covariance(cov, cvdict, filename_to_write)

    def create_covariance_from_epochs(self, params):
        subject = self.experiment.active_subject
        collection_names = params['collection_names']
        epochs = []
        filename_to_write = ''

        for collection_name in collection_names:
            epoch = subject.epochs.get(collection_name)
            epochs.append(epoch.raw)
            filename_to_write += os.path.splitext(collection_name)[0] + '-'
        
        filename_to_write = filename_to_write[:len(filename_to_write)-1] + '-cov.fif'
        tmin = params['tmin']
        tmax = params['tmax']
        keep_sample_mean = params['keep_sample_mean']
        method = params['method']
        n_jobs = self.parent.preferencesHandler.n_jobs
        
        try:
            cov = mne.compute_covariance(epochs,
                keep_sample_mean=keep_sample_mean, tmin=tmin, tmax=tmax,
                method=method, n_jobs=n_jobs)            
        except ValueError as e:
            raise ValueError('Error while computing covariance. ' + str(e))
        
        self._save_covariance(cov, params, filename_to_write)
        
    def _save_covariance(self, cov, params, filename_to_write):
        
        path = self.experiment.active_subject._source_analysis_directory

        # Remove previous covariance file before creating a new one.
        fileManager.remove_files_with_regex(path, '.*-cov.fif')

        filepath_to_write = os.path.join(path, filename_to_write)
        try:
            mne.write_cov(filepath_to_write, cov)
        except IOError as err:
            err.message = ('Could not write covariance file. The error '
                           'message was: \n\n' + err.message)
            raise

        # Delete previous and write a new parameter file.
        try:
            fileManager.remove_files_with_regex(path, 'covariance.param')
            cvparamFile = os.path.join(path, 'covariance.param')
            fileManager.pickleObjectToFile(params, cvparamFile)

        except Exception:
            fileManager.remove_files_with_regex(path, '*-cov.fif')
            raise

        # Update ui.
        self.parent.update_covariance_info_box()

    def plot_covariance(self):
        """Plots the covariance matrix."""
        subject = self.experiment.active_subject
        cov = subject.get_cov()
        cov.plot(subject._working_file.info)

    def make_source_estimate(self, inst_name, type, inv_name, method, lmbd):
        """
        Method for computing source estimate.
        Args:
            inst_name: Name of the data instance.
            type: str to indicate type of data.
                One of ['raw', 'epochs', 'evoked'].
            inv_name: Name of the inverse operator.
            method: Method to use ('MNE', 'dSPM', 'sLORETA').
            lmbd: Regularization parameter.
        """
        # TODO: refactor
        subject = self.experiment.active_subject
        source_dir = subject._source_analysis_directory
        inv_file = os.path.join(source_dir, inv_name)

        try:
            inv = mne.minimum_norm.read_inverse_operator(inv_file)
        except Exception as err:
            raise Exception('Error while reading inverse '
                            'operator:\n' + str(err))
        if type == 'raw':
            inst = subject.get_working_file()
            try:
                stc = mne.minimum_norm.apply_inverse_raw(inst, inv,
                                                         lambda2=lmbd,
                                                         method=method)
            except Exception as err:
                raise Exception('Exception while computing inverse '
                                'solution:\n' + str(err))
        elif type == 'epochs':
            inst = subject.epochs[inst_name].raw
            try:
                stc = mne.minimum_norm.apply_inverse_epochs(inst, inv,
                                                            lambda2=lmbd,
                                                            method=method)
            except Exception as err:
                raise Exception('Exception while computing inverse '
                                'solution:\n' + str(err))
        elif type == 'evoked':
            evoked = subject.evokeds[inst_name]
            stc = list()

            for mne_evoked in evoked.mne_evokeds.values():
                try:
                    stc.append(mne.minimum_norm.apply_inverse(mne_evoked, inv,
                        lambda2=lmbd, method=method))
                except Exception as err:
                    raise Exception('Exception while computing inverse '
                                    'solution:\n' + str(err))

        stc_fname = os.path.split(inv_file)[-1]
        if isinstance(stc, list):  # epochs and evoked saved individually
            if type == 'epochs':
                stc_path = os.path.join(subject._stc_directory,
                                        stc_fname[:-8] + '-' + type + '-' +
                                        method)
                os.mkdir(stc_path)
            for i, estimate in enumerate(stc):
                if type == 'epochs':
                    stc_fname = os.path.join(stc_path, 'epoch-' + str(i))
                else:
                    stc_fname = os.path.join(subject._stc_directory,
                                             stc_fname[:-8] + '-' + type +
                                             '-' + method + str(i))
                try:
                    estimate.save(stc_fname)
                except Exception as err:
                    raise Exception('Exception while saving inverse '
                                    'solution:\n' + str(err))
            print 'Inverse solution computed succesfully.'
            return stc

        stc_fname = os.path.join(subject._stc_directory,
                                 stc_fname[:-8] + '-' + type + '-' + method)
        try:
            stc.save(stc_fname)
        except Exception as err:
            raise Exception('Exception while saving inverse '
                            'solution:\n' + str(err))
        print 'Inverse solution computed succesfully.'
        return stc

    def plotStc(self, stc_name, hemi, surface, smoothing_steps, alpha):
        """Method for plotting source estimate.
        Args:
            stc: Stc name.
            hemi: Hemisphere 'lh', 'rh' or 'both'.
            surface: Type of surface.
            smoothing_steps: The amount of smoothing.
            alpha: Alpha value to use.
        """
        subject = self.experiment.active_subject
        stc_dir = subject._stc_directory
        fname = os.path.join(stc_dir, stc_name)
        stc = mne.read_source_estimate(fname)
        try:
            stc.plot(subject='', surface=surface, hemi=hemi, alpha=alpha,
                     smoothing_steps=smoothing_steps, time_viewer=True,
                     subjects_dir=subject._reconFiles_directory)
        except Exception as e:
            raise Exception('Error while plotting source estimate:\n' + str(e))

    def tfr_clicked(self, event, data, stc, freqs):
        """
        Callback function for plotting frequencies in source space.
        Args:
            event: Mpl event.
            data: Power in shape (sources, times).
            stc: Instance of SourceEstimate. Used for wrapping the freq data.
            freqs: List of float. Frequencies of interest.
        """
        x_data = event.xdata
        y_data = event.ydata
        ax = event.inaxes
        ax.text(0.5, 0.5, 'Loading...')
        ax.get_figure().canvas.draw()
        #time_idx = np.argmin([abs(x_data / 1000. - t) for t in stc.times])
        freq_idx = np.argmin([abs(y_data - f) for f in freqs])
        stc._data = data[:, freq_idx, :]
        subjects_dir = self.experiment.active_subject.reconFiles_directory
        label = str(freqs[freq_idx]) + ' Hz, time=%0.2f ms'
        stc.plot(subject='', subjects_dir=subjects_dir, time_label=label,
                 time_viewer=True)

    def plot_stc_freq(self, stc, data, freqs, tmin, tmax, ncycles):
        """
        Computes morlet tfr over set of stcs over epochs. Operates on stc
        instance in place.
        Args:
            stc: Instance of stc containing the info. Used as a wrapper when
                plotting the frequencies in source space. Modified in place.
            data: Data in shape (epochs, sources, times).
            freqs: List of float. Frequencies of interest.
            tmin: Float. Minimum time of interest.
            tmax: Float. Maximum time of interest.
            ncycles: Float or list of float. Number of cycles for the wavelet.

        Returns: Instance of figure.
        Matplotlib figure containing average TFR over the epoch stcs.

        """
        import matplotlib.pyplot as plt

        n_jobs = self.parent.preferencesHandler.n_jobs
        tmin_i = np.argmin([abs(tmin - t) for t in stc.times])
        tmax_i = np.argmin([abs(tmax - t) for t in stc.times])
        data = np.array(data)[:, :, tmin_i:tmax_i]
        power, _ = mne.time_frequency.tfr._induced_power_cwt(data,
            sfreq=stc.sfreq, frequencies=freqs, n_cycles=ncycles, n_jobs=n_jobs)

        fig, ax = plt.subplots(1, 1)
        ax.imshow(np.mean(power, axis=0),
                  extent=(stc.times[tmin_i], stc.times[tmax_i], freqs[0],
                          freqs[-1]), aspect="auto", origin="lower")
        

        stc.times = stc.times[tmin_i:tmax_i]
        click_callback = partial(self.tfr_clicked, data=power, stc=stc,
                                 freqs=freqs)
        fig.canvas.mpl_connect('button_press_event', click_callback)
        fig.suptitle('Average power over all sources.')
        plt.show(block=True)
        return fig

    def colors(self, n):
        import itertools
        cycler = itertools.cycle(['b', 'r', 'g', 'y', 'm', 'c', 'k', 'pink'])
        return list(itertools.islice(cycler, n))