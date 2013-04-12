'''
Created on Apr 12, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from eogParametersDialog import Ui_Dialog

class EogParametersDialog(QtGui.QDialog):


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog() # Refers to class in module eogParametersDialog
        self.ui.setupUi(self)
        
    def accept(self):
        tmin = self.ui.spinBoxTmin.value()
        tmax = self.ui.spinBoxTmax.value()
        event_id = self.ui.lineEditEventID.text()
        low_freq = self.ui.spinBoxLowPass.value()
        high_freq = self.ui.spinBoxHighPass.value()
        grad = self.ui.spinBoxGrad.value()
        mag = self.ui.spinBoxMag.value()
        eeg = self.ui.spinBoxEeg.value()
        filter_low = self.ui.spinBoxLow.value()
        filter_high = self.ui.spinBoxHigh.value()
        