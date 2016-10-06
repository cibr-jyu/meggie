'''
Created on 6.10.2016

@author: jaolpeso
'''
from PyQt4 import QtCore,QtGui
from meggie.ui.preprocessing.eegParametersDialogUi import Ui_Dialog

import mne

from meggie.code_meggie.general.caller import Caller

class EegParametersDialog(QtGui.QDialog):
    
    caller = Caller.Instance()
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        raw = self.caller.experiment.active_subject.get_working_file()
        self.ui.comboBoxChannelSelect.addItems(raw.info.get('ch_names'))

        self.ui.tableWidgetEvents.currentItemChanged.connect(self.\
                                            on_currentChanged)
        self.ui.tableWidgetEvents.setSortingEnabled(False)
        self.ui.tableWidgetEvents.setSelectionBehavior(1)        
        self.ui.tableWidgetEvents.setColumnCount(4)
        self.ui.tableWidgetEvents.setHorizontalHeaderLabels(["Time (s)",
                                                             "Sample",
                                                             "Prev. id",
                                                             "Current id"])

        
    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Finds EOG-events from the raw data.
        Called when find eog events -button is clicked.
        """
        raw = self.caller.experiment.active_subject.get_working_file()
        if checked is None or not raw: return
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        params = dict()
        event_id = int(self.ui.labelBlinkId.text())
        params['event_id'] = event_id
        params['ch_name'] = str(self.ui.comboBoxChannelSelect.currentText())
        params['l_freq'] = float(self.ui.doubleSpinBoxLowPass.value())
        params['h_freq'] = float(self.ui.doubleSpinBoxHighPass.value())
        params['filter_length'] = str(self.ui.spinBoxFilterLength.value())+'s'
        params['tstart'] = float(self.ui.doubleSpinBoxStart.value())
        
        try:
            #sfreq = self.caller.raw.info['sfreq']
            eog_events = self.findEogEvents(params) #self.caller.findEogEvents(params)
            #eog_events = self.caller.raw.index_as_time(eog_events)
            self.ui.tableWidgetEvents.clear()
            self.ui.tableWidgetEvents.setRowCount(0)
            for i in range(0, len(eog_events)):
                self.ui.tableWidgetEvents.insertRow(i)
                self.ui.tableWidgetEvents.setItem(i,0,QtGui.\
                            QTableWidgetItem(str(raw.index_as_time(eog_events[i][0])[0])))
                self.ui.tableWidgetEvents.setItem(i,1,QtGui.\
                            QTableWidgetItem(str(int(eog_events[i][0]))))
                self.ui.tableWidgetEvents.setItem(i,2,QtGui.\
                            QTableWidgetItem(str(eog_events[i][1])))
                self.ui.tableWidgetEvents.setItem(i,3,QtGui.\
                            QTableWidgetItem(str(eog_events[i][2])))
        except Exception as e:
            print str(e)
        finally:
            self.ui.tableWidgetEvents.setHorizontalHeaderLabels(["Time (s)",
                                                                 "Sample",
                                                                 "Prev. id",
                                                                 "Current id"])
            QtGui.QApplication.restoreOverrideCursor()
            
    def findEogEvents(self, params):
        #TODO: move to caller
        try:
            print type(params['event_id'])
            raw = self.caller.experiment.active_subject.get_working_file()
            eog_events = mne.preprocessing.find_eog_events(raw, event_id=params['event_id'],
                        l_freq=params['l_freq'], h_freq=params['h_freq'],
                        filter_length=params['filter_length'],
                        ch_name=params['ch_name'], verbose=True,
                        tstart=params['tstart'])
        except Exception as e:
            print "Exception while finding events.\n"
            print str(e)
            return []
        return eog_events

    def on_pushButtonRemove_clicked(self, checked=None):
        if checked is None: return
        index = self.ui.tableWidgetEvents.currentRow()
        self.ui.tableWidgetEvents.removeRow(index)

    @QtCore.pyqtSlot()
    def on_currentChanged(self):
        """
        Called when tableWidgetEvent row selection is changed.
        """
        index = self.ui.tableWidgetEvents.currentIndex().row()
        if index < 0:
            self.ui.pushButtonDelete.setEnabled(False)
        else:
            self.ui.pushButtonDelete.setEnabled(True)

        