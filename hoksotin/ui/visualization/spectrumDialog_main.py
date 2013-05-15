'''
Created on May 15, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui

from spectrumDialog_Ui import Ui_DialogSpectrum

class SpectrumDialog(QtGui.QDialog):
    '''
    Dialog to get the channel from the user and plot the magnitude spectrum.
    '''


    def __init__(self, parent):
        '''
        Constructor
        Keyword arguments:
        parent        -- Parent of this object.
        '''
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogSpectrum()
        self.ui.setupUi(self)
        ch_names = self.parent.experiment.working_file.ch_names
        self.ui.comboBoxChannel.addItems(ch_names)
        
    def accept(self):
        ch_index = self.ui.comboBoxChannel.currentIndex()
        raw = self.parent.experiment.working_file
        print ch_index
        self.parent.caller.magnitude_spectrum(raw, ch_index)
        self.close()