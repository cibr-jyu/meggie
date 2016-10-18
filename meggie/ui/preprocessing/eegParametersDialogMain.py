'''
Created on 6.10.2016

@author: jaolpeso
'''
from PyQt4 import QtCore,QtGui
from meggie.ui.preprocessing.eegParametersDialogUi import Ui_Dialog

import numpy as np

from meggie.code_meggie.general.caller import Caller
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget
from PyQt4.Qt import pyqtSlot

class EegParametersDialog(QtGui.QDialog):
    
    caller = Caller.Instance()
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.batching_widget = BatchingWidget(self, self.ui.scrollAreaWidgetContents)
        self.batching_widget.ui.checkBoxBatch.stateChanged.connect(self.disable_event_table())
        
        raw = self.caller.experiment.active_subject.get_working_file()
        self.ui.comboBoxChannelSelect.addItems(raw.ch_names)
        
        self.event_id = None
        self.ui.tableWidgetEvents.currentItemChanged.connect(
            self.on_currentChanged
        )
        self.ui.tableWidgetEvents.setSortingEnabled(False)
        self.ui.tableWidgetEvents.setSelectionBehavior(1)        
        self.ui.tableWidgetEvents.setColumnCount(4)
        self.set_event_table_headers()
        
    @pyqtSlot(int)
    def disable_event_table(self, value):
        self.ui.tableWidgetEvents.setEnabled(False)
        
    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Finds EOG-events from the raw data.
        Called when find eog events -button is clicked.
        """
        raw = self.caller.experiment.active_subject.get_working_file()
        if checked is None or not raw: return
        
        params = dict()
        self.event_id = int(self.ui.labelBlinkId.text())
        params['event_id'] = self.event_id
        params['ch_name'] = str(self.ui.comboBoxChannelSelect.currentText())
        params['l_freq'] = float(self.ui.doubleSpinBoxLowPass.value())
        params['h_freq'] = float(self.ui.doubleSpinBoxHighPass.value())
        params['filter_length'] = str(self.ui.spinBoxFilterLength.value())+'s'
        params['tstart'] = float(self.ui.doubleSpinBoxStart.value())
        
        try:
            eog_events = self.caller.find_eog_events(params)
            self.ui.tableWidgetEvents.clear()
            self.ui.tableWidgetEvents.setRowCount(0)
            for i in range(0, len(eog_events)):
                self.ui.tableWidgetEvents.insertRow(i)
                self.ui.tableWidgetEvents.setItem(
                    i,0,QtGui.QTableWidgetItem(
                        str(raw.index_as_time(eog_events[i][0])[0])
                    )
                )
                self.ui.tableWidgetEvents.setItem(i,1,QtGui.
                    QTableWidgetItem(str(int(eog_events[i][0])))
                )
                self.ui.tableWidgetEvents.setItem(
                    i,2,QtGui.QTableWidgetItem(str(eog_events[i][1]))
                )
                self.ui.tableWidgetEvents.setItem(
                    i,3,QtGui.QTableWidgetItem(str(eog_events[i][2]))
                )
        except Exception as e:
            exc_messagebox(self, e)

        self.set_event_table_headers()
        self.batching_widget.data['event_params'] = params
            
    def get_events(self):
        """
        A convenience function for fetching all the events from
        the tableWidgetEvents as a numpy array.
        returns:
        eog_events as numpy array
        """
        events = list()
        rowCount = self.ui.tableWidgetEvents.rowCount()
        
        for i in xrange(0, rowCount):
            #time = float(self.ui.tableWidgetEvents.item(i, 1).text())
            time = int(self.ui.tableWidgetEvents.item(i, 1).text())
            prev = int(self.ui.tableWidgetEvents.item(i, 2).text())
            curr = int(self.ui.tableWidgetEvents.item(i, 3).text())
            events.append([time, prev, curr])

        return np.array(events)

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
            self.ui.pushButtonRemove.setEnabled(False)
        else:
            self.ui.pushButtonRemove.setEnabled(True)

    def on_pushButtonPlotEpochs_clicked(self, checked=None):
        """
        Plots the averaged epochs.
        """
        if checked is None: return
        events = self.get_events()
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        self.caller.plot_average_epochs(events, tmin, tmax, self.event_id)
        
    def on_pushButtonShowEvents_clicked(self, checked=None):
        """
        Plots the events on mne_browse_raw.
        """
        if checked is None: return
        events = self.get_events()
        self.caller.plot_events(events)

    def set_event_table_headers(self):
        #TODO:
        self.ui.tableWidgetEvents.setHorizontalHeaderLabels([
            "Time (s)",
            "Sample",
            "Prev. id",
            "Current id"
        ])

    def update_events(self):
        #TODO:
        self.ui.tableWidgetEvents.clear()
        self.ui.tableWidgetEvents.setRowCount(0)
        self.set_event_table_headers()


    def selection_changed(self, subject_name, params_dict):
        """
        Unpickles parameter file from subject path and updates the values
        on dialog.
        """
        #TODO:

        #self.ui.comboBoxChannelSelect
        
        if len(params_dict) > 0:
            dic = params_dict  
        else:
            dic = self.get_default_values()
        
        #channel_list = self.batching_widget.data[subject_name + ' channels']
        subject = self.caller.experiment.subjects.get(subject_name)
        raw = subject.get_working_file(preload=False, temporary=True)
        channel_list = raw.ch_names
        self.ui.comboBoxChannelSelect.clear()
        self.ui.comboBoxChannelSelect.addItems(channel_list)
        channel_name = dic.get('ch_name')
        
        if channel_name is None:
            channel_name = channel_list[0]
        
        if channel_name == '':
            pass
        else:
            ch_idx = self.ui.comboBoxChannelSelect.findText(channel_name,
                            QtCore.Qt.MatchContains)
        
        self.ui.comboBoxChannelSelect.setCurrentIndex(ch_idx)
        self.ui.doubleSpinBoxTmin.setProperty("value", dic.get('tmin'))
        self.ui.doubleSpinBoxTmax.setProperty("value", dic.get('tmax'))
        #self.ui.spinBoxEventsID.setProperty("value", dic.get('event-id'))  # noqa
        self.ui.spinBoxVectors.setProperty("value", dic.get('n_eeg'))
        self.update_events()

    def get_default_values(self):
        """Sets default values for dialog."""
        #TODO:
        return {
            'tmin': -0.200,
            'tmax': 0.500,
            'event_id': 998,
            'n_eeg': 2,
            #'events': None,
        }
    
    def collect_parameter_values(self):
        """Collects parameter values from dialog.
        """
        dictionary = dict()
        dictionary['tmin'] = self.ui.doubleSpinBoxTmin.value()
        dictionary['tmax'] = self.ui.doubleSpinBoxTmax.value()
        dictionary['event_id'] = 998
        dictionary['events'] = self.get_events()
        dictionary['n_eeg'] = self.ui.spinBoxVectors.value()
        return dictionary

    def accept(self):
        """
        Collects the parameters for calculating PCA projections and pass them
        to the caller class.
        """
        #TODO:
        parameter_values = self.collect_parameter_values()
        active_subject_name =  self.caller.experiment.active_subject.subject_name
        self.batching_widget.data[active_subject_name] = parameter_values
        try:
            self.calculate_eeg(self.caller.experiment.active_subject)    
        except Exception as e:
            self.batching_widget.failed_subjects.append((
                self.caller.experiment.active_subject, str(e)))
            
        self.batching_widget.cleanup()
        self.parent.initialize_ui()
        self.close()
        
    def acceptBatch(self):
        #TODO:
        recently_active_subject = self.caller.experiment.active_subject.subject_name
        subject_names = []
        for i in range(self.batching_widget.ui.listWidgetSubjects.count()):
            item = self.batching_widget.ui.listWidgetSubjects.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                subject_names.append(item.text())
        # In case of batch process:
        # 1. Calculation is first done for the active subject to prevent an
        #    excessive reading of a raw file.
        if recently_active_subject in subject_names:
            try:
                #eog_events = self.caller.find_eog_events(
                #    self.batching_widget['event_params'])
                #self.batching_widget.data[recently_active_subject]['events'] = eog_events
                self.calculate_eeg(self.caller.experiment.active_subject)    
            except Exception as e:
                self.batching_widget.failed_subjects.append((
                    self.caller.experiment.active_subject, str(e)))
        
        # 2. Calculation is done for the rest of the subjects
        for name, subject in self.caller.experiment.subjects.items():
            if name in subject_names:
                if name == recently_active_subject:
                    continue
                self.caller.activate_subject(name)
                try:
                    eog_events = self.caller.find_eog_events(
                        self.batching_widget.data['event_params'])
                    self.batching_widget.data[recently_active_subject]['events'] = eog_events
                    self.calculate_eeg(subject)    
                except Exception as e:
                    self.batching_widget.failed_subjects.append((subject, str(e)))              

        self.caller.activate_subject(recently_active_subject)
        self.batching_widget.cleanup()        
        self.parent.initialize_ui()
        self.close()


    def calculate_eeg(self, subject):
        self.caller.call_eeg_ssp(
            self.batching_widget.data[subject.subject_name], subject)


    
    
        
        