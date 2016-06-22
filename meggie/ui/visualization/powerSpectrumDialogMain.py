'''
Created on 26.2.2015

@author: Jaakko Leppakangas
'''
from PyQt4 import QtGui, QtCore

import numpy as np
from mne import find_events

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import fileManager

from meggie.ui.visualization.powerSpectrumDialogUi import Ui_PowerSpectrumDialog

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox


class PowerSpectrumDialog(QtGui.QDialog):
    caller = Caller.Instance()

    def __init__(self, parent):
        """
        Init method for the dialog.
        Constructs a set of time series from the given parameters.
        Parameters:
        parent     - The parent window for this dialog.
        """
        QtGui.QDialog.__init__(self)
        self.intervals = []
        self.ui = Ui_PowerSpectrumDialog()
        self.ui.setupUi(self)
        self.parent = parent
        raw = self.caller.experiment.active_subject.get_working_file()
        tmax = np.floor(raw.index_as_time(raw.n_times))
        self.ui.doubleSpinBoxTmin.setValue(0)
        self.ui.doubleSpinBoxTmax.setValue(tmax)
        self.ui.doubleSpinBoxTmin.setMaximum(tmax)
        self.ui.doubleSpinBoxTmax.setMaximum(tmax)

    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None:
            return
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        if tmin >= tmax:
            messagebox(self.parent, "End time must be higher than the starting time")
            return
        interval = (tmin, tmax)
        self.intervals.append(interval)
        item = QtGui.QListWidgetItem(
            '%s - %s s' % (
            interval[0],
            interval[1]
        ))
        self.ui.listWidgetIntervals.addItem(item)

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return
        self.intervals = []
        self.ui.listWidgetIntervals.clear()

    def accept(self, *args, **kwargs):
        """Starts the computation."""

        times = self.intervals
        
        if not times:
            messagebox(self.parent, "Must have at least one interval")

        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()
        if fmin >= fmax:
            messagebox(self.parent, "End frequency must be higher than the starting frequency")
            return
        params = dict()
        params['times'] = times
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['log'] = self.ui.checkBoxLogarithm.isChecked()
        params['ch'] = str(self.ui.comboBoxChannels.currentText()).lower()
        params['overlap'] = self.ui.spinBoxOverlap.value()
        params['average'] = self.ui.checkBoxAverage.isChecked()
        save_data = self.ui.checkBoxSaveData.isChecked()

        try:
            QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.caller.plot_power_spectrum(params, save_data)
        except Exception as e:
            exc_messagebox(self.parent, e)
        QtGui.QApplication.restoreOverrideCursor()
