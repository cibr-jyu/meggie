"""
"""

import os

from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.messaging import messagebox

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

        if self.ui.radioButtonEEG.isChecked():
            self.eeg_channel_groups = {}
            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.eeg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)

        else:
            meg_defaults = dict([(sel, mne.read_selection(sel)) for sel in
                             mne.selection._SELECTIONS])
            self.meg_channel_groups = meg_defaults
            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.meg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)

    def on_pushButtonSetChannels_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment.active_subject:
            messagebox(self.parent, 'To set channels, active subject is needed')
            return

        # plot_sensors with selection here
            
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
