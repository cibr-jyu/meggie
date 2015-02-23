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

import os
import ast
import gc
import traceback

from PyQt4 import QtCore,QtGui
from eogParametersDialogUi import Ui_Dialog
from code_meggie.general.caller import Caller

import fileManager

import messageBoxes

class EogParametersDialog(QtGui.QDialog):
    """
    Class containing the logic for eogParametersDialog. Used for collecting
    parameter values for calculating EOG projections.
    """
    caller = Caller.Instance()

    def __init__(self, parent):
        """
        Constructor. Initializes the dialog.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog() # Refers to class in module eogParametersDialog
        self.ui.setupUi(self)
        for subject in self.caller.experiment._subjects:
            item = QtGui.QListWidgetItem(subject._subject_name)
            self.ui.listWidgetSubjects.addItem(item)
        # Connect signals and slots
        self.ui.listWidgetSubjects.currentItemChanged.connect(self.selection_changed)
        
    def accept(self):
        """
        Collects the parameters for calculating PCA projections and passes 
        them to the caller class.
        """
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        # Calculation is prevented because of...
        error_message = ''
        
        # If calculation is done for the active subject only, the subject does
        # not need to be activated again and the raw file stays in memory.
        if self.ui.checkBoxBatch.isChecked() == False:
            self.caller.experiment._active_subject._eog_params = self.\
            collect_parameter_values(False)
            error_message = self.\
            calculate_eog(self.caller.experiment._active_subject, error_message)
            if len(error_message) > 0:
                self.messageBox = messageBoxes.shortMessageBox(error_message)
                QtGui.QApplication.restoreOverrideCursor()
                self.messageBox.show()
                #self.parent.ui.pushButtonApplyEOG.setEnabled(False)
                #self.parent.ui.checkBoxEOGComputed.setChecked(False)
            else:
                self.parent.ui.pushButtonApplyEOG.setEnabled(True)
                self.parent.ui.checkBoxEOGComputed.setChecked(True)
            self.close()
            QtGui.QApplication.restoreOverrideCursor()
            return
        recently_active_subject = self.caller.experiment._active_subject._subject_name
        subject_names = []
        for i in range(self.ui.listWidgetSubjects.count()):
            item = self.ui.listWidgetSubjects.item(i)
            #if item.text() == recently_active_subject:
            #    continue
            subject_names.append(item.text())

        # In case of batch process:
        # 1. Calculation is first done for the active subject to prevent an
        #    excessive reading of a raw file.
        if recently_active_subject in subject_names:
            error_message = self.\
            calculate_eog(self.caller.experiment._active_subject, error_message)    
        # Free the memory usage from the active subject to the batch process.
        self.caller.experiment._active_subject._working_file = None
        self.caller.experiment._active_subject = None
        
        # 2. Calculation is done for the rest of the subjects.
        for subject in self.caller.experiment._subjects:
            if subject._subject_name in subject_names:
                if subject._subject_name == recently_active_subject:
                    continue
                # Calculation is done in a separate method so that Python
                # frees memory from the earlier subject's data calculation.
                error_message = self.calculate_eog(subject, error_message)
        self.caller.experiment.activate_subject(recently_active_subject)
        if len(error_message) > 0:
            self.messageBox = messageBoxes.shortMessageBox(error_message)
            self.messageBox.show()
        self.parent._initialize_ui()
        QtGui.QApplication.restoreOverrideCursor()
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
            message = 'Select a subject to remove.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()


    def on_pushButtonApply_clicked(self, checked=None):
        """Saves parameters to selected subject's eog parameters dictionary.
        """
        if checked is None: return
        batch_checked = True
        dictionary = self.collect_parameter_values(batch_checked)
        for subject in self.caller.experiment._subjects:
            if subject._subject_name == str(self.ui.listWidgetSubjects.\
                                            currentItem().text()):
                subject._eog_params = dictionary
        
        
    def on_pushButtonApplyAll_clicked(self, checked=None):
        """Saves parameters to selected subjects' eog parameters dictionaries.
        """
        if checked is None: return
        batch_checked = True
        for i in range(self.ui.listWidgetSubjects.count()):
            for subject in self.caller.experiment._subjects:
                if str(self.ui.listWidgetSubjects.item(i).text()) == subject._subject_name:
                    subject._eog_params = self.collect_parameter_values(batch_checked)


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
        if batch_checked is False:
            raw = self.caller.experiment.active_subject.working_file
            dictionary = {'i': raw}
        
        
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
        """
        try:
            self.parent.caller.call_eog_ssp(dictionary)
        except Exception, err:
            message = 'Cannot calculate projections: ' + str(err)
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        #self.parent._initialize_ui()
        # No need to initialize the whole mainwindow again.
        self.parent.ui.pushButtonApplyEOG.setEnabled(True)
        self.parent.ui.checkBoxEOGComputed.setChecked(True)
        self.close()
        """
        return dictionary


    def selection_changed(self):
        """Unpickles parameter file from subject path and updates the values
        on dialog.
        """
        subject_name = str(self.ui.listWidgetSubjects.currentItem().text())
        # TODO: if experiment had subjects dictionary instead of list,
        # we could set:
        # subject = self.parent.experiment._subjects[subject_name]
        
        for subject in self.caller.experiment._subjects:
            if subject_name == subject._subject_name:
                try:
                    if len(subject._eog_params) > 0:
                        dic = subject._eog_params  
                    else:
                        dic = fileManager.unpickle(os.path.join(subject._subject_path, 'eog_proj.param'))
                    self.ui.doubleSpinBoxTmin.setProperty("value", dic.get('tmin'))
                    self.ui.doubleSpinBoxTmax.setProperty("value", dic.get('tmax'))
                    self.ui.spinBoxEventsID.setProperty("value", dic.get('event-id'))
                    self.ui.spinBoxLowPass.setProperty("value", dic.get('eog-l-freq'))
                    self.ui.spinBoxHighPass.setProperty("value", dic.get('eog-h-freq'))
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
                                                               dic.get('rej-eog'))
                    self.ui.lineEditBad.setProperty("value", dic.get('bads'))
                    self.ui.spinBoxStart.setProperty("value", dic.get('tstart'))
                    self.ui.spinBoxTaps.setProperty("value", dic.get('filtersize'))
                    self.ui.spinBoxJobs.setProperty("value", dic.get('n-jobs'))
                    self.ui.checkBoxEEGProj.setChecked(dic.get('avg-ref'))
                    self.ui.checkBoxSSPProj.setChecked(dic.get('no-proj'))
                    self.ui.checkBoxSSPCompute.setChecked(dic.get('average'))
                except IOError:
                    print '.param file not found.'
                    
                    # TODO:
                    self.set_default_values()


    def set_default_values(self):
        """Sets default values for dialog.
        """
        self.ui.doubleSpinBoxTmin.setProperty("value", -0.200)
        self.ui.doubleSpinBoxTmax.setProperty("value", 0.200)
        self.ui.spinBoxEventsID.setProperty("value", 998)
        self.ui.spinBoxLowPass.setProperty("value", 1)
        self.ui.spinBoxHighPass.setProperty("value", 10)
        self.ui.spinBoxGrad.setProperty("value", 2)
        self.ui.spinBoxMag.setProperty("value", 2)
        self.ui.spinBoxEeg.setProperty("value", 2)
        self.ui.spinBoxLow.setProperty("value", 1)
        self.ui.spinBoxHigh.setProperty("value", 10)
        self.ui.doubleSpinBoxGradReject.setProperty("value", 3000.00)
        self.ui.doubleSpinBoxMagReject.setProperty("value", 4000.00)
        self.ui.doubleSpinBoxEEGReject.setProperty("value", 100.00)
        self.ui.doubleSpinBoxEOGReject.setProperty("value", 250.00)
        self.ui.lineEditBad.setProperty("value", '')
        self.ui.spinBoxStart.setProperty("value", 5)
        self.ui.spinBoxTaps.setProperty("value", 2048)
        self.ui.spinBoxJobs.setProperty("value", 1)
        self.ui.checkBoxEEGProj.setChecked(False)
        self.ui.checkBoxSSPProj.setChecked(True)
        self.ui.checkBoxSSPCompute.setChecked(False)
        
        
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
        self.ui.spinBoxLowPass.setProperty("value", dic.get('eog-l-freq'))
        self.ui.spinBoxHighPass.setProperty("value", dic.get('eog-h-freq'))
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
                                           dic.get('no-proj')))
        self.ui.checkBoxSSPCompute.setChecked(ast.literal_eval(
                                           dic.get('average')))


        
    def calculate_eog(self, subject, error_message):
        """Calls caller class for calculating the projections for the given
        subject and passes errors to accept method.
        
        Keyword arguments:
        subject               -- Subject object
        error_message         -- string to store unsuccessful subject
                                 calculation
        """
        gc.collect()
        if subject._subject_name == self.caller.experiment._active_subject_name:
            subject._eog_params['i'] = self.caller.experiment._active_subject._working_file
        else:
            subject._eog_params['i'] = self.caller.experiment.\
            get_subject_working_file(subject._subject_name)
        try:
            event_checker = self.caller.call_eog_ssp(subject._eog_params)
            if event_checker == -1:
                return error_message
        except Exception:
            tb = traceback.format_exc()
            #error_message += '\n' + subject._subject_name + ': ' + str(err)
            error_message += '\nAn error occurred during calculation for subject: ' + \
            subject._subject_name + '. Proceed with care and check parameters!\n\n' + \
            str(tb)
            if self.ui.checkBoxBatch.isChecked() == True:
                subject._working_file = None
            del subject._eog_params['i']
            return error_message
        try:
            del subject._eog_params['i']
        except Exception:
            pass
        fileManager.pickleObjectToFile(subject._eog_params, os.path.join(subject._subject_path, 'eog_proj.param'))
        if self.ui.checkBoxBatch.isChecked() == True:
            subject._working_file = None
        return error_message

        