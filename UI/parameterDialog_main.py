'''
Created on Mar 19, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from epochParameterDialog_UI import Ui_ParameterDialog

from measurementInfo import MeasurementInfo
from createEpochs import CreateEpochs
class ParameterDialog(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, raw):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ParameterDialog()
        self.ui.setupUi(self)
        self.fileEdit = self.ui.FilePathLineEdit
        self.raw = raw
        stim_channels = MeasurementInfo(raw).get_stim_channel_names()
        print stim_channels
        self.ui.comboBoxStimulus.addItems(stim_channels)
                
    def on_browseButton_clicked(self, checked=None):
        """
        Called when Browse-button is pressed. Opens a file browser.        
        """
        if checked is None: return # Standard workaround for file dialog opening twice
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/usr/local/bin/ParkkosenPurettu/meg/jn')
        self.fileEdit.setText(self.fname)
        
    def accept(self):
        """
        Called when the OK button is pressed.
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
        CreateEpochs(self.raw, event_id, stim_channel, tmin, tmax, reject,
                     meg, eeg, stim, eog)
        self.close()
        
        