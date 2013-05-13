'''
Created on Apr 30, 2013

@author: jaeilepp
'''
import messageBox
from epochDialog_Ui import Ui_Dialog

from epochs import Epochs

from PyQt4 import QtCore,QtGui

import numpy as np

class EpochDialog(QtGui.QDialog):
    """
    class containing the logic for epochDialog
    """
    index = 1

    def __init__(self, parent):
        """
        Constructor
        """
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
        
        reject = dict()
        if mag:
            reject['mag'] = 1e-12 * self.ui.doubleSpinBoxMagReject_3.value()
        if grad:
            reject['grad'] = 1e-12 * self.ui.doubleSpinBoxGradReject_3.value()
        if eeg:
            reject['eeg'] = eeg = 1e-6 * self.ui.doubleSpinBoxEEGReject_3.value()
        if eog:
            reject['eog'] = eog = 1e-6 * self.ui.doubleSpinBoxEOGReject_3.value()
        
        """
        reject = dict(grad = 1e-12 * self.ui.doubleSpinBoxGradReject_3.value(),
                      mag = 1e-12 * self.ui.doubleSpinBoxMagReject_3.value(),
                      eeg = 1e-6 * self.ui.doubleSpinBoxEEGReject_3.value(),
                      eog = 1e-6 * self.ui.doubleSpinBoxEOGReject_3.value())
        """
        """
        Reads the given event names as categories.
        """
        events = np.ndarray((self.parent.ui.listWidgetEvents.count(),3), int)
        category = dict()
        for index in xrange(self.parent.ui.listWidgetEvents.count()):
            event = (self.parent.ui.listWidgetEvents.item(index).data(32).
                     toPyObject())
            events[index] = (event)
            #print str(self.parent.ui.listWidgetEvents.item(index).data(33).toPyObject())
            category[str(self.parent.ui.listWidgetEvents.item(index).data(33).
                         toPyObject())] = event[2]
        try:
            epochs = Epochs(self.parent.parent.experiment.working_file, events,
                            mag, grad, eeg, stim, eog, reject, category,
                            float(self.tmin), float(self.tmax))
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Could not create epochs: '
                                                   + str(err))
            self.messageBox.exec_()
            return
        #for index in xrange(epochs):
        
        """
        Add's the epochs to the mainWindow's list.
        """
        item_string = ''
        for key, value in epochs.epochs.event_id.iteritems():
            item_string += key + '=' + str(value) + ' ' 
        item = QtGui.QListWidgetItem(item_string)
        item.setData(32, epochs)
        self.parent.parent.widget.ui.listWidgetEpochs.addItem(item)
        self.parent.parent.widget.ui.listWidgetEpochs.setCurrentItem(item)
        self.close()
        #return epochs