'''
Created on Apr 30, 2013

@author: jaeilepp
'''

from epochDialog_Ui import Ui_Dialog

from PyQt4 import QtCore,QtGui

class EpochDialog(QtGui.QDialog):
    '''
    classdocs
    '''
    index = 1

    def __init__(self, parent):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def accept(self):
        self.tmin = float(self.ui.doubleSpinBoxTmin.value())
        self.tmax = float(self.ui.doubleSpinBoxTmax.value())
        epoch_name = self.ui.lineEditName.text()
        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        channels = self.check_channels()
        reject = dict(grad = 1e-12 * self.ui.doubleSpinBoxGradReject_3.value(),
                      mag = 1e-12 * self.ui.doubleSpinBoxMagReject_3.value(),
                      eeg = 1e-6 * self.ui.doubleSpinBoxEEGReject_3.value(),
                      eog = 1e-6 * self.ui.doubleSpinBoxEOGReject_3.value())
        print channels
        try:
            epochs = Epochs(self.parent.experiment.raw_data, stim_channel, mag,
                            grad, eeg, stim, eog, reject, epoch_name, float(self.tmin),
                            float(self.tmax), int(self.event_id), channels)
        except:
            return #TODO error handling
        return epochs