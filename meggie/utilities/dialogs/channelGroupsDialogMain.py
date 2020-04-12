"""
"""

import os

from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import mne
import matplotlib as mpl
import matplotlib.pyplot as plt

import meggie.utilities.filemanager as filemanager

from meggie.utilities.messaging import messagebox
from meggie.utilities.channels import get_default_channel_groups

from meggie.utilities.dialogs.channelGroupsDialogUi import Ui_channelGroupsDialog


class ChannelGroupsDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_channelGroupsDialog()
        self.ui.setupUi(self)

        self.parent = parent

        channel_groups = self.parent.experiment.channel_groups

        self.eeg_channel_groups = deepcopy(channel_groups['eeg'])
        self.meg_channel_groups = deepcopy(channel_groups['meg'])

        # default channel type is MEG
        for ch_name in sorted(self.meg_channel_groups.keys()):
            self.ui.listWidgetChannelGroups.addItem(ch_name)

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        name = self.ui.lineEditAdd.text()

        if self.ui.radioButtonEEG.isChecked():
            if name in self.eeg_channel_groups.keys():
                return
            self.eeg_channel_groups[name] = []

            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.eeg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)
        else:
            if name in self.meg_channel_groups.keys():
                return
            self.meg_channel_groups[name] = []

            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.meg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)

    def on_pushButtonRemove_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        if not self.ui.listWidgetChannelGroups.currentItem():
            return

        current_item = str(self.ui.listWidgetChannelGroups.currentItem().text())

        if self.ui.radioButtonEEG.isChecked():
            self.eeg_channel_groups.pop(current_item)
            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.eeg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)
        else:
            self.meg_channel_groups.pop(current_item)
            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.meg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)


    def on_pushButtonReset_clicked(self, checked=None):
        if checked is None:
            return

        subject = self.parent.experiment.active_subject
        if not subject:
            messagebox(self.parent, 'To reset, active subject is needed')
            return

        info = subject.get_raw().info

        if self.ui.radioButtonEEG.isChecked():
            self.eeg_channel_groups = get_default_channel_groups(info, 'eeg')
            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.eeg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)

        else:
            meg_defaults = get_default_channel_groups(info, 'meg')
            self.meg_channel_groups = meg_defaults
            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.meg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)

    def on_pushButtonSetChannels_clicked(self, checked=None):
        if checked is None:
            return

        subject = self.parent.experiment.active_subject
        if not subject:
            messagebox(self.parent, 'To set channels, active subject is needed')
            return

        try:
            selected_item = self.ui.listWidgetChannelGroups.selectedItems()[0]
        except IndexError:
            messagebox(self.parent, 'Select a channel group first')
            return

        info = subject.get_raw().info
        
        if self.ui.radioButtonEEG.isChecked():
            if mne.pick_types(info, meg=False, eeg=True).size == 0:
                messagebox(self.parent, 'No EEG channels found')
                return

            ch_groups = [[], self.eeg_channel_groups[selected_item.text()]]

            fig, selection = mne.viz.plot_sensors(info, kind='select', ch_type='eeg',
                                                  ch_groups=ch_groups, show=False)

        else:
            if mne.pick_types(info, meg=True, eeg=False).size == 0:
                messagebox(self.parent, 'No MEG channels found')
                return

            ch_groups = [[], self.meg_channel_groups[selected_item.text()]]

            fig, selection = mne.viz.plot_sensors(info, kind='select', ch_type='mag',
                                                  ch_groups=ch_groups, show=False)

        # make markers bigger
        for child in fig.axes[0].get_children():
            if isinstance(child, mpl.collections.PathCollection):
                child.set_sizes([100])
                child.set_lw([1])
                break

        plt.show(block=True)

        ch_idxs = [info['ch_names'].index(ch_name) for ch_name in selection]

        if self.ui.radioButtonMEG.isChecked(): 
            self.meg_channel_groups[selected_item.text()] = ch_idxs
        else:
            self.eeg_channel_groups[selected_item.text()] = ch_idxs

    def on_radioButtonEEG_toggled(self):
        self.ui.listWidgetChannelGroups.clear()
        for ch_name in sorted(self.eeg_channel_groups.keys()):
            self.ui.listWidgetChannelGroups.addItem(ch_name)

    def on_radioButtonMEG_toggled(self):
        self.ui.listWidgetChannelGroups.clear()
        for ch_name in sorted(self.meg_channel_groups.keys()):
            self.ui.listWidgetChannelGroups.addItem(ch_name)

    def accept(self):
        # self.parent.experiment.save_experiment_settings()
        self.close()
