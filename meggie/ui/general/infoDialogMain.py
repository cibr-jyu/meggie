# coding: utf-8

"""
"""

import sys

from PyQt5 import QtWidgets

from meggie.ui.general.infoDialogUi import Ui_infoDialog
from meggie.code_meggie.general.measurementInfo import MeasurementInfo


class InfoDialog(QtWidgets.QDialog):
    """
    Dialog to get and show the info from the raw file. Can be used to direct
    the extracted information from the file to the dialog itself or some
    other ui with similar element names. Currently used for setting the
    subject info fields below the subject list in the mainWindow. 
    """
    def __init__(self, raw, targetUi, create_window):
        """
        Constructor    
        Keyword arguments:
        raw           -- Raw object.
        targetUi      -- Ui object that receives the info data.
        create_window -- Boolean to determine if a new dialog window 
                         is created.
        """
        QtWidgets.QDialog.__init__(self)
        self.raw = raw
        self.ui = targetUi
        if create_window:
            self.ui.setupUi(self)
            self.ui.tab_list = []
        
        self._setLabelTestValues()
    
    def on_ButtonClose_clicked(self):
        """
        Closes the dialog
        """
        self.close()
        
    def _setLabelTestValues(self):
        """
        Sets the data info to the labels.
        """
        self.mi = MeasurementInfo(self.raw)
        
        self.ui.labelDateValue.setText(self.mi.date)
        self.ui.labelLengthValue.setText('%0.2f' % self.raw.times[-1] + 's')
        self.ui.labelEEGValue.setText(str(self.mi.EEG_channels))
        self.ui.labelGradMEGValue.setText(str(self.mi.grad_channels))
        self.ui.labelHighValue.setText(str(self.mi.high_pass) + ' Hz')
        self.ui.labelLowValue.setText(str(self.mi.low_pass) + ' Hz')
        self.ui.labelMagMEGValue.setText(str(self.mi.mag_channels))
        self.ui.labelSamplesValue.setText(str(self.mi.sampling_freq) + ' Hz')
        self.ui.labelSubjectValue.setText(self.mi.subject_name)
