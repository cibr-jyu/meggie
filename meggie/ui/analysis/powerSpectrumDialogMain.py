"""
"""

import logging

from collections import OrderedDict

from PyQt5 import QtWidgets

import numpy as np

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne

from meggie.ui.analysis.powerSpectrumDialogUi import Ui_PowerSpectrumDialog
from meggie.ui.analysis.powerSpectrumEventsDialogMain import PowerSpectrumEvents

from meggie.code_meggie.analysis.spectral import create_power_spectrum

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox


class PowerSpectrumDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment):
        """
        Init method for the dialog.
        Constructs a set of time series from the given parameters.
        Parameters:
        parent     - The parent window for this dialog.
        """
        QtWidgets.QDialog.__init__(self)
        self.intervals = []
        self.ui = Ui_PowerSpectrumDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = experiment

        raw = self.experiment.active_subject.get_working_file()

        tmax = np.floor(raw.times[raw.n_times - 1]) - 0.1
        self.ui.doubleSpinBoxTmin.setValue(0)
        self.ui.doubleSpinBoxTmax.setValue(tmax)
        self.ui.doubleSpinBoxTmin.setMaximum(tmax)
        self.ui.doubleSpinBoxTmax.setMaximum(tmax)

        # set nfft initially to ~2 seconds and overlap to ~1 seconds
        sfreq = raw.info['sfreq']
        window_in_seconds = 2
        nfft = int(np.power(2, np.ceil(np.log(sfreq * window_in_seconds)/np.log(2))))
        overlap = nfft / 2

        self.ui.spinBoxNfft.setValue(nfft)
        self.ui.spinBoxOverlap.setValue(overlap)

        if raw.info.get('highpass'):
            if self.ui.spinBoxFmin.value() < raw.info['highpass']:
                self.ui.spinBoxFmin.setValue(int(np.ceil(raw.info['highpass'])))

        if raw.info.get('lowpass'):
            if self.ui.spinBoxFmax.value() > raw.info['lowpass']:
                self.ui.spinBoxFmax.setValue(int(raw.info['lowpass']))

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
            item = QtWidgets.QListWidgetItem(
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

        name = self.ui.lineEditName.text()
        if not name:
            messagebox(self.parent, "Must have a name")
            return

        times = self.intervals
        
        if not times:
            messagebox(self.parent, "Must have at least one interval")
            return

        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()
        if fmin >= fmax:
            messagebox(self.parent, ("End frequency must be higher than the"
                                     "starting frequency"))
            return
        
        subject = self.experiment.active_subject
        sfreq = subject.get_working_file().info['sfreq']
    
        valid = True
        for interval in times:
            if (interval[2] - interval[1]) * sfreq < float(self.ui.spinBoxNfft.value()):
                valid = False
        if not valid:
            messagebox(self.parent, ("Sampling rate times shortest interval"
                                     "should be more than window size"))
            return
        
        raw = self.experiment.active_subject.get_working_file()
        
        epochs = OrderedDict()
        for interval in times:
            events = np.array([[raw.first_samp + interval[1]*sfreq, 0, 1]], dtype=np.int)
            tmin, tmax = 0, interval[2] - interval[1]
            epoch = mne.Epochs(raw, events=events, tmin=tmin, tmax=tmax, baseline=None)
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

        try:
            experiment = self.experiment
            update_ui = self.parent.update_ui
            create_power_spectrum(experiment, name, params, epochs, 
                                  update_ui=update_ui)
            experiment.save_experiment_settings()
            self.parent.initialize_ui()
        except Exception as e:
            exc_messagebox(self.parent, e)

        self.close()
