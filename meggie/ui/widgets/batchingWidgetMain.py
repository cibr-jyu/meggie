"""
"""

import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.ui.widgets.batchingWidgetUi import Ui_BatchingWidget

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox

from copy import deepcopy

class BatchingWidget(QtWidgets.QWidget):
    """
    """
    
    def __init__(self, experiment_getter, parent, geometry, 
                 container=None, 
                 pushButtonCompute=None,
                 pushButtonComputeBatch=None, 
                 selection_changed=None,
                 collect_parameter_values=None, 
                 hideHook=None):
        super(BatchingWidget, self).__init__(container)
        self.ui = Ui_BatchingWidget()
        self.ui.setupUi(self)
        self.parent = parent

        if not pushButtonCompute:
            pushButtonCompute = self.parent.ui.pushButtonCompute
        if not pushButtonComputeBatch:    
            pushButtonComputeBatch = self.parent.ui.pushButtonComputeBatch
        if not selection_changed:
            selection_changed = self.parent.selection_changed
        if not collect_parameter_values:
            collect_parameter_values = self.parent.collect_parameter_values
            
        self.experiment_getter = experiment_getter
        self.experiment = None
        self.hideHook = hideHook
        
        self.pushButtonComputeBatch = pushButtonComputeBatch
        self.pushButtonCompute = pushButtonCompute
        self.selection_changed = selection_changed
        self.collect_parameter_values = collect_parameter_values
        
        self.pushButtonCompute.setEnabled(True)
        self.pushButtonComputeBatch.setEnabled(False)

        self.ui.functionalityWidget.hide()
        self.setGeometry(geometry)
        self.adjustSize()

        self.data = {}
        self.failed_subjects = []

    def update(self, enabled):

        if not self.experiment:
            return

        if enabled:
            self.ui.functionalityWidget.show()
            self.adjustSize()
            self.pushButtonCompute.setEnabled(False)
            self.pushButtonComputeBatch.setEnabled(True)

            subject_names = sorted(self.experiment.subjects.keys())
             
            for name in subject_names:
                item = QtWidgets.QListWidgetItem(name)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.listWidgetSubjects.addItem(item)

        else:
            self.ui.listWidgetSubjects.clear()
            self.ui.functionalityWidget.hide()
            self.adjustSize()
            self.pushButtonCompute.setEnabled(True)
            self.pushButtonComputeBatch.setEnabled(False)

            if self.hideHook:
                self.hideHook()
        
    def on_listWidgetSubjects_currentItemChanged(self, item):
        if not item:
            return
        
        # if item.checkState() != QtCore.Qt.Checked:
        #     return
        
        subject_name = str(item.text())
        if subject_name in self.data.keys():
            data_dict = self.data[subject_name]
        else:
            data_dict = {}
        self.selection_changed(subject_name, data_dict)
    
    def showWidget(self, enabled):
        self.experiment = self.experiment_getter()

        if self.experiment:
            self.update(enabled)
        
    def on_pushButtonApply_clicked(self, checked=None):
        """Saves parameters to selected subject's eog parameters dictionary.
        """
        if checked is None: 
            return
        item = self.ui.listWidgetSubjects.currentItem()
        if item is None:
            return
        item.setCheckState(QtCore.Qt.Checked)
        
        subject = self.experiment.subjects[str(item.text())]
        params = self.collect_parameter_values()
        if params:
            self.data[subject.subject_name] = params

    def on_pushButtonApplyAll_clicked(self, checked=None):
        """
        """
        if checked is None: 
            return

        for i in range(self.ui.listWidgetSubjects.count()):
            item = self.ui.listWidgetSubjects.item(i)
            item.setCheckState(QtCore.Qt.Checked)
            name = str(item.text())
            if name in self.experiment.subjects:
                params = self.collect_parameter_values()
                if params:
                    self.data[name] = params 
 
    def on_pushButtonRemove_clicked(self, checked=None):
        """Removes subject from the list of subjects to be processed."""
        if checked is None:
            return
        #item = self.ui.widget.ui.listWidgetSubjects.currentItem()
        item = self.ui.listWidgetSubjects.currentItem()
        if item is None:
            message = 'Select a subject to remove.'
            messagebox(self, message)
            return
        item.setCheckState(QtCore.Qt.Unchecked)

    @property
    def selected_subjects(self):
        subject_names = [] 
        for i in range(self.ui.listWidgetSubjects.count()):
            item = self.ui.listWidgetSubjects.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                subject_names.append(item.text())
                
        return subject_names

    def cleanup(self, parent=None):
        if len(self.failed_subjects) > 0:
            rows = []
            rows.append('Failed calculation for subjects:')
            
            for subject, message in self.failed_subjects:
                rows.append(subject.subject_name + ' (' + message + ')')
                
            if not parent:
                parent = self.parent.parent
            
            messagebox(parent, '\n'.join(rows))
        self.data = {}
        self.failed_subjects = []
        self.ui.checkBoxBatch.setChecked(False)
        self.ui.functionalityWidget.hide()
        
