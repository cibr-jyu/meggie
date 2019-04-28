"""
"""
import os
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import meggie.code_meggie.general.fileManager as fileManager

from meggie.ui.utils.messaging import exc_messagebox

from meggie.ui.general.logDialogUi import Ui_LogDialog


class LogDialog(QtWidgets.QDialog):
    """
    Class containing the logic for logDialogUi. It is used for displaying the
    MNE calls and params of the current experiment.
    """

    def __init__(self, parent):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)

        self.lines = int(str(self.ui.spinBoxBufferSize.value()))

        self.show_meggie = False
        self.show_mne = False

        if self.ui.checkBoxShowMeggie.checkState() == QtCore.Qt.Checked:
            self.show_meggie = True
        if self.ui.checkBoxShowMNE.checkState() == QtCore.Qt.Checked:
            self.show_mne = True

        self.update_contents()

    def update_contents(self):
        try:
            logfile_path = os.path.join(self.parent.experiment.workspace,
                                        self.parent.experiment.experiment_name, 'meggie.log')
            log_file = open(logfile_path, 'r')

            # logging.getLogger('ui_logger').info(
            #     'Showing last 10000 lines of ' + logfile_path)

            last_lines = fileManager.tail(log_file, lines=self.lines)

            mne_idxs = []
            meggie_idxs = []
            all_idxs = []
            for line_idx, line in enumerate(last_lines):
                if line.startswith('Meggie:'):
                    meggie_idxs.append(line_idx)
                    all_idxs.append(line_idx)
                elif line.startswith('MNE call:'):
                    mne_idxs.append(line_idx)
                    all_idxs.append(line_idx)

            self.ui.textEditBrowser.clear()

            if not self.show_mne and not self.show_meggie:
                selected_lines = []

            elif self.show_mne and not self.show_meggie:
                selected_lines = []
                for idx_idx, line_idx in enumerate(all_idxs):
                    if line_idx not in mne_idxs:
                        continue
                    if idx_idx != len(all_idxs) - 1:
                        selected_lines.extend(
                            last_lines[line_idx:all_idxs[idx_idx + 1]])
                    else:
                        selected_lines.extend(last_lines[line_idx:])
            elif self.show_meggie and not self.show_mne:
                selected_lines = []
                for idx_idx, line_idx in enumerate(all_idxs):
                    if line_idx not in meggie_idxs:
                        continue
                    if idx_idx != len(all_idxs) - 1:
                        selected_lines.extend(
                            last_lines[line_idx:all_idxs[idx_idx + 1]])
                    else:
                        selected_lines.extend(last_lines[line_idx:])
            else:
                selected_lines = last_lines

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

    def on_pushButtonBufferSize_clicked(self, checked=None):
        if checked is None:
            return
        self.lines = int(str(self.ui.spinBoxBufferSize.value()))
        self.update_contents()
