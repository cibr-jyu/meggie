"""
Created on 19.12.2015

@author: talli
"""
import os
import logging

from PyQt4 import QtGui

import meggie.code_meggie.general.fileManager as fileManager

from meggie.ui.general.logDialogUi import Ui_LogDialog

class LogDialog(QtGui.QDialog):
    """
    Class containing the logic for logDialogUi. It is used for displaying the
    MNE calls and params of the current experiment.
    """
    def __init__(self, parent):
        """
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)
        try:
            logfile_path = os.path.join(self.parent.experiment.workspace, 
                self.parent.experiment.experiment_name, 'meggie.log')
            log_file = open(logfile_path, 'r')

            logging.getLogger('ui_logger').info(
                'Showing last 10000 lines of ' + logfile_path)
            
            last_lines = fileManager.tail(log_file, lines=10000)

            for line in last_lines:
                self.ui.textEdit.append(line.strip('\n'))

        except:
            pass
