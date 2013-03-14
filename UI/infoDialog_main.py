import sys
from PyQt4 import QtCore, QtGui
from infoDialog_Ui import Ui_infoDialog
import measurementInfo
import mne


class infoDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.ui = Ui_infoDialog()
        self.ui.setupUi(self)
        self.ui.tab_list = []
        
        self.setLabelTestValues()
    
    def on_ButtonClose_clicked(self):
        self.close()
        
    def setLabelTestValues(self):
            
        raw = mne.fiff.Raw('/home/kpaliran/Hoksotin/parkkosenpaketti/meg/jn/jn_multimodal01_raw_sss.fif')
        #raw = mne.fiff.Raw('/usr/local/bin/ParkkosenPurettu/meg/jn/jn_multimodal01_raw_sss.fif')
        mi = measurementInfo.MeasurementInfo(raw)
        
        self.ui.labelDateValue.setText(mi.get_date())
        self.ui.labelEEGValue.setText(mi.get_EEG_channels())
        self.ui.labelGradMEGValue.setText(mi.get_grad_channels())
        self.ui.labelHighValue.setText(mi.get_high_pass())
        self.ui.labelLowValue.setText(mi.get_low_pass())
        self.ui.labelMagMEGValue.setText(mi.get_mag_channels())
        self.ui.labelSamplesValue.setText(mi.get_sampling_freq())
    
        

def main():
    app = QtGui.QApplication(sys.argv)
    window=infoDialog()
    
    
    
    window.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
