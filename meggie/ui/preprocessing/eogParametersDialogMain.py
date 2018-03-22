# coding: utf-8

"""
Created on Apr 12, 2013

@author: Jaakko Leppakangas
Contains the EogParametersDialog used for collecting parameter values for
calculating EOG projections.
"""

import os
import ast
import gc
import traceback

from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import pyqtSignal

from meggie.ui.preprocessing.eogParametersDialogUi import Ui_Dialog
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

from meggie.code_meggie.general import fileManager

from meggie.code_meggie.preprocessing.projections import call_eog_ssp
from meggie.code_meggie.preprocessing.projections import plot_eog_events


class EogParametersDialog(QtGui.QDialog):
    """
    Class containing the logic for eogParametersDialog. Used for collecting
    parameter values for calculating EOG projections.
    """

    def __init__(self, parent):
        """
        Constructor. Initializes the dialog.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.batching_widget = BatchingWidget(
            self.parent.experiment, 
            self, self.ui.scrollAreaWidgetContents)

    def on_pushButtonPlotEvents_clicked(self, checked=None):
        if checked is None:
            return

        parameter_values = self.collect_parameter_values()
        plot_eog_events(self.parent.experiment, parameter_values)    

    def accept(self):
        """
        """
        parameter_values = self.collect_parameter_values()
        active_subject_name = self.parent.experiment.active_subject.subject_name
        self.batching_widget.data[active_subject_name] = parameter_values

        try:
            self.calculate_eog(self.parent.experiment.active_subject)
        except Exception as e:
            self.batching_widget.failed_subjects.append((
                self.parent.experiment.active_subject, str(e)))        
        
        self.batching_widget.cleanup()
        self.parent.initialize_ui()
        self.close()
    
    def acceptBatch(self):
        
        recently_active_subject = self.parent.experiment.active_subject.subject_name
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
                self.calculate_eog(self.parent.experiment.active_subject)
            except Exception as e:
                self.batching_widget.failed_subjects.append((
                    self.parent.experiment.active_subject, str(e)))
        
        # 2. Calculation is done for the rest of the subjects.
        for name, subject in self.parent.experiment.subjects.items():
            if name in subject_names:
                if name == recently_active_subject:
                    continue
                try:
                    self.parent.experiment.activate_subject(name)
                    self.calculate_eog(subject)
                except Exception as e:
                    self.batching_widget.failed_subjects.append((
                        subject, str(e)))
                
        self.parent.experiment.activate_subject(recently_active_subject)
        self.batching_widget.cleanup()
        self.parent.initialize_ui()
        self.close()
        
    def collect_parameter_values(self):
        """Collects parameter values from dialog.
        """
        
        dictionary = dict()

        dictionary['tmin'] = self.ui.doubleSpinBoxTmin.value()
        dictionary['tmax'] = self.ui.doubleSpinBoxTmax.value()
        dictionary['eog-l-freq'] = self.ui.spinBoxLowPass.value()
        dictionary['eog-h-freq'] = self.ui.spinBoxHighPass.value()
        dictionary['n-grad'] = self.ui.spinBoxGrad.value()
        dictionary['n-mag'] = self.ui.spinBoxMag.value()
        dictionary['n-eeg'] = self.ui.spinBoxEeg.value()
        dictionary['l-freq'] = self.ui.spinBoxLow.value()
        dictionary['h-freq'] = self.ui.spinBoxHigh.value()
        dictionary['rej-grad'] = self.ui.doubleSpinBoxGradReject.value()
        dictionary['rej-mag'] = self.ui.doubleSpinBoxMagReject.value()
        dictionary['rej-eeg'] = self.ui.doubleSpinBoxEEGReject.value()
        dictionary['rej-eog'] = self.ui.doubleSpinBoxEOGReject.value()
        dictionary['tstart'] = self.ui.spinBoxStart.value()
        dictionary['filtersize'] = self.ui.spinBoxTaps.value()

        excl_ssp = self.ui.checkBoxSSPProj.checkState() == QtCore.Qt.Checked
        dictionary['no-proj'] = excl_ssp

        comp_ssp = self.ui.checkBoxSSPCompute.checkState()==QtCore.Qt.Checked
        dictionary['average'] = comp_ssp

        return dictionary

    def selection_changed(self, subject_name, params_dict):
        """Unpickles parameter file from subject path and updates the values
        on dialog.
        """

        subject = self.parent.experiment.subjects[subject_name]
        if len(params_dict) > 0:
            dic = params_dict  
        else:
            dic = self.get_default_values()
        self.ui.doubleSpinBoxTmin.setProperty("value", dic.get('tmin'))
        self.ui.doubleSpinBoxTmax.setProperty("value", dic.get('tmax'))
        self.ui.spinBoxLowPass.setProperty("value", dic.get('eog-l-freq'))  # noqa
        self.ui.spinBoxHighPass.setProperty("value", dic.get('eog-h-freq'))  # noqa
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
            'tmax': 0.200, 
            'eog-l-freq': 1,
            'eog-h-freq': 10,
            'n-grad': 2,
            'n-mag': 2,
            'n-eeg': 2,
            'l-freq': 1,
            'h-freq': 35,
            'rej-grad': 3000.00,
            'rej-mag': 4000.00,
            'reg-eeg': 100.00,
            'rej-eog': 1000000000.00,
            'tstart': 0,
            'filtersize': 2048,
            'no-proj': True,
            'average': False        
        }


    def calculate_eog(self, subject):
        """
        """
        update_ui = self.parent.update_ui
        call_eog_ssp(self.batching_widget.data[subject.subject_name], 
                     subject, update_ui)
        
