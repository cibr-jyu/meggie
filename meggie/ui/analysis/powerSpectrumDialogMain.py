'''
Created on 26.2.2015

@author: Jaakko Leppakangas
'''

from collections import OrderedDict

from PyQt4 import QtGui, QtCore

import numpy as np

from mne import Epochs

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import fileManager

from meggie.ui.analysis.powerSpectrumDialogUi import Ui_PowerSpectrumDialog
from meggie.ui.analysis.powerSpectrumEventsDialogMain import PowerSpectrumEvents

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
        tmax = np.floor(raw.times[raw.n_times - 1]) - 0.1
        self.ui.doubleSpinBoxTmin.setValue(0)
        self.ui.doubleSpinBoxTmax.setValue(tmax)
        self.ui.doubleSpinBoxTmin.setMaximum(tmax)
        self.ui.doubleSpinBoxTmax.setMaximum(tmax)

    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None:
            return
        group = int(self.ui.comboBoxAvgGroup.currentText())
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        if tmin >= tmax:
            messagebox(self.parent, "End time must be higher than the starting time")
            return
        
        self.add_intervals([(group, tmin, tmax)])

                
    def add_intervals(self, intervals):
        for interval in intervals:
            self.intervals.append(interval)
            item = QtGui.QListWidgetItem(
                '%s: %s - %s s' % (
                interval[0],
                round(interval[1], 4),
                round(interval[2], 4)
            ))
            self.ui.listWidgetIntervals.addItem(item)

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return
        self.intervals = []
        self.ui.listWidgetIntervals.clear()
        
    def on_pushButtonClearRow_clicked(self, checked=None):
        if checked is None:
            return
        current_row = self.ui.listWidgetIntervals.currentRow()
        self.ui.listWidgetIntervals.takeItem(current_row)
        self.intervals.pop(current_row)
        
    def on_pushButtonAddEvents_clicked(self, checked=None):
        if checked is None:
            return
        self.event_dialog = PowerSpectrumEvents(self)
        self.event_dialog.show()

    def accept(self, *args, **kwargs):
        """Starts the computation."""

        times = self.intervals
        
        if not times:
            messagebox(self.parent, "Must have at least one interval")
            return

        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()
        if fmin >= fmax:
            messagebox(self.parent, "End frequency must be higher than the starting frequency")
            return
        
        subject = self.caller.experiment.active_subject
        sfreq = subject.get_working_file().info['sfreq']
    
        valid = True
        for interval in times:
            if (interval[2] - interval[1]) * sfreq < float(self.ui.spinBoxNfft.value()):
                valid = False
        if not valid:
            messagebox(self.parent, "Sampling rate times shortest interval should be more than window size")
            return
        
        raw = self.caller.experiment.active_subject.get_working_file()
        
        epochs = OrderedDict()
        for interval in times:
            events = np.array([[raw.first_samp + interval[1]*sfreq, 0, 1]], dtype=np.int)
            tmin = 0
            tmax = interval[2] - interval[1]
            epoch = Epochs(raw, events=events, tmin=tmin, tmax=tmax)
            epoch.comment = str(interval)
            if interval[0] not in epochs:
                epochs[interval[0]] = []
            epochs[interval[0]].append(epoch)
        
        params = dict()
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['log'] = self.ui.checkBoxLogarithm.isChecked()
        params['overlap'] = self.ui.spinBoxOverlap.value()
        save_data = self.ui.checkBoxSaveData.isChecked()
        
        try:
            QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.caller.plot_power_spectrum(params, save_data, epochs)
        except Exception as e:
            exc_messagebox(self.parent, e)
        QtGui.QApplication.restoreOverrideCursor()
