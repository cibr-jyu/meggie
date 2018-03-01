"""
Author: Jaakko Leppakangas
"""

from PyQt4 import QtCore, QtGui

import os
import numpy as np
import mne

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general.fileManager import _read_epoch_stcs
from meggie.ui.utils.messaging import exc_messagebox
from stcFreqDialogUi import Ui_stcFreqDialog


class StcFreqDialog(QtGui.QDialog):
    """ Dialog for plotting frequencies over source estimates.
    """
    caller = Caller.Instance()
    fig = None

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_stcFreqDialog()
        self.ui.setupUi(self)

        stcs = _read_epoch_stcs(self.caller.experiment.active_subject)
        self.ui.listWidgetStcs.addItems(stcs)

    def accept(self):
        """ Computes TFR over all source amplitudes.
        """
        QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
        stc_dir = self.caller.experiment.active_subject.stc_directory
        stc_name = str(self.ui.listWidgetStcs.currentItem().text())
        full_path = os.path.join(stc_dir, stc_name)
        fmin = self.ui.doubleSpinBoxFmin.value()
        fmax = self.ui.doubleSpinBoxFmax.value()
        interval = self.ui.doubleSpinBoxInterval.value()
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        hemi = str(self.ui.comboBoxHemisphere.currentText())
        if hemi == 'left':
            hemi = '-lh.stc'
        elif hemi == 'right':
            hemi = '-rh.stc'
        freqs = np.arange(fmin, fmax, interval)
        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = self.ui.doubleSpinBoxCycleFactor.value() * freqs
        data = list()
        stc = None
        for f in os.listdir(full_path):
            if f.endswith(hemi):
                stc = mne.read_source_estimate(os.path.join(full_path, f))
                data.append(stc.data)
        try:
            self.caller.plot_stc_freq(stc, data, freqs, tmin, tmax, ncycles)
        except Exception as e:
            exc_messagebox(self, e)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
