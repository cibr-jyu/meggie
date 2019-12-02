"""
"""
import os
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import meggie.utilities.filemanager as filemanager

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.dialogs.logDialogUi import Ui_LogDialog


class LogDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)

        self.lines = int(str(self.ui.spinBoxBufferSize.value()))

        self.show_meggie = False
        self.show_mne = False
        self.show_mne_call = False

        if self.ui.checkBoxShowMeggie.checkState() == QtCore.Qt.Checked:
            self.show_meggie = True

        if self.ui.checkBoxShowMNE.checkState() == QtCore.Qt.Checked:
            self.show_mne = True

        if self.ui.checkBoxShowMNEcall.checkState() == QtCore.Qt.Checked:
            self.show_mne_call = True

        self.update_contents()

    def update_contents(self):
        try:
            logfile_path = os.path.join(self.parent.experiment.workspace,
                                        self.parent.experiment.name, 'meggie.log')
            log_file = open(logfile_path, 'r')

            # logging.getLogger('ui_logger').info(
            #     'Showing last 10000 lines of ' + logfile_path)

            last_lines = filemanager.tail(log_file, lines=self.lines)

            # track lines that start log entries as there can be multiline
            # entries.

            meggie_idxs = []
            mne_idxs = []
            mne_call_idxs = []
            all_idxs = []
            for line_idx, line in enumerate(last_lines):
                if line.startswith('Meggie:'):
                    meggie_idxs.append(line_idx)
                    all_idxs.append(line_idx)
                elif line.startswith('MNE call:'):
                    mne_call_idxs.append(line_idx)
                    all_idxs.append(line_idx)
                elif line.startswith('MNE:'):
                    mne_idxs.append(line_idx)
                    all_idxs.append(line_idx)

            self.ui.textEditBrowser.clear()

            selected_lines = []
            for idx_idx, line_idx in enumerate(all_idxs):
                if idx_idx != len(all_idxs) - 1:
                    next_idx = all_idxs[idx_idx + 1]
                else:
                    next_idx = -1
                if line_idx in meggie_idxs:
                    if self.show_meggie:
                        selected_lines.extend(
                            last_lines[line_idx:next_idx])
                elif line_idx in mne_idxs:
                    if self.show_mne:
                        selected_lines.extend(
                            last_lines[line_idx:next_idx])
                elif line_idx in mne_call_idxs:
                    if self.show_mne_call:
                        selected_lines.extend(
                            last_lines[line_idx:next_idx])

            for line in selected_lines:
                self.ui.textEditBrowser.append(line.strip('\n'))

        except Exception as exc:
            exc_messagebox(self, exc)

    def on_checkBoxShowMeggie_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.show_meggie = True
        else:
            self.show_meggie = False
        self.update_contents()

    def on_checkBoxShowMNE_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.show_mne = True
        else:
            self.show_mne = False
        self.update_contents()

    def on_checkBoxShowMNEcall_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.show_mne_call = True
        else:
            self.show_mne_call = False
        self.update_contents()

    def on_pushButtonBufferSize_clicked(self, checked=None):
        if checked is None:
            return
        self.lines = int(str(self.ui.spinBoxBufferSize.value()))
        self.update_contents()
