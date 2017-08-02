# coding: utf-8
'''
Created on Aug 02, 2017

@author: erpipehe
'''

from PyQt4 import QtCore,QtGui

from meggie.ui.preprocessing.icaDialogUi import Ui_Dialog

from meggie.code_meggie.general.caller import Caller

from meggie.ui.utils.messaging import messagebox

class ICADialog(QtGui.QDialog):
    """
    Class containing the logic for filterDialog. It collects the parameters
    needed for filtering and shows the preview for the filter if required.
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.caller = Caller.Instance()

    def accept(self):
        """
        Apply the zeroing.
        """

        print "Miau"

        self.close()
