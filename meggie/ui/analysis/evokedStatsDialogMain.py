'''
Created on Sep 4, 2013

@author: atmiraut
'''
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QFileDialog

import csv
import os
import numpy as np
import mne

from mne.channels.layout import _pair_grad_sensors_from_ch_names
from mne.channels.layout import _merge_grad_data
from mne.utils import _clean_names

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general.statistic import Statistic
from meggie.ui.analysis.evokedStatsDialogUi import Ui_EvokedStatsDialog

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.code_meggie.general import fileManager

class EvokedStatsDialog(QtGui.QDialog):

    """A Window for displaying statistical information of averaged epochs."""

    def __init__(self, parent, evoked_name):
        """Constructor.
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_EvokedStatsDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.evoked_name = evoked_name

        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds

        #Selected_items is a dictionary containing all the channels selected
        #across the evoked sets in the comboBoxEvokeds. 
        self.selected_channels = {}
        for evoked in evokeds.values():
            self.selected_channels[evoked.comment] = list()

        self.populateComboBoxEvoked()

        self.ui.checkBoxLFrontal.stateChanged.connect(self.
                                                      checkBox_state_changed)
        self.ui.checkBoxLOcci.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxLParietal.stateChanged.connect(self.
                                                       checkBox_state_changed)
        self.ui.checkBoxLTemp.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxRFrontal.stateChanged.connect(self.
                                                      checkBox_state_changed)
        self.ui.checkBoxROcci.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxRParietal.stateChanged.connect(self.
                                                       checkBox_state_changed)
        self.ui.checkBoxRTemp.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxVertex.stateChanged.connect(self.
                                                    checkBox_state_changed)

        self.statUpdater = Statistic()

        self.ui.comboBoxEvoked.currentIndexChanged.connect(self.
                                                           evoked_set_changed)
       
        self.evoked_set_changed()

        values = evokeds.values()
        self.ui.doubleSpinBoxStart.setValue(values[0].times[0])
        self.ui.doubleSpinBoxStop.setValue(values[0].times[-1])
        

    def checkBox_state_changed(self):
        """Select or unselect channels based on the checkbox.

        If the checkbox is unchecked, all related channels are unselected.
        If the checkbox is checked, all related channels are selected.

        Keyword arguments:

        state -- Integer stating whether the checkbox is checked or unchecked.
        """
        channels = mne.selection.read_selection(str(self.sender().text()))
        if ' ' in channels[0] and (' ' not in
                                   self.ui.listWidgetChannels.item(0).text()):
            remove_spaces = True
        else:
            remove_spaces = False
        channels = _clean_names(channels, remove_whitespace=remove_spaces)
        for channel in channels:
            for i in range(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                if str(item.text()) == channel:
                    item.setSelected(self.sender().isChecked())
                    break

    def evoked_set_changed(self):
        """Updates the channel list with current evoked's channels."""
        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds
        
        for evoked_value in evokeds.values():
            if self.ui.comboBoxEvoked.currentText() == evoked_value.comment:
                channels = evoked_value.ch_names
                evoked = evoked_value
                event_name = evoked_value.comment
        
        #First clear the channel list.
        for i in range(self.ui.listWidgetChannels.count()):
            self.ui.listWidgetChannels.takeItem(0)

        #Then add the new channels to the list.
        #Note: This could actually be useless. The channel names seem to be
        #the same across the data sets. Don't know if this is actually
        #the case though.
        for channel in channels:
            item = QtGui.QListWidgetItem(channel)
            self.ui.listWidgetChannels.addItem(item)
            self.ui.listWidgetChannels.sortItems()

        #Finally check if there are any channels that need to be set as
        #selected in the new channel list.
        #for channel in self.selected_channels[index]:
        for channel in self.selected_channels[event_name]:
            for i in range(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                if str(item.text()) == channel:
                    item.setSelected(True)
                    break

        self.update_start_stop(evoked)


    def on_pushButtonClearSelections_clicked(self):
        """Reset the values in the dialog's spinboxes."""
        self.reset_data_values()
    
    def reset_data_values(self):
        self.ui.listWidgetChannels.clearSelection()
        self.selected_channels = {}
        children = self.findChildren(QtGui.QDoubleSpinBox)
        
        for child in children:
            child.setValue(0)

        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds
        for evoked in evokeds.values():
            self.selected_channels[evoked.comment] = list()
            if self.ui.comboBoxEvoked.currentText() == evoked.comment:
                self.update_start_stop(evoked)      
        
    def on_pushButtonSetSelected_clicked(self, checked=None):
        """Save selected channels to selected_channels dictionary."""
        if checked is None: return
        if len(self.ui.listWidgetChannels.selectedItems()) == 0: return

        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds

        for evoked_value in evokeds.values():
            if self.ui.comboBoxEvoked.currentText() == evoked_value.comment:
                evoked = evoked_value
                event_name = evoked_value.comment
        
        selection = list()
        for item in self.ui.listWidgetChannels.selectedItems():
            if item not in self.selected_channels[event_name]:
                selection.append(str(item.text()))
        if self.ui.radioButtonGrad.isChecked():
            picks = mne.pick_types(evoked.info, meg='grad', ref_meg=False,
                                   selection=selection)
        elif self.ui.radioButtonMag.isChecked():
            picks = mne.pick_types(evoked.info, meg='mag', ref_meg=False,
                                   selection=selection)
        elif self.ui.radioButtonEeg.isChecked():
            picks = mne.pick_types(evoked.info, meg=False, eeg=True,
                                   ref_meg=False, selection=selection)
        self.selected_channels[event_name] = [evoked.ch_names[x] for x in picks]

        self.update_info()
        #TODO: Update the info widgets. If item_selection has multiple
        #channels, they should be averaged and the result of that should be
        #shown on the info widgets.

    def on_pushButtonVisualize_clicked(self, checked=None):
        """Visualize selected channel(s)."""
        if checked is None: 
            return
        caller = Caller.Instance()
        
        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds
        
        for evoked in evokeds.values():
            if self.ui.comboBoxEvoked.currentText() == evoked.comment:
                evoked_to_viz = evoked
                event_name = evoked.comment
        
        try:
            caller.average_channels(evoked_to_viz, None,
                                    set(self.selected_channels[event_name]))
        except TypeError as e:
            exc_messagebox(self, "Please set selections")
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonCSV_clicked(self, checked=None):
        """
        Saves a csv file of the statistics.
        """
        if checked is None:
            return
        
        caller = self.parent.caller
        path = fileManager.create_timestamped_folder(caller.experiment)
        collection_name = str(self.ui.comboBoxEvoked.currentText())
        filename = collection_name + '_stats.csv'
        path = os.path.join(path, filename)
        fname = str(QFileDialog.getSaveFileName(parent=self, 
                                                caption='Save csv file.',
                                                directory=path))

        if fname == '':
            return
        
        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds
        evoked = evokeds.get(collection_name)
        
        if not evoked:
            return
        
        print 'Saving csv...'
        tmin = self.ui.doubleSpinBoxStart.value()
        tmax = self.ui.doubleSpinBoxStop.value()
        times = evoked.times
        min_idx = np.searchsorted(times, tmin)
        max_idx = np.searchsorted(times, tmax)
        # cropping the data:
        data = evoked.data[:, min_idx:max_idx]
        
        with open(fname, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Ch name', 'Start', 'Stop', 'Minimum amplitude',
                             'Time of minimum', 'Maximum amplitude',
                             'Time of maximum', 'Half maximum',
                             'Time before max', 'Time after max', 'Duration',
                             'Integral'])
            for ch_name in self.selected_channels[collection_name]:
                pick = evoked.ch_names.index(ch_name)
                this_data = data[pick]
                ch_type = mne.channels.channels.channel_type(evoked.info, pick)
                if ch_type == 'grad':
                    scaler = 1e13
                elif ch_type == 'mag':
                    scaler = 1e15
                elif ch_type == 'eeg':
                    scaler = 1e6
                else:
                    print ('Statistics not supported for %s channels. Skipping'
                           ' channel %s.') % (ch_type, ch_name)
                    continue
                self._write_csv_row(writer, ch_name, this_data, times, tmin,
                                    tmax, min_idx, max_idx, scaler)

                if ch_name.startswith('MEG') and ch_name.endswith('3'):
                    if (ch_name[:-1] + '2') in self.selected_channels[collection_name]:
                        # Merge data from pair of grad channels
                        pick2 = evoked.ch_names.index(ch_name[:-1] + '2')
                        this_data = _merge_grad_data(np.array([this_data,
                                                               data[pick2]]))
                        self._write_csv_row(writer, ch_name[:-1] + 'X',
                                            this_data[0], times, tmin, tmax,
                                            min_idx, max_idx, scaler)

    def _write_csv_row(self, writer, ch_name, data, times, tmin, tmax, min_idx,
                       max_idx, scale_factor):
        """Helper for writing data row to csv file."""
        minimum, time_min_i = self.statUpdater.find_minimum(data)
        maximum, time_max_i = self.statUpdater.find_maximum(data)
        (half_max, time_before_i,
        time_after_i) = self.statUpdater.find_half_maximum(data)

        time_min = times[time_min_i]
        time_max = times[time_max_i]
        time_before = times[time_before_i]
        time_after = times[time_after_i]
        
        duration = time_after - time_before
        integral = self.statUpdater.integrate(data, times[min_idx:max_idx],
                                              time_before_i, time_after_i)

        minimum = minimum * scale_factor
        maximum = maximum * scale_factor
        half_max = half_max * scale_factor
        integral = integral * scale_factor
        writer.writerow([ch_name, tmin, tmax, minimum, time_min, maximum,
                         time_max, half_max, time_before, time_after, duration,
                         integral])

    def populateComboBoxEvoked(self):
        """Populate the combo box above the channel list with evoked set names.
        """
        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds
        
        for evoked in evokeds:
            self.ui.comboBoxEvoked.addItem(str(evoked))

    def resetSpinBoxes(self):
        """Reset the values in the dialog's spinboxes."""
        self.ui.doubleSpinBoxDuration.setValue(0)
        self.ui.doubleSpinBoxHalfMaxAfter.setValue(0)
        self.ui.doubleSpinBoxHalfMaxAmplitude.setValue(0)
        self.ui.doubleSpinBoxHalfMaxBefore.setValue(0)
        self.ui.doubleSpinBoxIntegral.setValue(0)
        self.ui.doubleSpinBoxMaxAmplitude.setValue(0)
        self.ui.doubleSpinBoxMaxTime.setValue(0)
        self.ui.doubleSpinBoxMinAmplitude.setValue(0)
        self.ui.doubleSpinBoxMinTime.setValue(0)

    def update_info(self):
        """Update the info widgets with data based on item."""
        subject = self.parent.caller.experiment.active_subject
        evokeds = subject.evokeds[self.evoked_name].mne_evokeds
        
        for evoked_value in evokeds.values():
            if self.ui.comboBoxEvoked.currentText() == evoked_value.comment:
                evoked = evoked_value
                event_name = evoked_value.comment
        
        names = self.selected_channels[event_name]
        tmin = self.ui.doubleSpinBoxStart.value()
        tmax = self.ui.doubleSpinBoxStop.value()
        times = evoked.times
        # cropping the data:
        min_idx = np.searchsorted(times, tmin)
        max_idx = np.searchsorted(times, tmax)
        data = evoked.data[:, min_idx:max_idx]
        times = evoked.times[min_idx:max_idx]
        this_data = list()
        ch_type = ''
        if isinstance(names, str):
            names = [names]

        for name in names:
            ch_index = evoked.ch_names.index(name)
            if ch_type == '':
                ch_type = mne.channels.channels.channel_type(evoked.info,
                                                             ch_index)
            this_data.append(data[ch_index])

        if ch_type == 'grad':
            suffix = 'fT/cm'
            scaler = 1e13
            gradsIdxs = _pair_grad_sensors_from_ch_names(names)
            this_data = np.array(this_data)
            try:
                this_data = _merge_grad_data(this_data[gradsIdxs])
            except ValueError as err:
                msg = 'Please select gradiometers as pairs for RMS.'
                messagebox(self, msg)
                return
        elif ch_type == 'mag':
            suffix = 'fT'
            scaler = 1e15
        elif ch_type == 'eeg':
            suffix = 'uV'
            scaler = 1e6
        else:
            msg = 'Could not find data.'
            messagebox(self, msg)
            return
        data = np.mean(this_data, axis=0)
        self.ui.doubleSpinBoxMinAmplitude.setSuffix(suffix)
        self.ui.doubleSpinBoxMaxAmplitude.setSuffix(suffix)
        self.ui.doubleSpinBoxHalfMaxAmplitude.setSuffix(suffix)

        #First collect all the necessary bits of information
        minimum, time_min_i = self.statUpdater.find_minimum(data)
        maximum, time_max_i = self.statUpdater.find_maximum(data)
        half_max, time_before_i, time_after_i = (self.statUpdater.
                                                 find_half_maximum(data))

        #time_min_i, time_max_i, time_before_i and time_after_i are actually
        #index values fetch the actual times from evoked.times.
        time_min = times[time_min_i]
        time_max = times[time_max_i]
        time_before = times[time_before_i]
        time_after = times[time_after_i]

        duration = time_after - time_before
        integral = self.statUpdater.integrate(data,
                                              evoked.times[min_idx:max_idx],
                                              time_before_i, time_after_i)

        minimum = minimum * scaler
        maximum = maximum * scaler
        half_max = half_max * scaler
        integral = integral * scaler

        #Then update the appropriate fields in the dialog.
        self.ui.labelSelectedChannel.setText(name)
        self.ui.doubleSpinBoxDuration.setValue(duration)
        self.ui.doubleSpinBoxHalfMaxAfter.setValue(time_after)
        self.ui.doubleSpinBoxHalfMaxAmplitude.setValue(half_max)
        self.ui.doubleSpinBoxHalfMaxBefore.setValue(time_before)
        self.ui.doubleSpinBoxIntegral.setValue(integral)
        self.ui.doubleSpinBoxMaxAmplitude.setValue(maximum)
        self.ui.doubleSpinBoxMaxTime.setValue(time_max)
        self.ui.doubleSpinBoxMinAmplitude.setValue(minimum)
        self.ui.doubleSpinBoxMinTime.setValue(time_min)

        if len(names) == 1:
            self.ui.labelSelectedChannel.setText(names[0])
        else:
            title = 'Average over {0} {1} channels.'.format(str(len(names)),
                                                            ch_type)
            self.ui.labelSelectedChannel.setText(title)

    def update_start_stop(self, evoked_event):
        """ Aux function for updating upper and lower limit for time window."""
        times = evoked_event.times

        self.ui.doubleSpinBoxStart.setMinimum(times[0])
        self.ui.doubleSpinBoxStart.setMaximum(times[-1])
        self.ui.doubleSpinBoxStop.setMinimum(times[0])
        self.ui.doubleSpinBoxStop.setMaximum(times[-1])

        self.ui.doubleSpinBoxStart.setValue(times[0])
        self.ui.doubleSpinBoxStop.setValue(times[-1])
