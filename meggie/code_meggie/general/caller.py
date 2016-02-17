# coding: utf-8
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
import inspect
from inspect import getcallargs
import linecache

from PyQt4 import QtCore, QtGui

import mne
from mne.channels.layout import read_layout
from mne.channels.layout import _pair_grad_sensors_from_ch_names
from mne.channels.layout import _merge_grad_data
from mne.viz import plot_topo
from mne.viz import iter_topography
from mne.utils import _clean_names
from mne.time_frequency.tfr import tfr_morlet, _induced_power_cwt
from mne.time_frequency import compute_raw_psd
from mne.preprocessing import compute_proj_ecg, compute_proj_eog
from mne.filter import low_pass_filter, high_pass_filter, band_stop_filter,\
    notch_filter

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join
from subprocess import CalledProcessError
from time import sleep
from copy import deepcopy

from meggie.ui.sourceModeling.holdCoregistrationDialogMain import holdCoregistrationDialog
from meggie.ui.sourceModeling.forwardModelSkipDialogMain import ForwardModelSkipDialog
from meggie.ui.utils.decorators import messaged
from meggie.ui.utils.decorators import threaded

from meggie.code_meggie.general.wrapper import wrap_mne_call
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.general.measurementInfo import MeasurementInfo
from meggie.code_meggie.general.singleton import Singleton


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

    # @messaged
    # @threaded
    def activate_subject(self, name):
        """
        Activates the subject.
        Keyword arguments:
        name      -- Name of the subject to activate.
        """
        if name == '':
            return

        self.experiment.activate_subject(name)
    
    def index_as_time(self, sample):
        """
        Aux function for converting sample to time.
        Keyword arguments:
        sample      -- Sample to convert to time.
        Returns time as seconds.
        """
        raw = self.experiment.active_subject.working_file
        
        #log mne call
        #self.log_action(raw.index_as_time, sample - raw.first_samp, 0)
        return raw.index_as_time(sample - raw.first_samp)[0]

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

    @messaged
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
        return True

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
        self.update_experiment_working_file(outputfile, raw)

        self.experiment.save_experiment_settings()

    def call_ecg_ssp(self, dic, subject):
        """
        Creates ECG projections using SSP for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        subject       -- The subject to perform the action on.
        """
        self._call_ecg_ssp(dic, subject, do_meanwhile=self.parent.update_ui)
        return 0

    @threaded
    def _call_ecg_ssp(self, dic, subject):
        """Performed in a worker thread."""
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
        if bads is None or bads == ['']:
            bads = []

        start = dic.get('tstart')
        taps = dic.get('filtersize')
        njobs = dic.get('n-jobs')
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

        projs, events = wrap_mne_call(self.experiment, 
                                      compute_proj_ecg, 
                                      raw_in, None, tmin, tmax, grad,
                                      mag, eeg, filter_low, filter_high,
                                      comp_ssp, taps, njobs, ch_name,
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
        return 0

    @threaded
    def _call_eog_ssp(self, dic, subject):
        """Performed in a worker thread."""
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
        if bads is None or bads == ['']:
            bads = []
        start = dic.get('tstart')
        taps = dic.get('filtersize')
        njobs = dic.get('n-jobs')
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

        projs, events = wrap_mne_call(self.experiment, compute_proj_eog,
                                      raw_in, None, tmin, tmax, grad,
                                      mag, eeg, filter_low, filter_high,
                                      comp_ssp, taps, njobs, reject,
                                      flat, bads, eeg_proj, excl_ssp,
                                      event_id, eog_low_freq,
                                      eog_high_freq, start)


        # TODO Reading a file
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)

        print "Writing EOG projections in %s" % eog_proj_fname
        #log mne call
        wrap_mne_call(self.experiment, mne.write_proj, eog_proj_fname, projs)

        print "Writing EOG events in %s" % eog_event_fname
        wrap_mne_call(self.experiment, mne.write_events, eog_event_fname, events)

    @messaged
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
        return True

    @threaded
    def _apply_exg(self, kind, raw, directory, projs, applied):
        """Performed in a worker thread."""
        if kind == 'ecg':
            if len(filter(os.path.isfile,
                      glob.glob(directory + '/*-eog_applied.fif'))) > 0:
                fname = glob.glob(directory + '/*-eog_applied.fif')[0]
            else:
                fname = raw.info.get('filename')
        elif kind == 'eog':
            if len(filter(os.path.isfile,
                      glob.glob(directory + '/*-ecg_applied.fif'))) > 0:
                fname = glob.glob(directory + '/*-ecg_applied.fif')[0]
            else:
                fname = raw.info.get('filename')

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

        if kind + '_applied' not in fname:
            fname = fname.split('.')[-2] + '-' + kind + '_applied.fif'

        #wrap_mne_call(self.experiment, raw.save, fname, overwrite=True)
        fileManager.save_raw(self.experiment, raw, fname, overwrite=True)
        
        raw = mne.io.Raw(fname, preload=True)
        self.update_experiment_working_file(fname, raw)
        self.experiment.save_experiment_settings()

    @messaged
    def plot_projs_topomap(self, raw):
        wrap_mne_call(self.experiment, raw.plot_projs_topomap)

    def average(self, epochs, category):
        """Average epochs.

        Average epochs and save the evoked dataset to a file.
        Raise an exception if epochs are not found.

        Keyword arguments:
        epochs      -- Epochs averaged
        """
        if epochs is None:
            raise Exception('No epochs found.')

        # Creates evoked potentials from the given events (variable 'name' 
        # refers to different categories).
        evokeds = []
        for epoch in epochs:
            for name in category.keys():
                if name in epoch.event_id:
                    evokeds.append(epoch[name].average())
                    #evokeds.append(wrap_mne_call(self.experiment, epoch[name].average()))
        #log mne call
        #TODO: epochs is a list of epoch -> log to single line with a comma separator
        self.experiment.action_logger.log_message('SUCCESS: average' + '\n' + str(epochs) + '\n-->' + '\n' + str(evokeds))
        return evokeds

    @messaged
    def batchEpoch(self, subjects, epoch_name, tmin, tmax, stim, event_id,
                   mask, event_name, grad, mag, eeg, eog):
        """
        Creates epoch collection for all ``subjects`` with the given parameters

        Keyword arguments:
        subjects      - List of strings. Subjects to create epochs for.
        epoch_name    - The name of the epoch collection as string.
        tmin          - Start time for epochs as float.
        tmax          - End time for epochs as float.
        stim          - Boolean to indicate whether to include stim channel.
        event_id      - The event_id as int.
        mask          - Bit wise mask as int.
        event_name    - Name for the event as string.
        grad          - Peak-to-peak rejection limit for gradiometer channels
                        or None if gradiometer channels are not included.
        mag           - Peak-to-peak rejection limit for magnetometer channels
                        or None if magnetometer channels are not included.
        eeg           - Peak-to-peak rejection limit for EEG channels
                        or None if EEG channels are not included.
        eog           - Peak-to-peak rejection limit for EOG channels
                        or None if EOG channels are not included.
        """

        self._batchEpoch(subjects, epoch_name, tmin, tmax, stim,
                         event_id, mask, event_name, grad, mag, eeg,
                         eog, do_meanwhile=self.parent.update_ui)

    @threaded
    def _batchEpoch(self, subjects, epoch_name, tmin, tmax, stim, event_id,
                    mask, event_name, grad, mag, eeg, eog):
        """Performed in a worker thread."""
        # active_subject = self.experiment.active_subject_name
        path = self.experiment.workspace
        working_files = self.experiment._working_file_names.values()
        reject = dict()
        if grad is not None and grad >= 0:
            reject['grad'] = grad
        if mag is not None and mag >= 0:
            reject['mag'] = mag
        if eeg is not None and eeg >= 0:
            reject['eeg'] = eeg
        if eog is not None and eog >= 0:
            reject['eog'] = eog
        mag = mag is not None
        grad = grad is not None
        eeg = eeg is not None
        eog = eog is not None

        for subject in subjects:
            path = os.path.join(path, subject)
            fname = ''
            for working_file in working_files:
                if os.path.split(working_file)[1].startswith(subject):
                    fname = working_file
                    break
            if fname == '':
                print 'Could not find working file for %s. Skipping.' % subject
                continue
            for sub in self.experiment.get_subjects():
                if sub.subject_name == subject:
                    this_subject = sub
                    break

            stim_channel = this_subject.stim_channel
            try:
                raw = mne.io.Raw(fname)
                #log mne call
                events = wrap_mne_call(self.experiment, mne.find_events, raw, stim_channel=stim_channel,
                                         shortest_event=1, mask=mask)
                #log mne call
                events = wrap_mne_call(self.experiment, mne.pick_events, events, include=event_id)
                epocher = Epochs()

                #log mne call in Epochs class
                epochs = epocher.create_epochs(self.experiment, raw, events, mag, grad, eeg,
                                               stim, eog, reject,
                                               {event_name: event_id}, tmin,
                                               tmax)
            except Exception as e:
                raise Exception('Could not create epochs for subject ' +
                                subject + ':\n' + str(e) + '\n')

            path = os.path.join(os.path.split(fname)[0], 'epochs')
            fname = os.path.join(path, epoch_name)
            events = [(event, event_name) for event in events]
            params = {'events': events, 'mag': mag, 'grad': grad,
                      'eeg': eeg, 'stim': stim, 'eog': eog,
                      'reject': reject, 'tmin': tmin, 'tmax': tmax,
                      'collectionName': epoch_name, 'raw': fname}
            this_subject.handle_new_epochs(epoch_name, params)
            # epochs_object = this_subject._epochs[epoch_name]
            fileManager.save_epoch(fname, epochs, params, overwrite=True)

    @messaged
    def create_new_epochs(self, epoch_params):
        """
        A method for creating new epochs with the given parameter values for
        the active subject.

        Keyword arguments:
        epoch_params = A dictionary containing the parameter values for
                       creating the epochs minus the raw data.
        """
        # Raw data is not present in the dictionary so get it from the
        # current experiment.active_subject.
        epocher = Epochs()
        subject = self.experiment.active_subject
        epochs = epocher.create_epochs_from_dict(self.experiment, epoch_params,
                                                 subject.working_file)

        epoch_params['raw'] = self.experiment._working_file_names[self.experiment._active_subject_name]

        fname = epoch_params['collectionName']
        self.experiment.active_subject.handle_new_epochs(fname, epoch_params)

        fpath = os.path.join(subject._epochs_directory, fname)

        fileManager.save_epoch(fpath, epochs, epoch_params, True)

    def draw_evoked_potentials(self, evokeds, layout):  # , category):
        """
        Draws a topography representation of the evoked potentials.

        Keyword arguments:
        evokeds  - Evoked object or list of evokeds.
        layout   - The desired layout as a string.
        """
        if layout == 'Infer from data':
            layout = None  # Tries to guess the locations from the data.
        else:
            layout = read_layout(layout)

        colors = ['y', 'm', 'c', 'r', 'g', 'b', 'w', 'k']

        mi = MeasurementInfo(self.experiment.active_subject.working_file)

        title = mi.subject_name

        fig = wrap_mne_call(self.experiment, plot_topo, evokeds, layout,
                            color=colors[:len(evokeds)], title=title)

        conditions = [e.comment for e in evokeds]
        positions = np.arange(0.025, 0.025 + 0.04 * len(evokeds), 0.04)
        for cond, col, pos in zip(conditions, colors[:len(evokeds)],
                                  positions):
            plt.figtext(0.775, pos, cond, color=col, fontsize=12)

        fig.show()
        
        # TODO: log info about the clicked channels
        def onclick(event):
            plt.show(block=False)

        fig.canvas.mpl_connect('button_press_event', onclick)

    @messaged
    def average_channels(self, instance, lobeName, channelSet=None):
        """
        Shows the averages for averaged channels in lobeName, or channelSet
        if it is provided.

        Keyword arguments:
        instance     -- name of the epochs to average, evoked object or list of
                        evoked objects.
        lobename     -- the lobe over which to average.
        channelSet   -- manually input list of channels. 
        """

        result = self._average_channels(instance, lobeName, channelSet,
                                        do_meanwhile=self.parent.update_ui)
        averageTitleString, dataList, evokeds = result

        # Plotting:
        plt.clf()
        fig = plt.figure()
        mi = MeasurementInfo(self.experiment.active_subject._working_file)
        fig.canvas.set_window_title(mi.subject_name + 
             '-- channel average for ' + averageTitleString)
        fig.suptitle('Channel average for ' + averageTitleString, y=1.0025)

        # Draw a separate plot for each event type
        for index, (eventName, data) in enumerate(dataList):
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

            ca.plot(evokeds[0].times , data)
            ca.set_xlabel('Time (s)')
            ca.set_ylabel(label)
        plt.tight_layout()
        fig.show()

    @threaded
    def _average_channels(self, instance, lobeName, channelSet=None):
        """Performed in a worker thread."""
        if isinstance(instance, str):  # epoch name
            epochs = self.experiment.active_subject.get_epochs(instance)
            if epochs is None:
                raise Exception('No epochs found.')

            category = epochs.event_id

            # Creates evoked potentials from the given events (variable 'name' 
            # refers to different categories).
            #log mne call
            #self.log_action(epochs.average, category)
            evokeds = [epochs[name].average() for name in category.keys()]
        elif isinstance(instance, mne.Evoked):
            evokeds = [instance]
        elif isinstance(instance, list) or isinstance(instance, np.ndarray):
            evokeds = instance

        if channelSet is None:
            channelsToAve = wrap_mne_call(self.experiment, mne.selection.read_selection, lobeName)
            averageTitle = lobeName
        else:
            if any([
                not isinstance(channelSet, set),
                len(channelSet) < 1,
                not channelSet.issubset(set(evokeds[0].ch_names))
            ]):
                raise ValueError('Please check that you have at least '
                                 'one channel, the channels are '
                                 'actual channels in the epochs data '
                                 'and they are in the right form.')
            channelsToAve = channelSet
            averageTitle = str(channelSet).strip('[]')

        averageTitleString = str(averageTitle)
        # Channel names in Evoked objects may or may not have whitespaces
        # depending on the measurements settings,
        # need to check and adjust channelsToAve accordingly.
        channelNameString = evokeds[0].info['ch_names'][0]
        if re.match("^MEG[0-9]+", channelNameString):
            channelsToAve = _clean_names(channelsToAve, remove_whitespace=True)

        # Picks only the desired channels from the evokeds.
        evokedToAve = wrap_mne_call(self.experiment,
                                    mne.pick_channels_evoked, evokeds[0],
                                    list(channelsToAve))

        # TODO: log something from below?
        # Returns channel indices for grad channel pairs in evokedToAve.
        ch_names = evokedToAve.ch_names
        gradsIdxs = _pair_grad_sensors_from_ch_names(ch_names)

        magsIdxs = mne.pick_channels_regexp(ch_names, regexp='MEG.{3,4}1$')

        # eegIdxs = mne.pick_channels_regexp(ch_names, regexp='EEG.{3,4}')
        eeg_picks = mne.pick_types(evokeds[0].info, meg=False, eeg=True,
                                   ref_meg=False)
        eegIdxs = [ch_names.index(evokeds[0].ch_names[idx]) for idx in
                   eeg_picks if evokeds[0].ch_names[idx] in ch_names]
        dataList = list()
        for i in range(len(evokeds)):
            print "Calculating channel averages for " + averageTitleString

            # Merges the grad channel pairs in evokedToAve
            # evokedToChannelAve = mne.fiff.evoked.Evoked(None)
            if len(gradsIdxs) > 0:
                gradData = _merge_grad_data(evokedToAve.data[gradsIdxs])

                # Averages the gradData
                averagedGradData = np.mean(gradData, axis=0)

                # Links the event name and the corresponding data
                dataList.append((evokeds[i].comment + '_grad',
                                 averagedGradData))
            elif len(ch_names) == 1 and re.compile('MEG.{3,4}[23]$').match(ch_names[0]):
                dataList.append((evokeds[i].comment + '_grad',
                                 evokedToAve.data[0]))
            if len(magsIdxs) > 0:
                mag_data = list()
                for idx in magsIdxs:
                    mag_data.append(evokedToAve.data[idx])
                averagedMagData = np.mean(mag_data, axis=0)
                dataList.append((evokeds[i].comment + '_mag', averagedMagData))
            if len(eegIdxs) > 0:
                eeg_data = list()
                for idx in eegIdxs:
                    eeg_data.append(evokedToAve.data[idx])
                averagedEegData = np.mean(eeg_data, axis=0)
                dataList.append((evokeds[i].comment + '_eeg', averagedEegData))

        return averageTitleString, dataList, evokeds

    @messaged
    def plot_group_average(self, groups, layout):
        """
        Plots group average of all subjects in the experiment. Also saves group
        average data to ``output`` folder.
        Keyword arguments:
        groups        -- A list of group names.
        layout        -- Layout used for plotting channels.
        """

        try:
            evokeds, groups = self._group_average(
                groups,
                do_meanwhile=self.parent.update_ui
            )
        except Warning as e:
            QtGui.QApplication.restoreOverrideCursor()
            reply = QtGui.QMessageBox.question(
                self.parent, 
                "Evoked responses not found",
                "Evoked responses not found from every subject. "
                "Draw the evoked potentials anyway?",
                QtGui.QMessageBox.Yes,
                QtGui.QMessageBox.No
            )
            if reply == QtGui.QMessageBox.No:
                return
            else:
                QtGui.QApplication.setOverrideCursor(
                    QtGui.QCursor(QtCore.Qt.WaitCursor))
                evokeds, groups = self._group_average(
                    groups,
                    ignore_not_found=True,
                    do_meanwhile=self.parent.update_ui
                )

        print "Plotting evoked..."
        self.parent.update_ui()
        self.draw_evoked_potentials(evokeds, layout)

    @threaded
    def _group_average(self, groups, ignore_not_found=False):
        """Performed in a worker thread."""
        # TODO: log something?
        chs = self.experiment.active_subject.working_file.info['ch_names']
        chs = _clean_names(chs)
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
            files = [ f for f in listdir(directory)\
                      if isfile(join(directory, f)) and f.endswith('.fif') ]
            for f in files:
                fgroups = re.split('[\[\]]', f)  # '1-2-3'
                if not len(fgroups) == 3: 
                    continue 
                fgroups = re.split('[-]', fgroups[1])  # ['1','2','3']
                if sorted(fgroups) == sorted(groups):
                    files2ave.append(directory + '/' + f)

        print "Found " + str(len(files2ave)) + " subjects with evoked " + \
                        "responses labeled: " + str(groups)
        if len(files2ave) < len(subjects) and not ignore_not_found:
            raise Warning(" ".join([
                "Found only", str(len(files2ave)),
                "subjects of", str(len(subjects)),
                "with evoked responses labeled:",
                str(groups)
            ]))

        evokedTmin = 0
        evokedInfo = []
        for f in files2ave:
            for group in groups:
                evoked = mne.read_evokeds(f, condition=group)
                evokedTmin = evoked.first / evoked.info['sfreq']
                evokedInfo = evoked.info

                info = evoked.info['ch_names']
                info = _clean_names(info)
                for cidx in xrange(len(info)):
                    ch_name = info[cidx]
                    if not ch_name in evokeds[group].keys():
                        raise KeyError('%s not in channels. Make sure all '
                                       'data sets contain the same channel '
                                       'info.' % ch_name)

                    evokeds[group][ch_name].append(evoked.data[cidx])
                eweights[group].append(evoked.nave)

        evs = []
        usedChannels = []
        bads = []
        for group in groups:
            max_key = max(evokeds[group],
                          key=lambda x: len(evokeds[group][x]))
            length = len(evokeds[group][max_key])
            evokedSet = []
            for ch in chs:
                if len(evokeds[group][ch]) < length:
                    if not ch in bads: 
                        bads.append(ch)
                    continue

                if not ch in usedChannels: 
                    usedChannels.append(ch)
                data = evokeds[group][ch]
                w = eweights[group]
                epoch_length = len(data[0])
                for d in data:
                    if not len(d) == epoch_length:
                        raise Exception("Epochs are different " +
                                        "in sizes!")
                ave = np.average(data, axis=0, weights=w)
                evokedSet.append(ave)

            evs.append(deepcopy(evokedSet))

        print 'Used channels: ' + str(usedChannels)
        print '\nBad channels: ' + str(bads)
        evokedInfo['ch_names'] = usedChannels
        evokedInfo['chs'] = [ch for ch in evokedInfo['chs']
                             if ch['ch_name'] in usedChannels]
        evokedInfo['bads'] = []
        evokedInfo['nchan'] = len(usedChannels)

        averagedEvokeds = []
        for groupidx in xrange(len(groups)):
            averagedEvokeds.append(mne.EvokedArray(evs[groupidx],
                                                   info=evokedInfo,
                                                   tmin=evokedTmin,
                                                   comment=groups
                                                   [groupidx]))

        write2file = True
        if write2file:  # TODO add option in GUI for this
            exp_path = os.path.join(self.experiment.workspace,
                                    self.experiment.experiment_name)
            if not os.path.isdir(exp_path + '/output'):
                os.mkdir(exp_path + '/output')
            fName = '-'.join(groups) + '_group_average.txt'
            fName = exp_path + '/output/' + fName
            print 'Saving averages in ' + fName
            f = open(fName, 'w')
            f.write('Times, ')
            for time in averagedEvokeds[0].times:
                f.write(repr(time))
                f.write(', ')
            f.write('\n')
            i = 0
            for evoked in averagedEvokeds:
                f.write(repr(groups[i]))
                f.write('\n')
                i = i + 1
                for ch_idx in xrange(len(evoked.ch_names)):
                    f.write(repr(evoked.ch_names[ch_idx] + ', '))
                    for j in xrange(len(evoked.data[ch_idx])):
                        f.write(repr(evoked.data[ch_idx][j]))
                        f.write(', ')
                    f.write('\n')
            f.close()

        return averagedEvokeds, groups

    @messaged
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
        frequencies = np.arange(minfreq, maxfreq, interval)
        
        result = self._TFR(epochs, ch_index, frequencies, ncycles, decim,
                           do_meanwhile=self.parent.update_ui)
        power, phase_lock, times, evoked, evoked_data = result

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

        plt.plot(times, evoked_data.T)
        plt.title('Evoked response (%s)' % evoked.ch_names[ch_index])
        plt.xlabel('time (ms)')
        plt.xlim(times[0], times[-1])

        plt.subplot2grid((3, 15), (1, 0), colspan=14)
        if color_map == 'auto':
            cmap = 'RdBu_r' if np.min(power[0] < 0) else 'Reds'
        else:
            cmap = color_map

        img = plt.imshow(power[0], extent=[times[0], times[-1],
                                           frequencies[0], frequencies[-1]],
                         aspect='auto', origin='lower', cmap=cmap)
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Induced power (%s)' % evoked.ch_names[ch_index])
        plt.colorbar(cax=plt.subplot2grid((3, 15), (1, 14)), mappable=img)
        if color_map == 'auto':
            cmap = 'RdBu_r' if np.min(phase_lock[0] < 0) else 'Reds'
        plt.subplot2grid((3, 15), (2, 0), colspan=14)
        img = plt.imshow(phase_lock[0], extent=[times[0], times[-1],
                                                frequencies[0],
                                                frequencies[-1]],
                         aspect='auto', origin='lower', cmap=cmap)
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Phase-lock (%s)' % evoked.ch_names[ch_index])
        plt.colorbar(cax=plt.subplot2grid((3, 15), (2, 14)), mappable=img)

        plt.tight_layout()
        fig.show()

    @threaded
    def _TFR(self, epochs, ch_index, frequencies, ncycles, decim):
        """
        Performed in a worker thread.
        """
        print 'Computing induced power...'
        evoked = epochs.average()
        data = epochs.get_data()
        times = 1e3 * epochs.times  # s to ms
        evoked_data = evoked.data

        data = data[:, ch_index:(ch_index+1), :]
        evoked_data = evoked_data[ch_index:(ch_index+1), :]

        power, itc = wrap_mne_call(self.experiment, _induced_power_cwt,
                                   data, epochs.info['sfreq'], frequencies,
                                   n_cycles=ncycles, decim=decim,
                                   use_fft=False, n_jobs=1, zero_mean=True)

        if epochs.times[0] < 0:
            baseline = (epochs.times[0], 0)
        else:
            baseline = None
        # TODO: log mne call
        power = mne.baseline.rescale(power, epochs.times[::decim], baseline,
                                     mode='ratio', copy=True)
        # TODO: log mne call
        itc = mne.baseline.rescale(itc, epochs.times[::decim], baseline,
                                   mode='ratio', copy=True)
        return power, itc, times, evoked, evoked_data

    @messaged
    def TFR_topology(self, inst, reptype, minfreq, maxfreq, decim, mode,  
                     blstart, blend, interval, ncycles, lout, ch_type, scalp,
                     color_map='auto'):
        """
        Plots time-frequency representations on topographies for MEG sensors.
        Modified from example by Alexandre Gramfort and Denis Engemann.
        Keyword arguments:
        inst          -- Epochs extracted from the data or previously computed
                         AverageTFR object to plot.
        reptype       -- Type of representation (average or itc).
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
        ch_type       -- Channel type (mag | grad | eeg).
        scalp         -- Parameter dictionary for scalp plot. If None, no scalp
                         plot is drawn.
        color_map     -- Matplotlib color map to use. Defaults to ``auto``, in
                         which case ``RdBu_r`` is used or ``Reds`` if only
                         positive values exist in the data.
        """

        plt.close()
        if isinstance(inst, mne.epochs._BaseEpochs):  # TFR from epochs
    
            # Find intervals for given frequency band
            frequencies = np.arange(minfreq, maxfreq, interval)
    
            power, itc = self._TFR_topology(
                inst, frequencies, ncycles,
                decim, do_meanwhile=self.parent.update_ui
            )

        elif reptype == 'average':  # TFR from averageTFR
            power = inst
        elif reptype == 'itc':  # TFR from averageTFR
            itc = inst

        if lout == 'Infer from data':
            layout = None
        else:
            layout = read_layout(lout)
        
        if blstart is None and blend is None:
            baseline = None
        else:
            baseline = (blstart, blend)

        print "Plotting..."
        self.parent.update_ui()
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
            self.parent.update_ui()
           
            fig = wrap_mne_call(self.experiment, power.plot_topo,
                                            baseline=baseline, mode=mode, fmin=minfreq,
                                            fmax=maxfreq, layout=layout, cmap=cmap,
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
                                baseline=baseline, mode=mode, fmin=minfreq,
                                fmax=maxfreq, layout=layout, cmap=cmap,
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
        power, itc = wrap_mne_call(self.experiment, tfr_morlet, epochs,
                                   freqs=frequencies, n_cycles=ncycles,
                                   use_fft=False, return_itc=True,
                                   decim=decim, n_jobs=3)

        tfr_path = os.path.join(self.experiment.active_subject.subject_path,
                                'TFR')
        if not os.path.isdir(tfr_path):
            os.mkdir(tfr_path)
        print 'Saving files to %s...' % tfr_path
        # TODO: log mne call
        power.save(os.path.join(tfr_path, 'power-tfr-' + epochs.name + '.h5'),
                   overwrite=True)
        # TODO: log mne call
        itc.save(os.path.join(tfr_path, 'itc-tfr-' + epochs.name + '.h5'),
                 overwrite=True)
        return power, itc

    @messaged
    def TFR_average(self, epochs_name, reptype, color_map, mode, minfreq,
                    maxfreq, interval, blstart, blend, ncycles, decim, layout,
                    selected_channels, form, dpi, save_topo, save_plot,
                    save_max):
        """
        Method for computing average TFR over all subjects in the experiment.
        Creates data and picture files to output folder of the experiment.
        """
        if layout == 'Infer from data':
            layout = None
        else:
            layout = read_layout(layout)

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
        chs = self.experiment.active_subject.working_file.info['ch_names']
        subjects = self.experiment.get_subjects()
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
            power, itc = wrap_mne_call(self.experiment, tfr_morlet, epochs,
                                       freqs=frequencies, n_cycles=ncycles,
                                       use_fft=False, return_itc=True,
                                       decim=decim, n_jobs=3)

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

    @messaged
    def plot_power_spectrum(self, params, save_data, colors, channelColors):
        """
        Method for plotting power spectrum.
        Parameters:
        params         - Dictionary containing the parameters.
        save_data      - Boolean indicating whether to save psd data to files.
                         Only data from channels of interest is saved.
        colors         - List of default colors. One for each time series.
        channelColors  - Dictionary of channel specific colors. Keys are
                         indices of the time series (starting from zero). The
                         values are tuple of (color, list of channels of
                         interest).
        """
        if params['lout'] == 'Infer from data':
            lout = None
        else:
            try:
                lout = read_layout(params['lout'], scale=True)
            except Exception:
                message = 'Could not read layout information.'
                raise Exception(message)
        raw = self.experiment.active_subject.working_file

        if params['ch'] == 'meg':
            picks = mne.pick_types(raw.info, meg=True, eeg=False,
                                   exclude=[])
        elif params['ch'] == 'eeg':
            picks = mne.pick_types(raw.info, meg=False, eeg=True,
                                   exclude=[])
        params['picks'] = picks

        psds = self._compute_spectrum(raw, params,
                                      do_meanwhile=self.parent.update_ui)

        if save_data:
            print 'Writing to file...'
            exp_path = os.path.join(self.experiment.workspace,
                                    self.experiment.experiment_name)
            if not os.path.isdir(exp_path + '/output'):
                os.mkdir(exp_path + '/output')
            fname = os.path.join(exp_path + '/output',
                                 self.experiment.active_subject.subject_name + 
                                 '_spectrum.txt')
            f = open(fname, 'w')
            f.write('freqs, ')
            for freq in psds[0][1]:
                f.write(str(freq) + ', ')
            for idx, time in enumerate(params['times']):
                f.write('\n' + str(time[0]) + 's to ' + str(time[1]) + 's\n')
                for ch_name in channelColors[idx][1]:
                    f.write(ch_name + ', ')
                    ch_idx = raw.ch_names.index(ch_name)
                    for psd in psds[idx][0][ch_idx]:
                        f.write(str(psd) + ', ')
                    f.write('\n')
            f.close()

        print "Plotting power spectrum..."

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

        info = deepcopy(raw.info)

        info['ch_names'] = [ch for idx, ch in enumerate(info['ch_names'])
                            if idx in picks]

        for ax, idx in iter_topography(info, fig_facecolor='white',
                                       axis_spinecolor='white',
                                       axis_facecolor='white', layout=lout,
                                       on_pick=my_callback):
            for i in xrange(len(psds)):
                channel = info['ch_names'][idx]
                if (channel in channelColors[i][1]):
                    ax.plot(psds[i][0][idx], color=channelColors[i][0],
                            linewidth=0.2)
                else:
                    ax.plot(psds[i][0][idx], color=colors[i], linewidth=0.2)
        plt.show()

    @threaded
    def _compute_spectrum(self, raw, params):
        """Performed in a worker thread."""
        times = params['times']
        fmin = params['fmin']
        fmax = params['fmax']
        nfft = params['nfft']
        overlap = params['overlap']
        picks = params['picks']

        psdList = []
        for time in times:
            psds, freqs = wrap_mne_call(self.experiment, compute_raw_psd,
                                        raw, tmin=time[0], tmax=time[1],
                                        fmin=fmin, fmax=fmax, n_fft=nfft,
                                        n_overlap=overlap, picks=picks,
                                        proj=True, verbose=True)
            if params['log']:
                psds = 10 * np.log10(psds)
            psdList.append((psds, freqs))
        return psdList

    @messaged
    @threaded
    def filter(self, dataToFilter, info, dic):
        """
        Filters the data array in place according to parameters in paramDict.
        Depending on the parameters, the filter is one or more of
        lowpass, highpass and bandstop (notch) filter.

        Keyword arguments:

        dataToFilter         -- array of data to filter or a raw object
        info                 -- info for the data file to filter
        dic                  -- Dictionary with filtering parameters

        Returns the filtered array.
        """
        return self._filter(dataToFilter, info, dic)

    def _filter(self, dataToFilter, info, dic):
        """Performed in a working thread."""
        sf = info['sfreq']

        if isinstance(dataToFilter, mne.io.Raw):
            hfreq = dic['low_cutoff_freq'] if dic['lowpass'] else None
            lfreq = dic['high_cutoff_freq'] if dic['highpass'] else None
            length = dic['length']
            trans_bw = dic['trans_bw']

            print "Filtering..."
            wrap_mne_call(self.experiment, dataToFilter.filter,
                          l_freq=lfreq, h_freq=hfreq, filter_length=length,
                          l_trans_bandwidth=trans_bw,
                          h_trans_bandwidth=trans_bw, n_jobs=2,
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
                              trans_bandwidth=trans_bw, n_jobs=2,
                              verbose=True)
            print 'Saving to file...'
            fileManager.save_raw(self.experiment, dataToFilter, info['filename'], overwrite=True)
        else:  # preview
            picks = mne.pick_types(info, meg=True, eeg=True)
            if dic.get('lowpass'):
                print "Low-pass filtering..."

                dataToFilter = wrap_mne_call(self.experiment,
                                             low_pass_filter, dataToFilter,
                                             sf,
                                             dic.get('low_cutoff_freq'),
                                             dic.get('length'),
                                             dic.get('trans_bw'), 'fft',
                                             None, picks=picks, n_jobs=2,
                                             copy=True)

            if dic.get('highpass') == True:
                print "High-pass filtering..."
                dataToFilter = wrap_mne_call(self.experiment,
                                             high_pass_filter,
                                             dataToFilter, sf,
                                             dic['high_cutoff_freq'],
                                             dic.get('length'),
                                             dic.get('trans_bw'), 'fft',
                                             None, picks=picks, n_jobs=2,
                                             copy=True)

            trans = dic['bandstop_transbw']
            if dic.get('bandstop1') == True:
                lfreq = dic['bandstop1_freq'] - dic['bandstop_bw'] / 2.
                hfreq = dic['bandstop1_freq'] + dic['bandstop_bw'] / 2.
                print "Band-stop filtering..."
                dataToFilter = wrap_mne_call(self.experiment,
                                             band_stop_filter,
                                             dataToFilter, sf, lfreq,
                                             hfreq, dic['bandstop_length'],
                                             trans, trans, picks=picks,
                                             n_jobs=2, copy=True)

            if dic.get('bandstop2') == True:
                lfreq = dic['bandstop2_freq'] - dic['bandstop_bw'] / 2.
                hfreq = dic['bandstop2_freq'] + dic['bandstop_bw'] / 2.
                print "Band-stop filtering..."
                dataToFilter = wrap_mne_call(self.experiment,
                                             band_stop_filter,
                                             dataToFilter, sf, lfreq,
                                             hfreq, dic['bandstop_length'],
                                             trans, trans, picks=picks,
                                             n_jobs=2, copy=True)

        return dataToFilter

### Methods needed for source modeling ###    

    @messaged
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

    @messaged
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
        
        if reply == 'computeAll':
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
                               self.experiment._working_file_names
                               [self.experiment._active_subject_name])

        mne.gui.coregistration(tabbed=True, split=True, scene_width=300,
                               raw=rawPath, subject=subject,
                               subjects_dir=subjects_dir)
        QtCore.QCoreApplication.processEvents()

        # Needed for copying the resulting trans file to the right location.
        self.coregHowtoDialog = holdCoregistrationDialog(self, activeSubject,
                                                         selectedFmodelName) 
        self.coregHowtoDialog.ui.labelTransFileWarning.hide()
        self.coregHowtoDialog.show()

    @messaged
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

        targetFileName = os.path.join(fmdir, 'reconFiles',
                                      'reconFiles-fwd.fif')

        try:
            mne.make_forward_solution(rawInfo, transFilePath, srcFilePath,
                                      bemSolFilePath, targetFileName,
                                      fsdict['includeMEG'],
                                      fsdict['includeEEG'], fsdict['mindist'],
                                      fsdict['ignoreref'], True,
                                      fsdict['njobs'])
            fileManager.write_forward_solution_parameters(fmdir, fsdict)
            self.parent.forwardModelModel.initialize_model()
        except Exception as e:
            title = 'Error'
            msg = ('There was a problem with forward solution. The MNE-Python '
                   'message was: \n\n' + str(e))
            raise Exception(msg)

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
            if subjectName is not None:
                if subjectName == self.experiment.active_subject_name:
                    fileNameToWrite = subjectName + '-cov.fif'
                    raw = self.experiment.active_subject.working_file
                else:
                    fileNameToWrite = subjectName + '-cov.fif'
                    raw = self.experiment.get_subject_working_file(subjectName)
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

        path = self.experiment.active_subject._source_analysis_directory

        # Remove previous covariance file before creating a new one.
        fileManager.remove_files_with_regex(path, '.*-cov.fif')

        filePathToWrite = os.path.join(path, fileNameToWrite)
        try:
            mne.write_cov(filePathToWrite, cov)
        except IOError as err:
            err.message = ('Could not write covariance file. The error '
                           'message was: \n\n' + err.message)
            raise

        # Delete previous and write a new parameter file.
        try:
            fileManager.remove_files_with_regex(path, 'covariance.param')
            cvparamFile = os.path.join(path, 'covariance.param')
            fileManager.pickleObjectToFile(cvdict, cvparamFile)

        except Exception:
            fileManager.remove_files_with_regex(path, '*-cov.fif')
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
        status = "Current working file: " + os.path.basename(self.experiment.active_subject_raw_path)
        self.parent.statusLabel.setText(status)
        
    def log_action(self, mne_func, *args, **kwargs):
        """
        Helper method for logging
        
        Keyword arguments:
        TODO: outcome     - string interpreting the successfulness of the action
        mne_func    - reference to mne function (or class in some cases)
        args        - arguments passed to the mne function (or class)
        kwargs      - keyword arguments passed to the mne function (or class)
        """
        #wrapper.wrap_mne_call(self.experiment.action_logger, mne_func, *args, **kwargs)
        
    def log_raw_changed(self, fname):
        self.experiment.action_logger.log_message('Raw changed: ' + fname)
