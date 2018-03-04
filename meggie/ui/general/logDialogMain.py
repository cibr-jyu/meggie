"""
Created on 19.12.2015

@author: talli
"""
import os

from PyQt4 import QtCore,QtGui

from meggie.ui.general.logDialogUi import Ui_LogDialog

class LogDialog(QtGui.QDialog):
    """
    Class containing the logic for logDialogUi. It is used for displaying the
    MNE calls and params of the current experiment.
    """
    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)
        try:
            log_file = open(os.path.join(self.parent.experiment.workspace, 
                self.parent.experiment.experiment_name, 'meggie.log'), 'r')
            for line in log_file:
                self.ui.textEdit.append(line.strip('\n'))
        except:
            pass
