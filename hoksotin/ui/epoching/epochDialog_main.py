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
        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        stim_channel = self.parent.parent.experiment.stim_channel
        reject = dict(grad = 1e-12 * self.ui.doubleSpinBoxGradReject_3.value(),
                      mag = 1e-12 * self.ui.doubleSpinBoxMagReject_3.value(),
                      eeg = 1e-6 * self.ui.doubleSpinBoxEEGReject_3.value(),
                      eog = 1e-6 * self.ui.doubleSpinBoxEOGReject_3.value())
        events = []
        category = dict()
        for index in xrange(self.parent.ui.listWidgetEvents.count()):
            event = self.parent.ui.listWidgetEvents.item(index).data(1).toPyObject()
            events.append(events)
            category[self.parent.ui.listWidgetEvents.item(index).data(2).toPyObject()] = event[2]
            
        try:
            epochs = Epochs(self.parent.experiment.working_file, events,
                            stim_channel, mag, grad, eeg, stim, eog, reject,
                            epoch_name, category, float(self.tmin),
                            float(self.tmax))
        except:
            return #TODO error handling
        print epochs
        return epochs