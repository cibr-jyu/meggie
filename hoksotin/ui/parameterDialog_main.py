'''
Created on Mar 19, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from epochParameterDialog_UI import Ui_ParameterDialog

from measurementInfo import MeasurementInfo
from enaml.components.push_button import PushButton

from epochs import Epochs

class ParameterDialog(QtGui.QDialog):
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
        self.ui = Ui_ParameterDialog()
        self.ui.setupUi(self)
        stim_channels = MeasurementInfo(parent.experiment.raw_data).stim_channel_names
        print stim_channels
        keys = map(str, parent.experiment.event_set.keys())
        print keys
        self.ui.comboBoxStimulus.addItems(stim_channels)
        self.ui.comboBoxEventID.addItems(keys)
        self.ui.lineEditName.setText('Event' + str(self.__class__.index))
        """
        self.ui.lineEditEventID.setText('5')
        self.ui.lineEditTmin.setText('-0.2')
        self.ui.lineEditTmax.setText('0.5')
        """   
        
        """        
    def on_browseButton_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/usr/local/bin/ParkkosenPurettu/meg/jn')
        self.fileEdit.setText(self.fname)
        """
        
    def create_epochs(self):
        stim_channel = str(self.ui.comboBoxStimulus.currentText())
        self.event_id = int(self.ui.comboBoxEventID.currentText())
        tmin = float(self.ui.doubleSpinBoxTmin.value())
        tmax = float(self.ui.doubleSpinBoxTmax.value())
        epoch_name = self.ui.lineEditName.text()
        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        try:
            epochs = Epochs(self.parent.raw, stim_channel, mag, grad, eeg,
                            stim, eog, epoch_name, float(tmin),
                            float(tmax), int(self.event_id))
        except:
            return #TODO error handling
        return epochs
        
    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None: return # Standard workaround
        epochs = self.create_epochs()
        print epochs
        self.__class__.index += 1
        #id = self.ui.spinBoxEventID.value()
        if isinstance(epochs, Epochs):
            event_set = '(ID:' + str(self.event_id) + ', ' + str(self.parent.experiment.event_set.get(self.event_id)) + ' events)'
            item = QtGui.QListWidgetItem(self.ui.lineEditName.text() + ' ' + event_set)
            item.setData(1, epochs)
            self.ui.listWidgetEvents.addItem(item)
            self.ui.lineEditName.setText('Event' + str(self.__class__.index))
            self.ui.listWidgetEvents.setCurrentItem(item) #select the last item
            self.ui.pushButtonRemove.setEnabled(True)
        #print self.parent.experiment.event_set
        
    def on_pushButtonRemove_clicked(self, checked=None):
        if checked is None: return # Standard workaround
        row = self.ui.listWidgetEvents.currentRow()
        self.ui.listWidgetEvents.takeItem(row)
        if self.ui.listWidgetEvents.currentRow() < 0:
            self.ui.pushButtonRemove.setEnabled(False)
        
        
    def accept(self):
        """
        Called when the OK button is pressed.
        """
        print self.ui.listWidgetEvents.currentItem().data(1).toPyObject()
        self.close()        
        """
        self.fname = self.fileEdit.text()
        stim_channel = str(self.ui.comboBoxStimulus.currentText())
        event_id = self.ui.lineEditEventID.text()
        tmin = self.ui.lineEditTmin.text()
        tmax = self.ui.lineEditTmax.text()
        reject = self.ui.lineEditReject.text()
        meg = self.ui.checkBoxMeg.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        self.close()
        self.parent.epochs = CreateEpochs(self.parent.raw, event_id,
                                          stim_channel, tmin, tmax, reject,
                                          meg, eeg, stim, eog)
        
        """
        