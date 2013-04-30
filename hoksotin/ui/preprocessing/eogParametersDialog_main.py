'''
Created on Apr 12, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from eogParametersDialog_Ui import Ui_Dialog

from caller import Caller

class EogParametersDialog(QtGui.QDialog):


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog() # Refers to class in module eogParametersDialog
        self.ui.setupUi(self)
        
    def accept(self):
        dictionary = {'i': self.parent.experiment.raw_data}
        tmin = self.ui.doubleSpinBoxTmin.value()
        dictionary['tmin'] = tmin
        tmax = self.ui.doubleSpinBoxTmax.value()
        dictionary['tmax'] = tmax
        event_id = self.ui.spinBoxEventsID.value()
        dictionary['event-id'] = event_id
        low_freq = self.ui.spinBoxLowPass.value()
        dictionary['eog-l-freq'] = low_freq
        high_freq = self.ui.spinBoxHighPass.value()
        dictionary['eog-h-freq'] = high_freq
        grad = self.ui.spinBoxGrad.value()
        dictionary['n-grad'] = grad
        mag = self.ui.spinBoxMag.value()
        dictionary['n-mag'] = mag
        eeg = self.ui.spinBoxEeg.value()
        dictionary['n-eeg'] = eeg
        filter_low = self.ui.spinBoxLow.value()
        dictionary['l-freq'] = filter_low
        filter_high = self.ui.spinBoxHigh.value()
        dictionary['h-freq'] = filter_high
        rej_grad = self.ui.doubleSpinBoxGradReject.value()
        dictionary['rej-grad'] = rej_grad
        rej_mag = self.ui.doubleSpinBoxMagReject.value()
        dictionary['rej-mag'] = rej_mag
        rej_eeg = self.ui.doubleSpinBoxEEGReject.value()
        dictionary['rej-eeg'] = rej_eeg
        rej_eog = self.ui.doubleSpinBoxEOGReject.value()
        dictionary['rej-eog'] = rej_eog
        bads = self.ui.lineEditBad.text()
        
        start = self.ui.spinBoxStart.value()
        dictionary['tstart'] = start
        taps = self.ui.spinBoxTaps.value()
        dictionary['filtersize'] = taps
        njobs = self.ui.spinBoxJobs.value()
        dictionary['n-jobs'] = njobs
        eeg_proj = self.ui.checkBoxEEGProj.checkState() == QtCore.Qt.Checked
        dictionary['avg-ref'] = eeg_proj
        excl_ssp = self.ui.checkBoxSSPProj.checkState() == QtCore.Qt.Checked
        dictionary['no-proj'] = excl_ssp
        comp_ssp = self.ui.checkBoxSSPCompute.checkState()==QtCore.Qt.Checked
        dictionary['average'] = comp_ssp
        
        # Uses the caller related to mainwindow
        self.parent.caller.call_eog_ssp(dictionary)
        self.parent._initialize_ui()
        self.close()
        