'''
Created on 7.1.2015

@author: Kari Aliranta
'''

from PyQt4 import QtGui

from covarianceRawDialogUi import Ui_covarianceRawDialog


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
        
           
    def accept(self):
        """
        Gets the arguments from the gui and passes them to caller for computing
        the noise covariance matrix. 
        """
        
        # TODO: basic input sanity checking here (start time later than end etc.
        
        pdict = dict()
        
        pdict['rawfilename'] = self.ui.lineEditRawFile.text()
        pdict['starttime'] = self.ui.doubleSpinBoxStartTime.value()
        pdict['endtime'] = self.ui.doubleSpinBoxEndTime.value()
        
        rejectDict = dict()
        flatDict = dict()
        if self.ui.checkBoxRejection.isChecked():
            if self.ui.checkBoxRejectGrad.isChecked():
                rejectDict['grad'] = self.ui.doubleSpinBoxGradReject.value()
            if self.ui.checkBoxRejectMag.isChecked():
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
            
        pdict
            
    def on_pushButtonBrowse_clicked(self, checked=None):
        """
        Open file browser for raw data file.
        """
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Select raw ' + \
                      'to use', '/home/')
        