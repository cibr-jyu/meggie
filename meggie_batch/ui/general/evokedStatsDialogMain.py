'''
Created on Sep 4, 2013

@author: atmiraut
'''
from PyQt4 import QtCore, QtGui

import mne
import numpy as np

from evokedStatsDialogUi import Ui_EvokedStatsDialog
from statistic import Statistic
from externalModules.mne.utils import _clean_names
import messageBoxes

class EvokedStatsDialog(QtGui.QDialog):

    """A Window for displaying statistical information of averaged epochs."""

    def __init__(self, evoked=None):
        """Constructor.

        Keyword arguments:

        evoked = a dictionary containing evoked-objects.
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_EvokedStatsDialog()
        self.ui.setupUi(self)
        self.evoked = evoked
        if evoked is None: return

        #Selected_items is a dictionary containing all the channels selected
        #across the evoked sets in the comboBoxEvokeds. 
        self.selected_channels = [list() for _ in self.evoked]

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
        self.ui.pushButtonSetSelected.setEnabled(False)

        self.evoked_set_changed()

        self.ui.listWidgetChannels.itemSelectionChanged.\
        connect(self.selection_changed)
        self.ui.doubleSpinBoxStart.setValue(evoked[0].times[0])
        self.ui.doubleSpinBoxStop.setValue(evoked[0].times[-1])
        #Save CSV: Create a CSV file of the key values displayed on the right side

    def checkBox_state_changed(self):
        """Select or unselect channels based on the checkbox.

        If the checkbox is unchecked, all related channels are unselected.
        If the checkbox is checked, all related channels are selected.

        Keyword arguments:

        state -- Integer stating whether the checkbox is checked or unchecked.
        """
        channels = mne.selection.read_selection(str(self.sender().text()))
        has_spaces = ' ' in channels[0]
        channels = _clean_names(channels, remove_whitespace=has_spaces)
        for channel in channels:
            for i in range(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                if str(item.text()) == channel:
                    item.setSelected(self.sender().isChecked())
                    break

    def evoked_set_changed(self):
        """Updates the channel list with current evoked's channels."""
        index = self.ui.comboBoxEvoked.currentIndex()
        channels = self.evoked[index].info['ch_names']

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
        for channel in self.selected_channels[index]:
            for i in range(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                if str(item.text()) == channel:
                    item.setSelected(True)
                    break

        self.update_start_stop()

        self.ui.pushButtonSetSelected.setEnabled(False)

    def on_pushButtonClearSelections_clicked(self):
        """Reset the values in the dialog's spinboxes."""
        self.reset_data_values()
        self.ui.pushButtonSetSelected.setEnabled(False)

    def on_pushButtonSetSelected_clicked(self, checked=None):
        """Save selected channels to selected_channels dictionary."""
        if checked is None: return
        if len(self.ui.listWidgetChannels.selectedItems()) == 0: return

        index = self.ui.comboBoxEvoked.currentIndex()
        self.selected_channels[index] = list()
        for item in self.ui.listWidgetChannels.selectedItems():
            if item not in self.selected_channels[index]:
                self.selected_channels[index].append(str(item.text()))

        self.ui.pushButtonSetSelected.setEnabled(False)

        channels = self.selected_channels[index]
        self.update_info(channels)
        #TODO: Update the info widgets. If item_selection has multiple
        #channels, they should be averaged and the result of that should be
        #shown on the info widgets.   

    def populateComboBoxEvoked(self):
        """Populate the combo box above the channel list with evoked set names.
        """
        for evoked in self.evoked:
            self.ui.comboBoxEvoked.addItem(str(evoked))

    def reset_data_values(self):
        """Reset all the spinboxes and labels displaying data."""
        self.ui.checkBoxLFrontal.setChecked(False)
        self.ui.checkBoxLOcci.setChecked(False)
        self.ui.checkBoxLParietal.setChecked(False)
        self.ui.checkBoxLTemp.setChecked(False)
        self.ui.checkBoxRFrontal.setChecked(False)
        self.ui.checkBoxROcci.setChecked(False)
        self.ui.checkBoxRParietal.setChecked(False)
        self.ui.checkBoxRTemp.setChecked(False)
        self.ui.checkBoxVertex.setChecked(False)
        self.ui.labelSelectedChannel.setText('No Channels selected.')
        self.resetSpinBoxes()

        for key in self.selected_channels.keys():
            self.selected_channels[key] = []

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

    def selection_changed(self):
        """Enable pushButtonSetSelected."""
        if len(self.ui.listWidgetChannels.selectedItems()) > 0:
            self.ui.pushButtonSetSelected.setEnabled(True)

        else: self.ui.pushButtonSetSelected.setEnabled(False)

    def update_info(self, names):
        """Update the info widgets with data based on item.
        
        Keyword arguments:
        
        names -- Name(s) of the channel(s) whose data is to be displayed. 
                List for many, string for one.
        """
        evoked = self.evoked[self.ui.comboBoxEvoked.currentIndex()]
        tmin = self.ui.doubleSpinBoxStart.value()
        tmax = self.ui.doubleSpinBoxStop.value()
        times = evoked.times
        # cropping the data:
        min_idx = np.searchsorted(times, tmin)
        max_idx = np.searchsorted(times, tmax)
        data = evoked.data[:, min_idx:max_idx]
        this_data = list()
        ch_type = ''
        if isinstance(names, str):
            names = [names]

        for name in names:
            ch_index = evoked.ch_names.index(name)
            if ch_type == '':
                ch_type = mne.channels.channels.channel_type(evoked.info,
                                                             ch_index)
            elif ch_type != mne.channels.channels.channel_type(evoked.info,
                                                               ch_index):
                msg = ('Channels are of different type.')
                messageBox = messageBoxes.shortMessageBox(msg)
                messageBox.exec_()
                return
            this_data.append(data[ch_index])
        data = np.mean(this_data, axis=0)
        if ch_type == 'grad':
            suffix = 'fT/cm'
            scaler = 1e13
        elif ch_type == 'mag':
            suffix = 'fT'
            scaler = 1e15
        elif ch_type == 'eeg':
            suffix = 'uV'
            scaler = 1e6
        else:
            msg = ('Statistics not supported for %s channels.' % ch_type)
            messageBox = messageBoxes.shortMessageBox(msg)
            messageBox.exec_()
            return
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
        time_min = self.evoked[0].times[time_min_i]
        time_max = self.evoked[0].times[time_max_i]
        time_before = self.evoked[0].times[time_before_i]
        time_after = self.evoked[0].times[time_after_i]

        duration = time_after - time_before
        integral = self.statUpdater.integrate(data, time_before_i,
                                              time_after_i)

        minimum = minimum * scaler
        maximum = maximum * scaler
        half_max = half_max * scaler
        #integral = integral * scaler

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

    def update_start_stop(self):
        """ Aux function for updating upper and lower limit for time window."""
        times = self.evoked[self.ui.comboBoxEvoked.currentIndex()].times
        self.ui.doubleSpinBoxStart.setMinimum(times[0])
        self.ui.doubleSpinBoxStart.setMaximum(times[-1])
        self.ui.doubleSpinBoxStop.setMinimum(times[0])
        self.ui.doubleSpinBoxStop.setMaximum(times[-1])
