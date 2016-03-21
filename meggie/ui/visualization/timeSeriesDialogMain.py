'''
Created on 8.9.2015

@author: Jaakko Leppakangas
'''
from PyQt4 import QtGui, QtCore

import mne
import numpy as np

from meggie.ui.visualization.timeSeriesDialogUi import Ui_TimeSeriesDialog
from meggie.ui.widgets.powerSpectrumWidgetMain import PowerSpectrumWidget

from meggie.code_meggie.general.caller import Caller


class TimeSeriesDialog(QtGui.QDialog):
    """
    Dialog for dynamically creating a set of time series. Time series is
    created between the found events so that it is possible to divide segments
    by inserting a trigger to the start of the segment.
    """
    caller = Caller.Instance()
    widgets = []
    timeSeriesChanged = QtCore.pyqtSignal(list)

    def __init__(self):
        """Init method for time series dialog."""
        QtGui.QDialog.__init__(self)

        self.ui = Ui_TimeSeriesDialog()
        self.ui.setupUi(self)

        self.widgets = []
        subject = self.caller.experiment.active_subject
        self.raw = subject.get_working_file()
        self.ui.comboBoxChannels.addItems(self.raw.ch_names)
        index = self.ui.comboBoxChannels.findText(subject.find_stim_channel())
        self.ui.comboBoxChannels.setCurrentIndex(index)

    def on_pushButtonFind_clicked(self, checked=None):
        """Finds events based on triggers on the selected channel."""
        if checked is None:
            return

        for widget in reversed(self.widgets):
            index = widget.index
            self.on_RemoveWidget_clicked(index)
        tstart = self.ui.spinBoxTstart.value()
        tend = self.ui.spinBoxTend.value()
        channel = str(self.ui.comboBoxChannels.currentText())
        mask = self.ui.spinBoxMask.value()
        try:
            events = mne.find_events(self.raw, stim_channel=channel, mask=mask,
                                     verbose=True)
        except:
            return
        tceil = np.floor(self.raw.index_as_time(self.raw.n_times))  # ms to s
        for i in xrange(len(events) - 1):
            widget = PowerSpectrumWidget(tceil, self)
            widget.index = i
            widget.ui.pushButtonRemove.setVisible(True)
            tmin = self.raw.index_as_time(events[i][0] -
                                          self.raw.first_samp) + tstart
            tmax = self.raw.index_as_time(events[i+1][0] -
                                          self.raw.first_samp) - tend
            widget.setStartTime(tmin[0])
            widget.setEndTime(tmax[0])
            self.widgets.append(widget)
            widget.removeWidget.connect(self.on_RemoveWidget_clicked)
            widget.channelCopy.connect(self.copyChannels)
            self.ui.verticalLayoutConditions.addWidget(widget)

    @QtCore.pyqtSlot(int)
    def on_RemoveWidget_clicked(self, index):
        """
        Called when a power spectrum widget sends a remove signal.
        Removes a condition from the list.
        Parameters:
        index - Index given for the PowerSpectrumWidget.
        """
        widget = self.widgets.pop(index)
        self.ui.verticalLayoutConditions.removeWidget(widget)
        widget.deleteLater()
        widget = None
        # Restore order of indices:
        for i in xrange(len(self.widgets)):
            self.widgets[i].index = i
            self.widgets[i].ui.pushButtonRemove.setVisible(True)

    @QtCore.pyqtSlot(int)
    def copyChannels(self, index):
        """Slot for copying channels of interest to all widgets."""
        channels = self.widgets[index].getChannels()
        for widget in self.conditions:
            widget.on_ChannelsChanged(channels)

    def accept(self, *args, **kwargs):
        self.timeSeriesChanged.emit(self.widgets)
        return QtGui.QDialog.accept(self, *args, **kwargs)
