import sys
from PyQt4 import QtCore, QtGui
from infoDialog_Ui import Ui_infoDialog
from measurementInfo import MeasurementInfo
import mne


class InfoDialog(QtGui.QDialog):
    def __init__(self, raw, info, create_window):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        info          -- Ui object that receives the info data
        create_window -- Boolean that tells if a new window is created
        """
        QtGui.QDialog.__init__(self)
        self.raw = raw
        self.ui = info
        if create_window:
            self.ui.setupUi(self)
            self.ui.tab_list = []
        
        self.setLabelTestValues()
    
    def on_ButtonClose_clicked(self):
        self.close()
        
    def setLabelTestValues(self):
        
        #raw = mne.fiff.Raw('/home/kpaliran/Hoksotin/parkkosenpaketti/meg/jn/jn_multimodal01_raw_sss.fif')
        #raw = mne.fiff.Raw('/usr/local/bin/ParkkosenPurettu/meg/jn/jn_multimodal01_raw_sss.fif')
        self.mi = MeasurementInfo(self.raw)
        
        self.ui.labelDateValue.setText(self.mi.get_date())
        self.ui.labelEEGValue.setText(str(self.mi.get_EEG_channels()))
        self.ui.labelGradMEGValue.setText(str(self.mi.get_grad_channels()))
        self.ui.labelHighValue.setText(str(self.mi.get_high_pass()))
        self.ui.labelLowValue.setText(str(self.mi.get_low_pass()))
        self.ui.labelMagMEGValue.setText(str(self.mi.get_mag_channels()))
        self.ui.labelSamplesValue.setText(str(self.mi.get_sampling_freq()))
        self.ui.labelSubjectValue.setText(self.mi.get_subject_name())
    
        
"""
def main():
    app = QtGui.QApplication(sys.argv)
    window=infoDialog()
    
    
    
    window.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
"""