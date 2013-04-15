import sys
from PyQt4 import QtCore, QtGui
from infoDialog_Ui import Ui_infoDialog
from measurementInfo import MeasurementInfo
import mne


class InfoDialog(QtGui.QDialog):
    '''
    Dialog to get and show the info from the raw file. Can be used to direct
    the extracted information from the file to the dialog itself or some
    other ui with similar element names. Currently used for setting the
    parameters in the Raw tab of the mainWindow. 
    '''
    def __init__(self, raw, targetUi, create_window):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        targetUi      -- Ui object that receives the info data
        create_window -- Boolean that tells if a new window is created
        """
        QtGui.QDialog.__init__(self)
        self.raw = raw
        self.ui = targetUi
        if create_window:
            self.ui.setupUi(self)
            self.ui.tab_list = []
        
        self._setLabelTestValues()
    
    def on_ButtonClose_clicked(self):
        self.close()
        
    def _setLabelTestValues(self):
        
        self.mi = MeasurementInfo(self.raw)
        
        self.ui.labelDateValue.setText(self.mi.date)
        self.ui.labelEEGValue.setText(str(self.mi.EEG_channels))
        self.ui.labelGradMEGValue.setText(str(self.mi.grad_channels))
        self.ui.labelHighValue.setText(str(self.mi.high_pass))
        self.ui.labelLowValue.setText(str(self.mi.low_pass))
        self.ui.labelMagMEGValue.setText(str(self.mi.mag_channels))
        self.ui.labelSamplesValue.setText(str(self.mi.sampling_freq))
        self.ui.labelSubjectValue.setText(self.mi.subject_name)
    
        
"""
def main():
    app = QtGui.QApplication(sys.argv)
    window=infoDialog()
    
    
    
    window.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
"""