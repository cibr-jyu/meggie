""" Contains a class for logic of channel groups dialog.
"""

import os
import logging

from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import mne
import matplotlib as mpl
import matplotlib.pyplot as plt

import meggie.utilities.filemanager as filemanager

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.channels import get_default_channel_groups
from meggie.utilities.channels import get_triplet_from_mag

from meggie.mainwindow.dialogs.channelGroupsDialogUi import Ui_channelGroupsDialog


class ChannelGroupsDialog(QtWidgets.QDialog):
    """ Contains the the logic for channel groups dialog.
    """

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

        raw = subject.get_raw()

        if self.ui.radioButtonEEG.isChecked():
            self.eeg_channel_groups = get_default_channel_groups(raw, 'eeg')
            self.ui.listWidgetChannelGroups.clear()
            for ch_name in sorted(self.eeg_channel_groups.keys()):
                self.ui.listWidgetChannelGroups.addItem(ch_name)

        else:
            meg_defaults = get_default_channel_groups(raw, 'meg')
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

        raw = subject.get_raw()
        
        if self.ui.radioButtonEEG.isChecked():
            if mne.pick_types(raw.info, meg=False, eeg=True).size == 0:
                messagebox(self.parent, 'No EEG channels found')
                return

            ch_names = self.eeg_channel_groups[selected_item.text()]
            try:
                ch_idxs = [raw.info['ch_names'].index(ch_name) for ch_name in ch_names]
            except ValueError:
                messagebox(self.parent, "Channel names in the group "
                                        "and the current subject don't match")
                return

            ch_groups = [[], ch_idxs]

            try:
                fig, selection = mne.viz.plot_sensors(raw.info, kind='select', ch_type='eeg',
                                                      ch_groups=ch_groups, show=False,
                                                      title='Group channels')
            except RuntimeError:
                messagebox(self.parent, 'Could not plot sensors. Is the montage set?')
                return

        else:
            if mne.pick_types(raw.info, meg=True, eeg=False).size == 0:
                messagebox(self.parent, 'No MEG channels found')
                return

            ch_names = self.meg_channel_groups[selected_item.text()]
            try:
                ch_idxs = [raw.info['ch_names'].index(ch_name) for ch_name in ch_names]
            except ValueError:
                messagebox(self.parent, "Channel names in the group "
                                        "and the current subject don't match")
                return

            ch_groups = [[], ch_idxs]

            fig, selection = mne.viz.plot_sensors(raw.info, kind='select', ch_type='mag',
                                                  ch_groups=ch_groups, show=False,
                                                  title='Group channels')

        # make markers bigger
        for child in fig.axes[0].get_children():
            if isinstance(child, mpl.collections.PathCollection):
                child.set_sizes([100])
                child.set_lw([1])
                break

        plt.show()

        def on_close(event):
            if self.ui.radioButtonMEG.isChecked():
                if selection:
                    all_megs = []
                    for ch_name in selection:
                        all_megs.extend(get_triplet_from_mag(ch_name))
                    self.meg_channel_groups[selected_item.text()] = all_megs
            else:
                if selection:
                    self.eeg_channel_groups[selected_item.text()] = selection


        fig.canvas.mpl_connect('close_event', on_close)

    def on_radioButtonEEG_toggled(self):
        self.ui.listWidgetChannelGroups.clear()
        for ch_name in sorted(self.eeg_channel_groups.keys()):
            self.ui.listWidgetChannelGroups.addItem(ch_name)

    def on_radioButtonMEG_toggled(self):
        self.ui.listWidgetChannelGroups.clear()
        for ch_name in sorted(self.meg_channel_groups.keys()):
            self.ui.listWidgetChannelGroups.addItem(ch_name)

    def accept(self):
        channel_groups = {
            'eeg': self.eeg_channel_groups,
            'meg': self.meg_channel_groups
        }
        try:
            self.parent.experiment.channel_groups = channel_groups
            self.parent.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return
        
        logging.getLogger('ui_logger').info('Channel groups saved.')
        self.close()
