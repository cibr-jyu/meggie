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
'''
Created on 27.8.2015

@author: Jaakko Leppakangas
'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialogButtonBox, QListWidgetItem

from meggie.code_meggie.general.caller import Caller

from meggie.ui.epoching.groupEpochingDialogUi import Ui_GroupEpochDialog
from meggie.ui.general import messageBoxes

class GroupEpochingDialog(QtGui.QDialog):
    """
    Class containing the logic for creating epochs for multiple subjects.
    """

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_GroupEpochDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText('Start '
                                                              'computation')
        self.caller = Caller.Instance()
        subjects = self.caller.experiment.get_subjects()
        self.ui.listWidgetSubjects.setSelectionMode(QtGui.\
                                    QAbstractItemView.MultiSelection)
        for subject in subjects:
            item = QListWidgetItem(subject.subject_name)
            self.ui.listWidgetSubjects.addItem(item)
            item.setSelected(True)

    def accept(self, *args, **kwargs):
        """
        Start computing the epochs.
        """
        items = self.ui.listWidgetSubjects.selectedItems()
        subjects = [str(item.text()) for item in items]
        epoch_name = str(self.ui.lineEditCollectionName.text())
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        stim = self.ui.checkBoxStim.isChecked()
        event_id = self.ui.spinBoxEventId.value()
        mask = self.ui.spinBoxMask.value()
        event_name = str(self.ui.lineEditName.text())
        if event_name == '':
            msg = 'Event name cannot be empty!'
            mBox = messageBoxes.shortMessageBox(msg)
            mBox.exec_()
            return
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        grad = self.ui.doubleSpinBoxGradReject_3.value() * 1e-13 if\
                self.ui.checkBoxGrad.isChecked() else None
        mag = self.ui.doubleSpinBoxMagReject_3.value() * 1e-15 if\
                self.ui.checkBoxMag.isChecked() else None
        eeg = self.ui.doubleSpinBoxEEGReject_3.value() * 1e-6 if\
                self.ui.checkBoxEeg.isChecked() else None
        eog = self.ui.doubleSpinBoxEOGReject_3.value() * 1e-6 if\
                self.ui.checkBoxEog.isChecked() else None
        self.caller.batchEpoch(subjects, epoch_name, tmin, tmax, stim,
                               event_id, mask, event_name, grad, mag, eeg, eog)
        QtGui.QApplication.restoreOverrideCursor()
        self.close()
