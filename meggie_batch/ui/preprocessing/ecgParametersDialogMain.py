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
Created on Apr 16, 2013

@author: Kari Aliranta, Jaakko Leppakangas
Contains the EcgParametersDialog-class used for collecting parameter values
for calculating ECG projections.
"""
import os
import ast

from PyQt4 import QtCore,QtGui
from ecgParametersDialogUi import Ui_Dialog

from fileManager import FileManager
from caller import Caller
from measurementInfo import MeasurementInfo

import messageBox

class EcgParametersDialog(QtGui.QDialog):
    """
    Class containing the logic for ecgParametersDialog. it collects parameter
    values for calculating ECG projections.
    """


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        MEG_channels = MeasurementInfo(parent.experiment.active_subject.working_file). \
        MEG_channel_names
        self.ui.comboBoxECGChannel.addItems(MEG_channels)
        for subject in self.parent.experiment._subjects:
            item = QtGui.QListWidgetItem(subject._subject_name)
            self.ui.listWidgetSubjects.addItem(item)
        """ 
        If the dialog has been opened previously, reads the previous
        parameters from a parameter file into a dictionary. The creation of the
        parameter file is handled by the caller.
        """
        
        #paramdict = parent.experiment.parse_parameter_file('ecgproj')
        #self.set_previous_values(paramdict)     
        
    def set_previous_values(self, dic):
        """
        Sets the initial values of the dialog widgets to those used when the
        dialog was used (OK button was clicked) the previous time.
        
        Keyword arguments:
        dic    -- the dictionary with previous values of fields, checkboxes, 
                  etc.
        """
        # If no parameter file exists, return
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
        """
        Collects the parameters for calculating PCA projections and pass them
        to the caller class.
        """
        
        # TODO: Add browser for saved param files.
        # TODO: Add possibility to save param files with user chosen name.
        
        
        # If batch processing is not enabled, the raw is taken from the active
        # subject.
        if self.ui.checkBoxBatch.isChecked() == False:
            dictionary = self.collect_parameter_values(False)
            # Uses the caller related to main window
            try:
                # Returns -1 if no events found with current settings.
                event_checker = self.parent.caller.call_ecg_ssp(dictionary)
                if event_checker == -1:
                    return
            except Exception, err:
                error_message = 'Cannot calculate projections: ' + str(err) + \
                '\nCheck parameters.'
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText(error_message)
                self.messageBox.show()
                return
            # No need to initialize the whole main window again.
            self.parent.ui.pushButtonApplyECG.setEnabled(True)
            self.parent.ui.checkBoxECGComputed.setChecked(True)
        
        else:
            for i in range(self.ui.listWidgetSubjects.count()):
                for subject in self.parent.experiment._subjects:
                    if subject._subject_name == str(self.ui.listWidgetSubjects.\
                                                    item(i).text()):
                        # Reads and returns the raw file.
                        raw = self.parent.experiment.\
                        get_subject_working_file(subject._subject_name)
                        subject._ecg_params['i'] = raw
                        
                                                
                        # Fixes the ecg_params ch_name to match with the raw
                        # file ch_name. Assume that if the first channel name
                        # has/doesn't have whitespace the same applies for the
                        # rest of the channel names.
                        ch_names = MeasurementInfo(raw).MEG_channel_names
                        if ch_names[0][3] is not subject._ecg_params['ch_name'][3]:
                            # subjec._ecg_params['ch_name'] is a QString object.
                            ch_name = str(subject._ecg_params['ch_name'])
                            ch_name = ch_name.replace(' ', '')
                            if ch_names[0][3] is not ch_name[3]:
                                # TODO: Add more options if problems occur,
                                # for example ECG channel would mix up with
                                # replace('C', 'C ').
                                
                                # Replaces MEG and EOG
                                ch_name = ch_name.replace('G', 'G ')
                                # Replaces STI
                                ch_name = ch_name.replace('I', 'I ')
                                # Replaces MISC
                                ch_name = ch_name.replace('C', 'C ')
                            subject._ecg_params['ch_name'] = ch_name
                        try:
                            event_checker = self.parent.caller.\
                            call_ecg_ssp(subject._ecg_params)
                            if event_checker == -1:
                                return
                            if subject == self.parent.experiment._active_subject:
                                # Update the main window if also the active
                                # subject is processed.
                                self.parent.ui.pushButtonApplyECG.setEnabled(True)
                                self.parent.ui.checkBoxECGComputed.setChecked(True)
                        except Exception, err:
                            error_message = 'Cannot calculate projections: ' + \
                            str(err) + '\nCheck parameters.'
                            self.messageBox = messageBox.AppForm()
                            self.messageBox.labelException.\
                            setText(error_message)
                            self.messageBox.show()
                            
                        # Remove extra raw file from memory
                        del subject._ecg_params['i']
                        f = FileManager()
                        f.pickle(subject._ecg_params, os.path.join(subject._subject_path, 'ecg_proj.params'))
        self.close()

    def on_pushButtonRemove_clicked(self, checked=None):
        """Removes subject from the list of subjects to be processed.
        """
        if checked is None: return
        item = self.ui.listWidgetSubjects.currentItem()
        if self.ui.listWidgetSubjects.currentItem() is not None:
            row = self.ui.listWidgetSubjects.row(item)
            self.ui.listWidgetSubjects.takeItem(row)
        else:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Select a subject to remove.')
            self.messageBox.show()
    
    def on_pushButtonApply_clicked(self, checked=None):
        """Saves parameters to selected subject's ecg parameters dictionary.
        """
        if checked is None: return
        batch_checked = True
        dictionary = self.collect_parameter_values(batch_checked)
        for subject in self.parent.experiment._subjects:
            if subject._subject_name == str(self.ui.listWidgetSubjects.\
                                            currentItem().text()):
                subject._ecg_params = dictionary
        
    def on_pushButtonApplyAll_clicked(self, checked=None):
        """Saves parameters to selected subjects' ecg parameters dictionaries.
        """
        if checked is None: return
        batch_checked = True
        
        for i in range(self.ui.listWidgetSubjects.count()):
            for subject in self.parent.experiment._subjects:
                if str(self.ui.listWidgetSubjects.item(i).text()) == subject._subject_name:
                    subject._ecg_params = self.collect_parameter_values(batch_checked)
        
    def collect_parameter_values(self, batch_checked):
        """Collects parameter values from dialog.
        
        Keyword arguments:
        batch_checked    -- True if batch processing is enabled
        """
        
        """
        Can't set raw if batching is enabled:
        1. would pickle a huge dictionary
        2. would have to read raw every time when creating params dictionaries
        """
        dictionary = dict()
        if batch_checked:
            pass
        else:
            raw = self.parent.experiment.active_subject.working_file
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

        return dictionary
        