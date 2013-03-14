import sys
from PyQt4 import QtCore, QtGui
from infodialog import Ui_infoDialog
from root.controller.measurementInfo import MeasurementInfo
import mne


class InfoDialog(QtGui.QMainWindow):
    def __init__(self, raw):
        QtGui.QMainWindow.__init__(self)
        
        self.ui = Ui_infoDialog()
        self.ui.setupUi(self)
        self.ui.tab_list = []
        button = self.ui.ButtonClose       
        button.clicked.connect(self.button_clicked)
        #raw = mne.fiff.Raw('/usr/local/bin/ParkkosenPurettu/meg/jn/jn_multimodal01_raw_sss.fif')
        mi = MeasurementInfo(raw)
        
        self.ui.labelDateValue.setText(mi.get_date())
        self.ui.labelEEGValue.setText(mi.get_EEG_channels())
        self.ui.labelGradMEGValue.setText(mi.get_grad_channels())
        self.ui.labelHighValue.setText(mi.get_high_pass())
        self.ui.labelLowValue.setText(mi.get_low_pass())
        self.ui.labelMagMEGValue.setText(mi.get_mag_channels())
        self.ui.labelSamplesValue.setText(mi.get_sampling_freq())
    
    def button_clicked(self):
        self.close()
        

def main():
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
