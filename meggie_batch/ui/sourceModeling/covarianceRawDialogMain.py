'''
Created on 7.1.2015

@author: Kari Aliranta
'''

from PyQt4 import QtGui
from covarianceRawDialogUi import Ui_covarianceRawDialog

import messageBoxes
import fileManager
import os
from infoDialogUi import Ui_infoDialog
from infoDialogMain import InfoDialog


class CovarianceRawDialog(QtGui.QDialog):
    """
    The class containing the logic for the dialog for collecting the
    parameters computing the noise covariance for a raw file.
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_covarianceRawDialog()
        self.ui.setupUi(self)
        self.ui.listViewSubjects.setModel(self.parent.subjectListModel)
           
           
    def accept(self):
        """
        Gets the arguments from the gui and passes them to caller for computing
        the noise covariance matrix. 
        """
        pdict = dict()
        
        if self.ui.buttonGroupRawFile.checkedButton() == \
        self.ui.radioButtonSubjectList:
            selIndexes = self.ui.listViewSubjects.selectedIndexes()
            subjectName = selIndexes[0].data()
            pdict['rawsubjectname'] = subjectName
            pdict['rawfilepath'] = None 
        else:
            pdict['rawfilepath'] = self.ui.lineEditRawFile.text()
            pdict['rawsubjectname'] = None
        
        pdict['starttime'] = self.ui.doubleSpinBoxStartTime.value()
        pdict['endtime'] = self.ui.doubleSpinBoxEndTime.value()
        pdict['tstep'] = self.ui.doubleSpinBoxChunkLength.value()
        
        
        rejectDict = dict()
        flatDict = dict()
        if self.ui.checkBoxRejection.isChecked():
            if self.ui.checkBoxGradReject.isChecked():
                rejectDict['grad'] = self.ui.doubleSpinBoxGradReject.value()
            if self.ui.checkBoxMagReject.isChecked():
                rejectDict['mag'] = self.ui.doubleSpinBoxMagReject.value()
            if self.ui.checkBoxEEGReject.isChecked():
                rejectDict['eeg'] = self.ui.doubleSpinBoxEEGReject.value()
            if self.ui.checkBoxEOGReject.isChecked():
                rejectDict['eog'] = self.ui.doubleSpinBoxEOGReject.value()
            if self.ui.checkBoxFlatGrad.isChecked():
                flatDict['grad'] = self.ui.doubleSpinBoxFlatGrad.value()
            if self.ui.checkBoxFlatMag.isChecked():
                flatDict['mag'] = self.ui.doubleSpinBoxFlatMag.value()
            if self.ui.checkBoxFlatEeg.isChecked():
                flatDict['eeg'] = self.ui.doubleSpinBoxFlatEEG.value()
            if self.ui.checkBoxFlatECG.isChecked():
                flatDict['ecg'] = self.ui.doubleSpinBoxFlatECG.value()
            if self.ui.checkBoxFlatEOG.isChecked():
                flatDict['eog'] = self.ui.doubleSpinBoxFlatEOG.value()
         
        if len(rejectDict) > 0:
            pdict['reject'] = rejectDict
        else: pdict['reject'] = None
            
        if len(flatDict) > 0:
            pdict['flat'] = flatDict
        else: pdict['flat'] = None
        
        if self.ui.buttonGroupIncludeChannels.checkedButton() == \
        self.ui.radioButtonIncludeAll:
            pdict['picks'] = None
        else:
            # TODO: this needs a parser, see validatorParser module
            pdict['picks'] = self.ui.plainTextEditIncludeChannelList.\
                             toPlainText()
        
        # Basic sanity checking for input values
        if pdict['starttime'] >= pdict['endtime']:
            message = 'Check beginning and end of your time interval'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        if (self.ui.buttonGroupRawFile.checkedButton() == \
        self.ui.radioButtonSubjectList and \
        len(self.ui.listViewSubjects.selectedIndexes()) == 0) or \
        (self.ui.buttonGroupRawFile.checkedButton() == \
        self.ui.radioButtonElseWhere and \
        self.ui.lineEditRawFile.text()) == '' :
            message = 'Please select a raw file to compute covariance from.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        self.parent.caller.create_covariance_from_raw(pdict)
        
        
    def on_pushButtonBrowse_clicked(self, checked=None):
        """
        Open file browser for raw data file.
        """
        if checked is None: return
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select raw ' + \
                      'to use', '/home/')
        self.ui.lineEditRawFile.setText(fname)
        
        
    def on_pushButtonShowInfo_clicked(self, checked=None):
        """
        Show basic information about the raw selected raw file.
        """
        if checked is None: return
        
        if self.ui.buttonGroupRawFile.checkedButton() == \
        self.ui.radioButtonSubjectList:
            selIndexes = self.ui.listViewSubjects.selectedIndexes()
            subjectName = selIndexes[0].data()
            subjectPath = os.path.join(self.parent.experiment.workspace,
                                       self.parent.experiment.experiment_name,
                                       subjectName, subjectName + '.fif')
        else:
            subjectPath = self.ui.lineEditRawFile.text()
        
        try:
            raw = fileManager.open_raw(subjectPath, False)
        except Exception:
            message = 'Could not open file for showing info.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        info = Ui_infoDialog()
        self.infoDialog = InfoDialog(raw, info, True)
        self.infoDialog.show()