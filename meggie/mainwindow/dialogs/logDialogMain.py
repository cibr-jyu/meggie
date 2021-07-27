""" Contains a class for logic of log dialog.
"""
import os
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import meggie.utilities.filemanager as filemanager

from meggie.utilities.messaging import exc_messagebox
from meggie.mainwindow.dialogs.logDialogUi import Ui_LogDialog


class LogDialog(QtWidgets.QDialog):
    """ Contains logic for log dialog.
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)

        self.lines = int(str(self.ui.spinBoxBufferSize.value()))
        self._update_contents()

    def _update_contents(self):
        try:
            logfile_path = os.path.join(self.parent.experiment.path, 'mne.log')
            log_file = open(logfile_path, 'r')

            msg = 'Showing last {0} lines of {1}'.format(
                self.lines, logfile_path)
            logging.getLogger('ui_logger').info(msg)

            last_lines = filemanager.tail(log_file, lines=self.lines)

            # find first idx that starts a call
            start_idx = None
            for line_idx, line in enumerate(last_lines):
                if line.startswith('MNE call:'):
                    start_idx = line_idx
                    break

            self.ui.textEditBrowser.clear()

            if start_idx is None:
                return

            for line in last_lines[start_idx:]:
                self.ui.textEditBrowser.append(line.strip('\n'))

        except Exception as exc:
            exc_messagebox(self, exc)

    def on_pushButtonBufferSize_clicked(self, checked=None):
        if checked is None:
            return
        self.lines = int(str(self.ui.spinBoxBufferSize.value()))
        self._update_contents()
