"""
Created on Apr 16, 2013

@author: Jaakko Leppakangas
"""
import os
import ast

from PyQt4 import QtCore,QtGui
from ecgParametersDialog_Ui import Ui_Dialog

from caller import Caller
from measurementInfo import MeasurementInfo

import messageBox

class EcgParametersDialog(QtGui.QDialog):
    """
    Class containing the logic for ecgParametersDialog.
    """


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        stim_channels = MeasurementInfo(parent.experiment.raw_data). \
        MEG_channel_names
        self.ui.comboBoxECGChannel.addItems(stim_channels)
        
        """ 
        If the dialog has been opened previously, reads the previous
        parameters from a parameter file into a dictionary. The creation of the
        parameter file is handled by the caller.
        TODO Should call with a list of globstrings, as the mne script this 
        dialog evokes can produce files ending with "ecg_proj.fif" or
        "ecg_ave_proj.fif".
        """
        
        paramdict = parent.experiment.parse_parameter_file('ecgproj')
        self.set_previous_values(paramdict)     
        
    def set_previous_values(self, dic):
        # If no parameter file existed, return
        if ( dic == None ): return
        
        """
        Sets the values in the newly created dialog to those in the dictionary
        given. See the *** for the specifics about the dictionary.
        TODO exact source of dictionary information
        """
        self.ui.doubleSpinBoxTmin.setProperty("value", dic.get('tmin'))
        self.ui.doubleSpinBoxTmax.setProperty("value", dic.get('tmax'))
        self.ui.spinBoxEventsID.setProperty("value", dic.get('event-id'))
        self.ui.spinBoxLowPass.setProperty("value", dic.get('ecg-l-freq'))
        self.ui.spinBoxHighPass.setProperty("value", dic.get('ecg-h-freq'))
        self.ui.spinBoxGrad.setProperty("value", dic.get('n-grad'))
        self.ui.spinBoxMag.setProperty("value", dic.get('n-mag'))
        self.ui.spinBoxEeg.setProperty("value", dic.get('n-eeg'))
        self.ui.spinBoxLow.setProperty("value", dic.get('l-freq'))
        self.ui.spinBoxHigh.setProperty("value", dic.get('h-freq'))
        self.ui.doubleSpinBoxGradReject.setProperty("value",
                                                     dic.get('rej-grad'))
        self.ui.doubleSpinBoxMagReject.setProperty("value",
                                                     dic.get('rej-mag'))
        self.ui.doubleSpinBoxEEGReject.setProperty("value", 
                                                   dic.get('rej-eeg'))
        self.ui.doubleSpinBoxEOGReject.setProperty("value", 
                                                   dic.get('reg-eog'))
        self.ui.lineEditBad.setProperty("value", dic.get('bads'))
        self.ui.spinBoxStart.setProperty("value", dic.get('tstart'))
        self.ui.spinBoxTaps.setProperty("value", dic.get('filtersize'))
        self.ui.spinBoxJobs.setProperty("value", dic.get('njobs'))
        self.ui.checkBoxEEGProj.setChecked(ast.literal_eval(
                                           dic.get('avg-ref')))
        self.ui.checkBoxSSPProj.setChecked(ast.literal_eval(
                                           dic.get('avg-ref')))
        self.ui.checkBoxSSPCompute.setChecked(ast.literal_eval(
                                           dic.get('no-proj')))
        # TODO get the selected channel from the combobox
        #self.ui.comboBoxECGChannel.set  dic.get('average')))
                                           

    def accept(self):
        raw = self.parent.experiment.working_file
        dictionary = {'i': raw}
        
        tmin = self.ui.doubleSpinBoxTmin.value()
        dictionary['tmin'] = tmin
        
        tmax = self.ui.doubleSpinBoxTmax.value()
        dictionary['tmax'] = tmax
        
        event_id = self.ui.spinBoxEventsID.value()
        dictionary['event-id'] = event_id
        
        low_freq = self.ui.spinBoxLowPass.value()
        dictionary['ecg-l-freq'] = low_freq
        
        high_freq = self.ui.spinBoxHighPass.value()
        dictionary['ecg-h-freq'] = high_freq
        
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
        
        qrs = self.ui.doubleSpinBoxQrs.value()
        dictionary['qrs'] = qrs
        
        # Split the string into a list.
        bads = map(str.strip, str(self.ui.lineEditBad.text()).split(','))
        dictionary['bads'] = bads
        
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
        
        dictionary['ch_name'] = self.ui.comboBoxECGChannel.currentText()
            
        # Uses the caller related to mainwindow
        try:
            self.parent.caller.call_ecg_ssp(dictionary)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Cannot calculate ' +
                    'projections: ' + str(err) + '\nCheck parameters.')
            self.messageBox.show()
            return
        self.parent._initialize_ui()
        self.close()

