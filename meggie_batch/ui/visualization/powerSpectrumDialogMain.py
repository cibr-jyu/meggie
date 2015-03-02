'''
Created on 26.2.2015

@author: Jaakko Leppakangas
'''
from PyQt4 import QtGui, QtCore
#from PyQt4.Qt import QSettings

import numpy as np
from mne import find_events

from code_meggie.general.caller import Caller
from powerSpectrumDialogUi import Ui_PowerSpectrumDialog
from ui.widgets.powerSpectrumWidgetMain import PowerSpectrumWidget
from ui.general.messageBoxes import shortMessageBox
from code_meggie.general import fileManager
from PyQt4.Qt import pyqtSlot
#from timeSeriesDialog import TimeSeriesDialog

class PowerSpectrumDialog(QtGui.QDialog):
    fileChanged = QtCore.pyqtSignal()
    caller = Caller.Instance()
    conditions = []
    tmax = 1000
    #settings = QSettings("CIBR", "Eggie")
    
    def __init__(self, parent): #, conditions, fmin, fmax, nfft, logarithm, lout, 
        #tmax):
        """
        Init method for the dialog.
        Constructs a set of time series from the given parameters.
        Parameters:
        parent     - The parent window for this dialog.
        conditions - A list of PowerSpectrumWidgets. The data from these 
                     widgets are copied to this dialog.
        fmin       - Starting frequency of interest.
        fmax       - Ending frequency of interest.
        nfft       - The length of the tapers ie. the windows. 
                     The smaller it is the smoother are the PSDs.
        logarithm  - A boolean that determines if a logarithmic scale is used.
        lout       - A layout file name.
        """
        QtGui.QDialog.__init__(self)
        
        self.conditions = []
        self.ui = Ui_PowerSpectrumDialog()
        self.ui.setupUi(self)
        self.installEventFilters()
        self.parent = parent
        raw = self.caller.experiment.active_subject.working_file
        tmax = np.floor(raw.index_as_time(raw.n_times))
        self.tmax = tmax
        widget = PowerSpectrumWidget(tmax, self)
        widget.setStartTime(5)
        widget.setEndTime(tmax)
        self.conditions.append(widget)
        widget.index = 0
        widget.removeWidget.connect(self.on_RemoveWidget_clicked)
        widget.channelCopy.connect(self.copyChannels)
        self.ui.verticalLayoutConditions.addWidget(widget)
        
        try:
            triggers = find_events(raw, stim_channel='STI 014')
            for trigger in set(triggers[:,2]):
                self.ui.comboBoxStart.addItem(str(trigger))
                self.ui.comboBoxEnd.addItem(str(trigger))
        except Exception as e:
            print 'Could not find triggers from STI 014.'
            print str(e)

        self.ui.buttonBox.addButton("Start", QtGui.QDialogButtonBox.AcceptRole)
        self.ui.buttonBox.addButton(QtGui.QDialogButtonBox.Close)
        
        #Populate layouts combobox.
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)   
        
    
        
    @QtCore.pyqtSlot(int)
    def on_RemoveWidget_clicked(self, index):
        """
        Called when a condition widget sends a remove signal.
        Removes a condition from the list.
        """
        widget = self.conditions.pop(index)
        self.ui.verticalLayoutConditions.removeWidget(widget)
        widget.deleteLater()
        widget = None
        # Restore order of indices:
        for i in xrange(len(self.conditions)):
            self.conditions[i].index = i
            
    @QtCore.pyqtSlot(int)
    def copyChannels(self, index):
        """
        """
        channels = self.conditions[index].getChannels()
        for widget in self.conditions:
            widget.on_ChannelsChanged(channels)
            
            
    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """
        Called when browse layout button is clicked.
        Opens a file dialog for selecting a file.
        """
        if checked is None: return
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                            '/home/', 
                            "Layout-files (*.lout *.lay);;All files (*.*)"))
        self.ui.labelLayout.setText(fname)
        #self.settings.setValue("Layout", fname)
        
        
    def on_pushButtonAddTimeSeries_clicked(self, checked=None):
        """
        Called when the add condition button is clicked.
        Adds a new condition to the list.
        """
        if checked is None: return
        index = len(self.conditions)
        channels = self.conditions[0].getChannels()
        widget = PowerSpectrumWidget(self.tmax, self)
        widget.index = index
        widget.on_ChannelsChanged(channels)
        self.conditions.append(widget)
        self.ui.verticalLayoutConditions.addWidget(widget)
        widget.removeWidget.connect(self.on_RemoveWidget_clicked)
        widget.channelCopy.connect(self.copyChannels)
    
    
    def accept(self, *args, **kwargs):
        """
        
        """

        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        
        colors = []
        times = [] # Array for start and end times.
        channelColors = dict()
        i = 0
        for condition in self.conditions:
            start = condition.getStartTime()
            end = condition.getEndTime()
            if end < start:
                messageBox = QtGui.QMessageBox()
                messageBox.setText("End time must be higher than the " + \
                                   "start time.")
                QtGui.QApplication.restoreOverrideCursor()
                messageBox.exec_()
                return 
            times.append((start, end))
            
            colors.append(condition.getColor())
            channels = condition.getChannels()
            channelColors[i] = (condition.getChannelColor(), channels)
            i += 1
        if len(times) == 0:
            messageBox = QtGui.QMessageBox()
            messageBox.setText("Could not find data. Check parameters!")
            QtGui.QApplication.restoreOverrideCursor()
            messageBox.exec_()
            return 
        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()
        if fmin >= fmax:
            messageBox = QtGui.QMessageBox()
            messageBox.setText("End frequency must be higher than the " + \
                               "starting frequency.")
            QtGui.QApplication.restoreOverrideCursor()
            messageBox.exec_()
            return
        params = dict()
        params['times'] = times
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['log']  = self.ui.checkBoxLogarithm.isChecked()
        params['ch'] = str(self.ui.comboBoxChannels.currentText()).lower()
        if self.ui.radioButtonSelectLayout.isChecked():
            params['lout'] = str(self.ui.comboBoxLayout.currentText())
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            params['lout'] = str(self.ui.labelLayout.text())
            if params['lout'] == 'No layout selected':
                QtGui.QApplication.restoreOverrideCursor()
                messageBox = QtGui.QMessageBox()
                messageBox.setText("No layout selected!")
                messageBox.exec_()
                return
        try:
            self.caller.plot_power_spectrum(params, colors, channelColors)
        except Exception as e:
            messageBox = QtGui.QMessageBox()
            messageBox.setText(str(e))
            QtGui.QApplication.restoreOverrideCursor()
            messageBox.exec_()
            return

        QtGui.QApplication.restoreOverrideCursor()
        
    
    @QtCore.pyqtSlot(int)   
    def on_comboBoxStart_currentIndexChanged(self, index):
        """
        Method for setting time on the start time spinbox after trigger 
        selection has changed.
        Parameters:
        index - Index of the selection in combobox.
        """
        if not self.ui.checkBoxTriggers.isChecked(): return
        raw = self.caller.experiment.active_subject.working_file
        triggers = find_events(raw, stim_channel='STI 014')
        triggerStart = int(self.ui.comboBoxStart.currentText())
        tmin = np.where(triggers[:,2]==triggerStart)[0][0]
        tmin = raw.index_as_time(triggers[tmin][0])
        tmin = int(tmin[0])
        self.conditions[0].setStartTime(tmin)
        
    @QtCore.pyqtSlot(int)   
    def on_comboBoxEnd_currentIndexChanged(self, index):
        """
        Method for setting time on the end time spinbox after trigger selection
        has changed.
        Parameters:
        index - Index of the selection in combobox.
        """
        if not self.ui.checkBoxTriggers.isChecked(): return
        raw = self.caller.experiment.active_subject.working_file
        triggers = find_events(raw, stim_channel='STI 014')
        triggerEnd = int(self.ui.comboBoxEnd.currentText())
        tmax = np.where(triggers[:,2]==triggerEnd)[0][0]
        tmax = raw.index_as_time(triggers[tmax][0])
        tmax = int(tmax[0])
        self.conditions[0].setEndTime(tmax)
        if not len(triggers) == len(set(triggers[:,2])):
            message = 'Data contains more than one of each trigger value. ' +\
                      'By selecting a trigger that appears in the data more '+\
                      'than once, there is ambiguity in the selection of the'+\
                      ' time window!'
            mBox = shortMessageBox(message)
            mBox.exec_()
            
        
    @QtCore.pyqtSlot(bool)
    def on_checkBoxTriggers_toggled(self, toggled):
        """
        A slot for setting the powerspectrumwidgets according to trigger 
        settings. Called when trigger check box is toggled.
        Parameters:
        toggled - A boolean that determines if check box is ticked.
        """
        if toggled:
            for condition in reversed(self.conditions):
                index = condition.index
                if index != 0:
                    self.on_RemoveWidget_clicked(index)
                else:
                    condition.disableSpinBoxes(toggled)
            self.ui.pushButtonAddTimeSeries.setEnabled(False)
            index = self.ui.comboBoxStart.currentIndex()
            self.on_comboBoxStart_currentIndexChanged(index)
            index = self.ui.comboBoxEnd.currentIndex()
            self.on_comboBoxEnd_currentIndexChanged(index)
        else:
            self.conditions[0].disableSpinBoxes(False)
            self.ui.pushButtonAddTimeSeries.setEnabled(True)
                        
    def on_pushButtonSeriesFromTriggers_clicked(self, checked=None):
        """
        Opens a TimeSeriesDialog.
        Called when construct time series from triggers -button is clicked.
        """
        pass
        """
        if checked is None or self.caller.raw is None: return
        dialog = TimeSeriesDialog()
        dialog.timeSeriesChanged.connect(self.on_TimeSeriesChanged)
        dialog.exec_()
        """
        
    @QtCore.pyqtSlot(list)    
    def on_TimeSeriesChanged(self, conditions):
        """
        Slot for adding a set of PowerSpectrumWidgets to this dialog.
        Called from TimeSeriesDialog.
        Parameters:
        conditions - A list of PowerSpectrumWidgets.
        """
        if conditions == []: return
        for widget in self.conditions:
            self.on_RemoveWidget_clicked(widget.index)
        i = 0
        tmax = np.floor(self.caller.raw.index_as_time(self.caller.raw.n_times))
        for condition in conditions:
            widget = PowerSpectrumWidget(tmax, self)
            widget.setStartTime(condition.getStartTime())
            widget.setEndTime(condition.getEndTime())
            widget.setColor(condition.getColor())
            widget.setChannelColor(condition.getChannelColor())
            widget.on_ChannelsChanged(condition.getChannels())
            self.conditions.append(widget)
            widget.index = i
            widget.removeWidget.connect(self.on_RemoveWidget_clicked)
            widget.channelCopy.connect(self.copyChannels)
            self.ui.verticalLayoutConditions.addWidget(widget)
            i+=1
        self.ui.scrollAreaConditions.updateGeometry()
        
    def updateUi(self):
        self.parent.updateUi()
        
    def keyPressEvent(self, qKeyEvent):
        """
        Overrided method to prevent enter or return from starting the plotting.
        Parameters:
        qKeyEvent - Qt key event.
        """
        key = qKeyEvent.key()
        if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            return
        return QtGui.QDialog.keyPressEvent(self, qKeyEvent)
    
    def installEventFilters(self):
        """
        Helper method for disabling wheel events on all widgets.
        """
        self.ui.spinBoxFmin.installEventFilter(self)
        self.ui.spinBoxFmax.installEventFilter(self)
        self.ui.spinBoxNfft.installEventFilter(self)
    
    def eventFilter(self, source, event):
        """
        Event filter for disabling wheel events on spin boxes and such.
        """
        if (event.type() == QtCore.QEvent.Wheel):
            return True
        return QtGui.QWidget.eventFilter(self, source, event)
        
