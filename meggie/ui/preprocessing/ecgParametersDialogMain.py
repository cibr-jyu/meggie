# coding: utf-8

"""
Created on Apr 16, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen
Contains the EcgParametersDialog-class used for collecting parameter values
for calculating ECG projections.
"""

import logging

from PyQt4 import QtCore
from PyQt4 import QtGui

from meggie.ui.preprocessing.ecgParametersDialogUi import Ui_Dialog

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.general.measurementInfo import MeasurementInfo

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

from meggie.ui.widgets.batchingWidgetMain import BatchingWidget

class EcgParametersDialog(QtGui.QDialog):
    """
    Class containing the logic for ecgParametersDialog. it collects parameter
    values for calculating ECG projections.
    """
    caller = Caller.Instance()

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.batching_widget = BatchingWidget(self, self.ui.scrollAreaWidgetContents_2)

        raw = self.caller.experiment.active_subject.get_working_file()
        MEG_channels = MeasurementInfo(raw).MEG_channel_names
        self.ui.comboBoxECGChannel.addItems(MEG_channels)


    def selection_changed(self, subject_name, params_dict):
        """
        Unpickles parameter file from subject path and updates the values
        on dialog.
        """

        self.ui.comboBoxECGChannel.clear()
        
        if len(params_dict) > 0:
            dic = params_dict  
        else:
            dic = self.get_default_values()
        
        #channel_list = self.batching_widget.data[subject_name + ' channels']
        subject = self.caller.experiment.subjects.get(subject_name)
        raw = subject.get_working_file(preload=False, temporary=True)
        channel_list = raw.ch_names
        self.ui.comboBoxECGChannel.addItems(channel_list)
        channel_name = dic.get('ch_name')
        
        if channel_name is None:
            channel_name = channel_list[0]
        
        if channel_name == '':
            pass
        else:
            ch_idx = self.ui.comboBoxECGChannel.findText(channel_name, 
                QtCore.Qt.MatchContains)
        
        self.ui.comboBoxECGChannel.setCurrentIndex(ch_idx)
        self.ui.doubleSpinBoxTmin.setProperty("value", dic.get('tmin'))
        self.ui.doubleSpinBoxTmax.setProperty("value", dic.get('tmax'))
        self.ui.spinBoxLowPass.setProperty("value", dic.get('ecg-l-freq'))  # noqa
        self.ui.spinBoxHighPass.setProperty("value", dic.get('ecg-h-freq'))  # noqa
        self.ui.spinBoxGrad.setProperty("value", dic.get('n-grad'))
        self.ui.spinBoxMag.setProperty("value", dic.get('n-mag'))
        self.ui.spinBoxEeg.setProperty("value", dic.get('n-eeg'))
        self.ui.spinBoxLow.setProperty("value", dic.get('l-freq'))
        self.ui.spinBoxHigh.setProperty("value", dic.get('h-freq'))
        self.ui.doubleSpinBoxGradReject.setProperty("value", dic.get('rej-grad'))  # noqa
        self.ui.doubleSpinBoxMagReject.setProperty("value", dic.get('rej-mag'))  # noqa
        self.ui.doubleSpinBoxEEGReject.setProperty("value", dic.get('rej-eeg'))  # noqa
        self.ui.doubleSpinBoxEOGReject.setProperty("value", dic.get('rej-eog'))  # noqa
        self.ui.spinBoxStart.setProperty("value", dic.get('tstart'))
        self.ui.spinBoxTaps.setProperty("value", dic.get('filtersize'))
        self.ui.checkBoxSSPProj.setChecked(dic.get('no-proj'))
        self.ui.checkBoxSSPCompute.setChecked(dic.get('average'))

    def get_default_values(self):
        """Sets default values for dialog."""

        return {
            'tmin': -0.200,
            'tmax': 0.400,
            'eog-l-freq': 1,
            'eog-h-freq': 40,
            'n-grad': 2,
            'n-mag': 2,
            'n-eeg': 2,
            'l-freq': 1,
            'h-freq': 100,
            'rej-grad': 3000.00,
            'rej-mag': 4000.00,
            'reg-eeg': 100.00,
            'rej-eog': 250.00,
            'tstart': 5,
            'filtersize': 2048,
            'no-proj': True,
            'average': True        
        }

    def accept(self):
        """
        Collects the parameters for calculating PCA projections and pass them
        to the caller class.
        """
        parameter_values = self.collect_parameter_values()
        active_subject_name =  self.caller.experiment.active_subject.subject_name
        self.batching_widget.data[active_subject_name] = parameter_values
        try:
            self.calculate_ecg(self.caller.experiment.active_subject)    
        except Exception as e:
            self.batching_widget.failed_subjects.append((
                self.caller.experiment.active_subject, str(e)))
            
        self.batching_widget.cleanup()
        self.parent.initialize_ui()
        self.close()
        
    def on_pushButtonPlotEvents_clicked(self, checked=None):
        if checked is None:
            return

        parameter_values = self.collect_parameter_values()
        self.caller.plot_ecg_events(parameter_values)    
        
    def acceptBatch(self):
        
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
                self.calculate_ecg(self.caller.experiment.active_subject)    
            except Exception as e:
                self.batching_widget.failed_subjects.append((
                    self.caller.experiment.active_subject, str(e)))
        
        # 2. Calculation is done for the rest of the subjects
        for name, subject in self.caller.experiment.subjects.items():
            if name in subject_names:
                if name == recently_active_subject:
                    continue
                try:
                    self.caller.activate_subject(name)
                    self.calculate_ecg(subject)    
                except Exception as e:
                    self.batching_widget.failed_subjects.append((subject, str(e)))              

        self.caller.activate_subject(recently_active_subject)
        self.batching_widget.cleanup()        
        self.parent.initialize_ui()
        self.close()
        

    def collect_parameter_values(self):
        """Collects parameter values from dialog.
        """
        dictionary = dict()

        dictionary['tmin'] = self.ui.doubleSpinBoxTmin.value()
        dictionary['tmax'] = self.ui.doubleSpinBoxTmax.value()
        dictionary['ecg-l-freq'] = self.ui.spinBoxLowPass.value()
        dictionary['ecg-h-freq'] = self.ui.spinBoxHighPass.value()
        dictionary['n-grad'] = self.ui.spinBoxGrad.value()
        dictionary['n-mag'] = self.ui.spinBoxMag.value()
        dictionary['n-eeg'] = self.ui.spinBoxEeg.value()
        dictionary['l-freq'] = self.ui.spinBoxLow.value()
        dictionary['h-freq'] = self.ui.spinBoxHigh.value()
        dictionary['rej-grad'] = self.ui.doubleSpinBoxGradReject.value()
        dictionary['rej-mag'] = self.ui.doubleSpinBoxMagReject.value()
        dictionary['rej-eeg'] = self.ui.doubleSpinBoxEEGReject.value()
        dictionary['rej-eog'] = self.ui.doubleSpinBoxEOGReject.value()
        dictionary['qrs'] = self.ui.doubleSpinBoxQrs.value()
        dictionary['tstart'] = self.ui.spinBoxStart.value()
        dictionary['filtersize'] = self.ui.spinBoxTaps.value()
        dictionary['no-proj'] = self.ui.checkBoxSSPProj.isChecked()
        dictionary['average'] = self.ui.checkBoxSSPCompute.isChecked()
        dictionary['ch_name'] = self.ui.comboBoxECGChannel.currentText()

        return dictionary

    def calculate_ecg(self, subject):
        """Calls caller class for calculating the projections for the given
        subject and passes errors to accept method.
        
        Keyword arguments:
        subject               -- Subject object
        """
        self.caller.call_ecg_ssp(
            self.batching_widget.data[subject.subject_name], subject)
