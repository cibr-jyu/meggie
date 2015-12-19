"""
Created on 19.12.2015

@author: talli
"""
import os

from PyQt4 import QtCore,QtGui

from meggie.code_meggie.general.caller import Caller
from meggie.ui.general.logDialogUi import Ui_LogDialog

class LogDialog(QtGui.QDialog):
    """
    Class containing the logic for logDialogUi. It is used for displaying the
    MNE calls and params of the current experiment.
    """
    caller = Caller.Instance()

    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)
        log_file = open(os.path.join(self.caller.experiment_name, 'meggie.log', 'w'))
        for line in log_file:
            self.ui.textEdit.append(line + '\n')