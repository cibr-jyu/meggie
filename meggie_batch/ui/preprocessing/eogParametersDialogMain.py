# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Apr 12, 2013

@author: Jaakko Leppakangas
Contains the EogParametersDialog used for collecting parameter values for
calculating EOG projections.
"""
from PyQt4 import QtCore,QtGui
from eogParametersDialogUi import Ui_Dialog

from caller import Caller

import messageBoxes

class EogParametersDialog(QtGui.QDialog):
    """
    Class containing the logic for eogParametersDialog. Used for collecting
    parameter values for calculating EOG projections.
    """


    def __init__(self, parent):
        """
        Constructor. Initializes the dialog.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog() # Refers to class in module eogParametersDialog
        self.ui.setupUi(self)
        
    def accept(self):
        """
        Collects the parameters for calculating PCA projections and passes 
        them to the caller class.
        """
        dictionary = {'i': self.parent.experiment.active_subject.working_file}
        
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
        
        # Uses the caller related to mainwindow
        try:
            self.parent.caller.call_eog_ssp(dictionary)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Cannot calculate ' +
                                                   'projections: ' + str(err))
            self.messageBox.show()
            return
        
        #self.parent._initialize_ui()
        # No need to initialize the whole mainwindow again.
        self.parent.ui.pushButtonApplyEOG.setEnabled(True)
        self.parent.ui.checkBoxEOGComputed.setChecked(True)
        self.close()