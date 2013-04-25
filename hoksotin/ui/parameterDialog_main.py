'''
Created on Mar 19, 2013

@author: Jarkko Leppäkangas, Atte Rautio
'''
from PyQt4 import QtCore,QtGui
from parameterDialog_ui import Ui_ParameterDialog

from measurementInfo import MeasurementInfo
#from enaml.components.push_button import PushButton

from epochs import Epochs
import brainRegions

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
        stim_channels = MeasurementInfo(
                                        parent.experiment.raw_data
                                        ).stim_channel_names
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
        
    def create_eventlist(self):
        stim_channel = str(self.ui.comboBoxStimulus.currentText())
        self.event_id = int(self.ui.comboBoxEventID.currentText())
        self.tmin = float(self.ui.doubleSpinBoxTmin.value())
        self.tmax = float(self.ui.doubleSpinBoxTmax.value())
        epoch_name = self.ui.lineEditName.text()
        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        channels = self.check_channels()
        reject = dict(grad = 1e-12 * self.ui.doubleSpinBoxGradReject_3,
                      mag = 1e-12 * self.ui.doubleSpinBoxMagReject_3,
                      eeg = 1e-6 * self.ui.doubleSpinBoxEEGReject_3,
                      eog = 1e-6 * self.ui.doubleSpinBoxEOGReject_3)
        print channels
        try:
            epochs = Epochs(self.parent.experiment.raw_data, stim_channel, mag,
                            grad, eeg, stim, eog, epoch_name, float(self.tmin),
                            float(self.tmax), int(self.event_id), channels,
                            reject)
        except:
            return #TODO error handling
        return epochs
        
    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None: return # Standard workaround
        epochs = self.create_eventlist()
        print epochs
        self.__class__.index += 1
        if isinstance(epochs, Epochs):
            event_set = '(ID:' + str(self.event_id) + ', ' + \
                str(self.parent.experiment.event_set.get(self.event_id)) + \
                ' events, start: ' + str(self.tmin) + ', end: ' + \
                str(self.tmax) + ')'
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
        
        for index in xrange(self.ui.listWidgetEvents.count()):
            item = QtGui.QListWidgetItem(self.ui.listWidgetEvents.item(index).text())
            item.setData(1, self.ui.listWidgetEvents.item(index).data(1).toPyObject())
            self.parent.ui.listWidgetEvents.addItem(item)
            
        
        #print self.ui.listWidgetEvents.currentItem().data(1).toPyObject()
        self.close()
        
    def check_channels(self):
        if self.ui.comboBoxChannelGroup.currentText() == 'Vertex':
            return ['MEG ' + str(x) for x in brainRegions.vertex]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-temporal':
            return ['MEG ' + str(x) for x in brainRegions.left_temporal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-temporal':
            return ['MEG ' + str(x) for x in brainRegions.right_temporal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-parietal':
            return ['MEG ' + str(x) for x in brainRegions.left_parietal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-parietal':
            return ['MEG ' + str(x) for x in brainRegions.right_parietal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-occipital':
            return ['MEG ' + str(x) for x in brainRegions.left_occipital]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-occipital':
            return ['MEG ' + str(x) for x in brainRegions.right_occipital]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-frontal':
            return ['MEG ' + str(x) for x in brainRegions.left_frontal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-frontal':
            return ['MEG ' + str(x) for x in brainRegions.right_frontal]
        
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
        