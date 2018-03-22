# coding: utf-8

"""
Created on 24.5.2016

@author: jaolpeso
"""
from PyQt4 import QtGui

from meggie.ui.analysis.TFRfromRawDialogUi import Ui_DialogRawTFR
from meggie.code_meggie.general import fileManager

from meggie.code_meggie.analysis.spectral import TFR_raw

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

class TFRRawDialog(QtGui.QDialog):
    """
    """
    
    def __init__(self, parent):
        """
        Constructor. Sets up the dialog
        
        Keyword arguments:
        
        parent    --    Parent of the dialog
        epochs    --    a collection of epochs
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogRawTFR()
        self.ui.setupUi(self)
        
        raw = self.parent.experiment.active_subject.get_working_file()
        channels = raw.info['ch_names']
        self.ui.comboBoxChannel.addItems(channels)
        self.ui.doubleSpinBoxBaselineStart.setMinimum(raw.times[0])
        self.ui.doubleSpinBoxBaselineStart.setMaximum(raw.times[-1])
        self.ui.doubleSpinBoxBaselineStart.setValue(raw.times[0])
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(raw.times[0])
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(raw.times[-1])
        self.ui.doubleSpinBoxBaselineEnd.setValue(raw.times[-1])

        
        
    def accept(self):
        """
        """
        wsize = self.ui.spinBoxWsize.value()
        if self.ui.checkBoxTstep.isChecked():
            tstep = wsize / 2
        else:
            tstep = self.ui.spinBoxTstep.value()
            
        channel_idx = self.ui.comboBoxChannel.currentIndex()
        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()
        save_data = self.ui.checkBoxSaveData.isChecked()    
        
        if self.ui.groupBoxBaseline.isChecked():
            mode = str(self.ui.comboBoxMode.currentText())
            blstart = self.ui.doubleSpinBoxBaselineStart.value()
            blend = self.ui.doubleSpinBoxBaselineEnd.value()
        else:
            blstart, blend, mode = None, None, None

        
        try:
            experiment = self.parent.experiment
            TFR_raw(experiment, wsize=wsize, tstep=tstep, channel=channel_idx,
                fmin=fmin, fmax=fmax, blstart=blstart, blend=blend, mode=mode,
                save_data=save_data)
        except Exception as e:
            exc_messagebox(self, e)
            
