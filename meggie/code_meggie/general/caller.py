# coding: utf-8
"""
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen, Erkka Heinilä
"""

import itertools
import os
import re
import copy
import logging

from os.path import join
from copy import deepcopy

from functools import partial
from collections import OrderedDict

from PyQt4 import QtGui

import numpy as np
import matplotlib.pyplot as plt

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.ui.utils.decorators import threaded
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.epoching.events import Events
from meggie.code_meggie.general.singleton import Singleton
from meggie.code_meggie.utils.units import get_scaling
from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.utils.units import get_power_unit


@Singleton
class Caller(object):
    """
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

        reject = {
            'grad': float(rej_grad) / get_scaling('grad'), 
            'mag': float(rej_mag) / get_scaling('mag'),
            'eeg': float(rej_eeg) / get_scaling('eeg'), 
            'eog': float(rej_eog) / get_scaling('eog'),
        }

        qrs_threshold = dic.get('qrs')
        start = dic.get('tstart')
        taps = dic.get('filtersize')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        ch_name = dic.get('ch_name')

        prefix = os.path.join(subject.subject_path, subject.subject_name)

        ecg_event_fname = prefix + '_ecg-eve.fif'

        if comp_ssp:
            ecg_proj_fname = prefix + '_ecg_avg_proj.fif'
        else:
            ecg_proj_fname = prefix + '_ecg_proj.fif'

        # To avoid casualities
        n_jobs = 1
        projs, events = mne.compute_proj_ecg(raw=raw_in, tmin=tmin, tmax=tmax,
            n_grad=grad, n_mag=mag, n_eeg=eeg, l_freq=filter_low, 
            h_freq=filter_high, average=comp_ssp, filter_length=taps, 
            n_jobs=n_jobs, ch_name=ch_name, reject=reject,
            no_proj=excl_ssp, ecg_l_freq=ecg_low_freq,
            ecg_h_freq=ecg_high_freq, tstart=start, qrs_threshold=qrs_threshold)

        if not projs:
            raise Exception('No ECG events found. Change settings.')

        message = "Writing ECG projections in %s" % ecg_proj_fname
        logging.getLogger('ui_logger').info(message)
        mne.write_proj(ecg_proj_fname, projs)

        message = "Writing ECG events in %s" % ecg_event_fname
        logging.getLogger('ui_logger').info(message)
        mne.write_events(ecg_event_fname, events)

    def plot_ecg_events(self, params):
        raw = self.experiment.active_subject.get_working_file()
        
        events, _, _ = find_ecg_events(raw,
            ch_name=params['ch_name'], event_id=1, l_freq=params['ecg-l-freq'],
            h_freq=params['ecg-h-freq'], tstart=params['tstart'],
            qrs_threshold=params['qrs'], filter_length=params['filtersize'])
        
        picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False,
            eog=False, include=[params['ch_name']])
        epochs = mne.Epochs(raw, events=events, event_id=1,
            tmin=params['tmin'], tmax=params['tmax'], picks=picks, proj=False)
        
        data = epochs.get_data()
        message = "Number of detected ECG artifacts : %d" % len(data)
        logging.getLogger('ui_logger').info(message)
        
        plt.plot(1e3 * epochs.times, np.squeeze(data).T)
        plt.xlabel('Times (ms)')
        plt.ylabel('ECG')
        subject_name = self.experiment.active_subject.subject_name
        plt.gcf().canvas.set_window_title('_'.join(['ECG_events', subject_name,
                                                    params['ch_name']]))
        plt.show()

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

        start = dic.get('tstart')
        taps = dic.get('filtersize')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        reject = {
            'grad': float(rej_grad) / get_scaling('grad'), 
            'mag': float(rej_mag) / get_scaling('mag'),
            'eeg': float(rej_eeg) / get_scaling('eeg'), 
            'eog': float(rej_eog) / get_scaling('eog'),
        }

        prefix = os.path.join(subject.subject_path, subject.subject_name) 
        eog_event_fname = prefix + '_eog-eve.fif'

        if comp_ssp:
            eog_proj_fname = prefix + '_eog_avg_proj.fif'
        else:
            eog_proj_fname = prefix + '_eog_proj.fif'

        # To avoid casualities
        n_jobs = 1        
        projs, events = mne.compute_proj_eog(raw=raw_in, tmin=tmin, tmax=tmax,
            n_grad=grad, n_mag=mag, n_eeg=eeg, l_freq=filter_low, 
            h_freq=filter_high, average=comp_ssp, filter_length=taps, 
            n_jobs=n_jobs, reject=reject, no_proj=excl_ssp, 
            eog_l_freq=eog_low_freq, eog_h_freq=eog_high_freq, tstart=start)

        message = "Writing EOG projections in %s" % eog_proj_fname
        logging.getLogger('ui_logger').info(message)
        mne.write_proj( eog_proj_fname, projs)

        message = "Writing EOG events in %s" % eog_event_fname
        logging.getLogger('ui_logger').info(message)
        mne.write_events(eog_event_fname, events)

    def plot_eog_events(self, params):
        raw = self.experiment.active_subject.get_working_file()
        
        picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False,
            eog=True)

        try:
            ch_name = [ch_name for idx, ch_name 
                       in enumerate(raw.info['ch_names']) if idx in picks][0]
        except IndexError:
            raise Exception("No EOG channel found")

        events = mne.find_eog_events(raw, event_id=1, 
            l_freq=params['eog-l-freq'], h_freq=params['eog-h-freq'], 
            filter_length=params['filtersize'], ch_name=ch_name, 
            tstart=params['tstart'])

        epochs = mne.Epochs(raw, events=events, event_id=1,
            tmin=params['tmin'], tmax=params['tmax'], picks=picks, proj=False)
        
        data = epochs.get_data()

        message = "Number of detected EOG artifacts : %d" % len(data)
        logging.getLogger('ui_logger').info(message)
        
        plt.plot(1e3 * epochs.times, np.squeeze(data).T)
        plt.xlabel('Times (ms)')
        plt.ylabel('EOG')
        subject_name = self.experiment.active_subject.subject_name
        plt.gcf().canvas.set_window_title('EOG_events_' + subject_name)
        plt.show()


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
        
        eog_epochs = mne.Epochs(raw, events, tmin=tmin, tmax=tmax)
        
        
        eog_evoked = eog_epochs.average()
        
        # Compute SSPs
        projs = mne.compute_proj_evoked(eog_evoked, n_eeg=n_eeg)

        prefix = os.path.join(subject.subject_path, subject.subject_name) 
        eeg_event_fname = prefix + '_eeg-eve.fif'
        eeg_proj_fname = prefix + '_eeg_proj.fif'
        
        message = "Writing ocular projections in %s" % eeg_proj_fname
        logging.getLogger('ui_logger').info(message) 
        mne.write_proj(eeg_proj_fname, projs)

        message = "Writing ocular events in %s" % eeg_event_fname
        logging.getLogger('ui_logger').info(message) 
        mne.write_events(eeg_event_fname, events)

    def plot_average_epochs(self, events, tmin, tmax):
        """
        Method for plotting average epochs.
        """
        raw = self.experiment.active_subject.get_working_file()
        logging.getLogger('ui_logger').info("Plotting averages...")
        eog_epochs = mne.Epochs(raw, events,
                        tmin=tmin, tmax=tmax)
        
        # Average EOG epochs
        eog_evoked = eog_epochs.average()
        fig = eog_evoked.plot()
        subject_name = self.experiment.active_subject.subject_name
        fig.canvas.set_window_title('avg_epochs_' + subject_name)

    def plot_events(self, events):
        """
        Method for plotting the event locations in mne_browse_raw.
        Parameters:
        events - A list of events
        """
        raw = self.experiment.active_subject.get_working_file()

        logging.getLogger('ui_logger').info("Plotting events...")
        raw.plot(events=events, scalings=dict(eeg=40e-6))
        plt.show()

    def plot_projs_topomap(self, raw):
        fig = raw.plot_projs_topomap()
        name = self.experiment.active_subject.subject_name
        fig.canvas.set_window_title('Projections_' + name)

    @threaded
    def find_eog_events(self, params):
        raw = self.experiment.active_subject.get_working_file()
        eog_events = mne.find_eog_events(raw, l_freq=params['l_freq'], 
            h_freq=params['h_freq'], filter_length=params['filter_length'],
            ch_name=params['ch_name'], tstart=params['tstart'])
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

        # convert data from human readable units to standard units
        for key in ['grad', 'mag', 'eog', 'eeg']:
            if key in reject_data:
                reject_data[key] /= get_scaling(key)
        
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
                events.extend(mne.make_fixed_length_events(raw, 
                    event_params_dic['event_id'],
                    event_params_dic['tmin'],
                    event_params_dic['tmax'], 
                    event_params_dic['interval']
                ))
                event_id_counter += 1

        if len(events) == 0:
            raise ValueError('Could not create epochs for subject: No events found with given params.')

        if not isinstance(raw, mne.RAW_TYPE):
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

        epochs = mne.Epochs(raw, np.array(events), 
            category, params_copy['tmin'], params_copy['tmax'], 
            picks=picks, reject=params_copy['reject'])
            
        if len(epochs.get_data()) == 0:
            raise ValueError('Could not find any data. Perhaps the ' + 
                             'rejection thresholds are too strict...')
        
        epochs_object = Epochs(params['collection_name'], subject, params, epochs)
        fileManager.save_epoch(epochs_object, overwrite=True)
        subject.add_epochs(epochs_object)
        
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
        e = Events(self.experiment, raw, stim_channel, params['mask'], params['event_id'])

        return e.events

    def read_layout(self, layout):
        if not layout or layout == "Infer from data":
            return None
        
        import pkg_resources
        path_mne = pkg_resources.resource_filename('mne', 'channels/data/layouts')
        path_meggie = pkg_resources.resource_filename('meggie', 'data/layouts')
        
        if os.path.exists(os.path.join(path_mne, layout)):
            return mne.read_layout(layout, path_mne)
        
        if os.path.exists(os.path.join(path_meggie, layout)):
            return mne.read_layout(layout, path_meggie)


    def draw_evoked_potentials(self, evokeds, title=None):
        """
        Draws a topography representation of the evoked potentials.

        """
        layout = self.read_layout(self.experiment.layout)
        colors = self.colors(len(evokeds))

        fig = mne.plot_evoked_topo(evokeds, layout,
            color=colors, title=title, fig_facecolor='w', axis_facecolor='w',
            font_color='k')

        conditions = [e.comment for e in evokeds]
        positions = np.arange(0.025, 0.025 + 0.04 * len(evokeds), 0.04)
                
        for cond, col, pos in zip(conditions, colors, positions):
            plt.figtext(0.775, pos, cond, color=col, fontsize=12)
            
        window_title = '_'.join(conditions)
        fig.canvas.set_window_title(window_title)
        fig.show()
        
        def onclick(event):
            channel = plt.getp(plt.gca(), 'title')
            plt.gcf().canvas.set_window_title('_'.join([window_title, channel]))
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
            title = 'selected set of channels'
        else:
            channels = mne.read_selection(lobeName)
            title = lobeName
            
        message = "Calculating channel averages for " + title
        logging.getLogger('ui_logger').info(message)

        dataList, epochs_name = self._average_channels(
            instance, channels, do_meanwhile=self.parent.update_ui)

        # Plotting:
        plt.clf()
        fig = plt.figure()
        subject_name = self.experiment.active_subject.subject_name
        fig.canvas.set_window_title('_'.join([epochs_name, 
            'channel_avg', title]))
        fig.suptitle('Channel average for ' + title, y=1.0025)

        # Draw a separate plot for each event type
        for index, (times, eventName, data) in enumerate(dataList):
            ca = fig.add_subplot(len(dataList), 1, index + 1) 
            ca.set_title(eventName)

            if eventName.endswith('grad'):
                ch_type = 'grad'
            elif eventName.endswith('mag'):
                ch_type = 'mag'
            elif eventName.endswith('eeg'):
                ch_type = 'eeg'

            label = get_unit(ch_type)
            data *= get_scaling(ch_type)

            ca.plot(times, data)

            ca.set_xlabel('Time (s)')
            ca.set_ylabel(label)

        plt.tight_layout()
        fig.show()

    @threaded
    def _average_channels(self, instance, channelsToAve):
        """Performed in a worker thread."""
        if isinstance(instance, str):  # epoch name
            _epochs = self.experiment.active_subject.epochs.get(instance)
            epochs = _epochs.raw
            epochs_name = _epochs.collection_name
            if epochs is None:
                raise Exception('No epochs found.')
            category = epochs.event_id

            # Creates evoked potentials from the given events (variable 'name' 
            # refers to different categories).
            evokeds = [epochs[name].average() for name in category.keys()]
        elif isinstance(instance, mne.EVOKED_TYPE):
            evokeds = [instance]
            epochs_name = evokeds[0].comment
        elif isinstance(instance, list) or isinstance(instance, np.ndarray):
            evokeds = instance
            epochs_name = 'List_of_epochs'
        # Channel names in Evoked objects may or may not have whitespaces
        # depending on the measurements settings,
        # need to check and adjust channelsToAve accordingly.
        
        channelNameString = evokeds[0].info['ch_names'][0]
        if re.match("^MEG[0-9]+", channelNameString):
            channelsToAve = mne._clean_names(channelsToAve, remove_whitespace=True)

        dataList = []

        for evoked in evokeds:
            evokedToAve = mne.pick_channels_evoked(evoked, list(channelsToAve))

            ch_names = evokedToAve.ch_names
            gradsIdxs = mne._pair_grad_sensors_from_ch_names(ch_names)
    
            magsIdxs = mne.pick_channels_regexp(ch_names, regexp='MEG.{3,4}1$')
    
            eegIdxs = mne.pick_types(evokedToAve.info, meg=False, eeg=True,
                                       ref_meg=False)

            # Merges the grad channel pairs in evokedToAve
            if len(gradsIdxs) > 0:
                gradData = mne._merge_grad_data(evokedToAve.data[gradsIdxs])

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

        return dataList, epochs_name

    def group_average(self, evoked_name):
        """
        Plots group average of all subjects in the experiment. 
        average data to ``output`` folder.
        Keyword arguments:
        evoked_name        -- name of the evoked objects
        """
        count = 0
        group_info = {}
        for subject in self.experiment.subjects.values():
            if subject.evokeds.get(evoked_name):
                count += 1
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

        return evokeds, group_info

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

    def TFR(self, epochs, collection_name, ch_index, freqs, ncycles, decim,
            mode, blstart, blend, save_data, color_map='auto'):
        """
        Plots a time-frequency representation of the data for a selected
        channel. Modified from example by Alexandre Gramfort.
        """

        n_jobs = self.parent.preferencesHandler.n_jobs
        baseline = (blstart, blend)
        
        @threaded
        def calculate_tfrs():
            power, itc = mne.tfr_morlet(epochs, freqs=freqs, n_cycles=ncycles, 
                                        decim=decim, n_jobs=n_jobs)
            evoked = epochs.average()
            return power, itc, evoked
            
        power, itc, evoked = calculate_tfrs()
        
        if mode:
            power.data = mne.rescale(power.data, power.times, 
                baseline=baseline, mode=mode)
            itc.data = mne.rescale(itc.data, itc.times, 
                baseline=baseline, mode=mode)          
        
        ch_name = power.ch_names[ch_index]
        
        if save_data:

            subject = self.experiment.active_subject.subject_name
            path = fileManager.create_timestamped_folder(self.experiment)
            ch_name = power.ch_names[ch_index]

            power_fname = os.path.join(
                path,
                subject + '_' + ch_name + '_TFR_epochs_induced.csv'
            )

            fileManager.save_tfr(power_fname, power.data[ch_index], power.times, freqs)

            itc_fname = os.path.join(
                path,
                subject + '_' + ch_name + '_TFR_epochs_itc.csv'
            )

            fileManager.save_tfr(itc_fname, itc.data[ch_index], itc.times, freqs)

        evoked_data = evoked.data[ch_index]
        evoked_times = 1e3 * evoked.times

        logging.getLogger('ui_logger').info('Plotting TFR.')
        fig = plt.figure()

        plt.subplot2grid((3, 15), (0, 0), colspan=14)

        ch_type = mne.channel_type(evoked.info, ch_index)

        try:
            plt.ylabel(get_unit(ch_type))
            evoked_data *= get_scaling(ch_type)
        except:
            raise TypeError('TFR plotting for %s channels not supported.' % 
                            ch_type)

        plt.plot(evoked_times, evoked_data)
        plt.title('Evoked response (%s)' % evoked.ch_names[ch_index])
        plt.xlabel('Time (ms)')
        plt.xlim(evoked_times[0], evoked_times[-1])

        if color_map == 'auto':
            cmap = 'RdBu_r'
        else:
            cmap = color_map    

        data = power.data[ch_index]

        plt.subplot2grid((3, 15), (1, 0), colspan=14)
        img = plt.imshow(data, extent=[evoked_times[0], evoked_times[-1],
            freqs[0], freqs[-1]], aspect='auto', origin='lower', cmap=cmap)
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Induced power (%s)' % evoked.ch_names[ch_index])
        plt.colorbar(cax=plt.subplot2grid((3, 15), (1, 14)), mappable=img)

        data = itc.data[ch_index]
            
        plt.subplot2grid((3, 15), (2, 0), colspan=14)
        img = plt.imshow(data, extent=[evoked_times[0], evoked_times[-1],
            freqs[0], freqs[-1]], aspect='auto', origin='lower', cmap=cmap)
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Phase-lock (%s)' % evoked.ch_names[ch_index])
        plt.colorbar(cax=plt.subplot2grid((3, 15), (2, 14)), mappable=img)

        plt.tight_layout()
        fig.canvas.set_window_title('_'.join(['TFR', collection_name,
                                              ch_name]))
        fig.show()


    def TFR_topology(self, inst, collection_name, reptype, freqs, decim, mode, 
                     blstart, blend, ncycles, ch_type, scalp, color_map='auto',
                     save_data=False):
        """
        Plots time-frequency representations on topographies for MEG sensors.
        Modified from example by Alexandre Gramfort and Denis Engemann.
        Keyword arguments:
        inst            -- Epochs extracted from the data or previously computed
                           AverageTFR object to plot.
        collection_name -- Name of the epoch collection.
        reptype         -- Type of representation (average or itc).
        freqs           -- Frequencies for the representation as a numpy array.
        decim           -- Temporal decimation factor.
        mode            -- Rescaling mode (logratio | ratio | zscore |
                           mean | percent).
        blstart         -- Starting point for baseline correction.
        blend           -- Ending point for baseline correction.
        ncycles         -- Value used to count the number of cycles.
        ch_type         -- Channel type (mag | grad | eeg).
        scalp           -- Parameter dictionary for scalp plot. If None, no scalp
                           plot is drawn.
        color_map       -- Matplotlib color map to use. Defaults to ``auto``, in
                           which case ``RdBu_r`` is used or ``Reds`` if only
                           positive values exist in the data.
        save_data       -- save data to file or not
        """

        @threaded
        def calculate_tfrs():
            n_jobs = self.parent.preferencesHandler.n_jobs
            power, itc = mne.tfr_morlet(inst, freqs=freqs, n_cycles=ncycles, 
                                        decim=decim, n_jobs=n_jobs)
            return power, itc
        
        power, itc = calculate_tfrs()
        baseline = (blstart, blend)
        layout = self.read_layout(self.experiment.layout)
                
        if reptype == 'average':
            inst = power
            title = 'Average power'
        elif reptype == 'itc':
            inst = itc
            title = 'Inter-trial coherence'
            
        if color_map == 'auto':
            cmap = 'RdBu_r'
        else:
            cmap = color_map

        if mode:
            inst.data = mne.rescale(inst.data, inst.times, 
                baseline=baseline, mode=mode)    

        if save_data:
            subject = self.experiment.active_subject.subject_name
            path = fileManager.create_timestamped_folder(self.experiment)

            fname = os.path.join(
                path,
                subject + '_TFR_epochs_allchannels.csv'
            )

            labels = []
            for ch_name in inst.info['ch_names']:
                if ch_name in inst.info['bads']:
                    ch_name += ' (bad)'
                labels.append(ch_name)

            logging.getLogger('ui_logger').info("Saving data..")
            fileManager.save_tfr_topology(fname, inst.data, 
                                inst.times, freqs, labels)
            

        if scalp is not None:
            inst.plot_topomap(tmin=scalp['tmin'], tmax=scalp['tmax'],
                              fmin=scalp['fmin'], fmax=scalp['fmax'],
                              ch_type=ch_type, layout=layout,
                              show=False, cmap=cmap)

        logging.getLogger('ui_logger').info("Plotting.")
        fig = inst.plot_topo(fmin=freqs[0], fmax=freqs[-1], layout=layout, 
            cmap=cmap, title=title)

        fig.canvas.set_window_title('TFR' + '_' + collection_name)
        fig.show()

        def onclick(event):
            channel = plt.getp(plt.gca(), 'title')
            plt.gcf().canvas.set_window_title('_'.join(['TFR', collection_name,
                                                        channel]))
            plt.show(block=False)

        fig.canvas.mpl_connect('button_press_event', onclick)


    def TFR_raw(self, wsize, tstep, channel, fmin, fmax, blstart, blend, mode,
                save_data):
        lout = self.read_layout(self.experiment.layout)
        
        raw = self.experiment.active_subject.get_working_file()
        
        raw = raw.copy()
        raw.apply_proj()
        
        tfr = np.abs(mne.stft(raw._data, wsize, tstep=tstep))
        freqs = mne.stftfreq(wsize, sfreq=raw.info['sfreq'])
        times = np.arange(tfr.shape[2]) * tstep / raw.info['sfreq']
        baseline = (blstart, blend)
        
        tfr_ = mne.AverageTFR(raw.info, tfr, times, freqs, 1)
        
        if mode:
            tfr_.data = mne.rescale(tfr_.data, times, baseline=baseline, 
                                             mode=mode)
        
        fig = tfr_.plot(picks=[channel], fmin=fmin, fmax=fmax, layout=lout)
        subject_name = self.experiment.active_subject.subject_name
        fig.canvas.set_window_title(''.join(['TFR_raw_', subject_name, '_',
                                    raw.ch_names[channel]]))
        
        if save_data:
            path = fileManager.create_timestamped_folder(self.experiment)
            filename = os.path.join(path, ''.join([
                self.experiment.active_subject.subject_name, '_',
                raw.ch_names[channel], '_TFR.csv']))
            fileManager.save_tfr(filename, tfr[channel], times, freqs)

    def plot_power_spectrum(self, params, save_data, epoch_groups, basename='raw'):
        """
        Method for plotting power spectrum.
        Parameters:
        params         - Dictionary containing the parameters.
        save_data      - Boolean indicating whether to save psd data to files.
                         Only data from channels of interest is saved.
        """
        lout = self.read_layout(self.experiment.layout)
            
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
            # do a weighted (epoch lengths as weights) average of psds inside a group
            weights = np.array([length for psds_, freqs, length in psd_list])
            weights = weights.astype(float) / np.sum(weights)
            psd = np.average([psds_ for psds_, freqs, length in psd_list], 
                             weights=weights, axis=0)
            psds.append(psd)
            
        colors = self.colors(len(psds))

        subject_name = self.experiment.active_subject.subject_name
        if save_data:
            path = fileManager.create_timestamped_folder(self.experiment)
            for idx, psd in enumerate(psds):
                filename = ''.join([subject_name, '_', basename, '_',
                    'spectrum', '_', str(psd_groups.keys()[idx]), '.csv'])
                fileManager.save_np_array(os.path.join(path, filename), 
                                          freqs, psd, info)

        logging.getLogger('ui_logger').info("Plotting power spectrum...")

        def my_callback(ax, ch_idx):
            """
            Callback for the interactive plot.
            Opens a channel specific plot.
            """
            fig = plt.gcf()
            fig.canvas.set_window_title(''.join(['Spectrum_', subject_name,
                                        '_', info['ch_names'][ch_idx]]))
            
            conditions = [str(key) for key in psd_groups]
            positions = np.arange(0.025, 0.025 + 0.04 * len(conditions), 0.04)
            
            for cond, col, pos in zip(conditions, colors, positions):
                plt.figtext(0.775, pos, cond, color=col, fontsize=12)

            color_idx = 0
            for psd in psds:
                plt.plot(freqs, psd[ch_idx], color=colors[color_idx])
                color_idx += 1
            
            plt.xlabel('Frequency (Hz)')

            plt.ylabel('Power ({})'.format(get_power_unit(
                mne.channel_type(info, ch_idx),
                params['log'] 
            )))

            plt.show()

        info = deepcopy(info)
        info['ch_names'] = [ch for idx, ch in enumerate(info['ch_names'])
                            if idx in picks]

        for ax, idx in mne.iter_topography(info, fig_facecolor='white',
                                           axis_spinecolor='white',
                                           axis_facecolor='white', layout=lout,
                                           on_pick=my_callback):
            
            color_idx = 0
            for psd in psds:
                ax.plot(psd[idx], linewidth=0.2, color=colors[color_idx])
                color_idx += 1
        plt.gcf().canvas.set_window_title('Spectrum_' + subject_name)
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

                epoch.load_data()
                length = epoch._data.shape[-1]
                
                psds, freqs = mne.psd_welch(epoch, fmin=fmin, fmax=fmax, 
                    n_fft=nfft, n_overlap=overlap, picks=picks, 
                    proj=True, n_jobs=n_jobs)

                psds = np.average(psds, axis=0)

                if params['log']:
                    psds = 10 * np.log10(psds)
                
                if key not in psd_groups:
                    psd_groups[key] = []

                psd_groups[key].append((psds, freqs, length))

        return psd_groups

    def colors(self, n):
        cycler = itertools.cycle(['b', 'r', 'g', 'y', 'm', 'c', 'k', 'pink'])
        return list(itertools.islice(cycler, n))
