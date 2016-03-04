'''
Created on 22.1.2016

@author: jaolpeso
'''
import sys
from PyQt4 import QtGui, QtCore

from meggie.code_meggie.general.caller import Caller

from meggie.ui.widgets.batchingWidgetUi import Ui_BatchingWidget
from meggie.ui.general import messageBoxes
from copy import deepcopy

class BatchingWidget(QtGui.QWidget):
    """Generic widget for handling batching in several dialogs.
    The parent dialogs need to implement the following:
        - selection_changed          (method)
        - collect_parameter_values   (method)
        - pushButtonCompute          (QPushButton, signal: clicked() -> accept())
        - pushButtonComputeBatch     (QPushButton, signal: clicked() -> acceptBatch() <--create custom signal)
        - pushButtonCancel           (QPushButton, signal: clicked() -> reject())
        - widget                     (QWidget)
    """
    caller = Caller.Instance()
    
    def __init__(self, parent, *args, **kwargs):
        super(BatchingWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_BatchingWidget()
        self.ui.setupUi(self)
        self.parent = parent
        self.parent.ui.pushButtonCompute.setEnabled(True)
        self.parent.ui.pushButtonComputeBatch.setEnabled(False)
        self.ui.groupBoxBatch.hide()
        self.setGeometry(self.parent.ui.widget.geometry())
        self.adjustSize()

        self.data = {}
        
        for subject in self.caller.experiment._subjects:
            item = QtGui.QListWidgetItem(subject.subject_name)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.listWidgetSubjects.addItem(item)


    def on_listWidgetSubjects_currentItemChanged(self, item):
        #print str(item.text())
        subject_name = str(item.text())
        if subject_name in self.data.keys():
            data_dict = self.data[subject_name]
        else:
            data_dict = {}
        self.parent.selection_changed(subject_name, data_dict)
    
    def showWidget(self, disabled):
        if disabled:
            self.ui.groupBoxBatch.show()
            self.adjustSize()
            self.parent.ui.pushButtonCompute.setEnabled(False)
            self.parent.ui.pushButtonComputeBatch.setEnabled(True)
            #TODO: self.parent.adjustSize() (doesnt work with scrollArea?)
        else:
            self.ui.groupBoxBatch.hide()
            self.adjustSize()
            self.parent.ui.pushButtonCompute.setEnabled(True)
            self.parent.ui.pushButtonComputeBatch.setEnabled(False)
            #TODO: self.parent.adjustSize() (doesnt work with scrollArea?)

    def on_pushButtonApply_clicked(self, checked=None):
        """Saves parameters to selected subject's eog parameters dictionary.
        """
        if checked is None: return
        item = self.ui.listWidgetSubjects.currentItem()
        if item is None:
            return
        item.setCheckState(QtCore.Qt.Checked)
        for subject in self.caller.experiment.get_subjects():
            if subject.subject_name == str(item.text()):
                
                self.data[subject.subject_name] = self.parent.collect_parameter_values()
                
                """
                #TODO: pls come up with something practical instead, if the current style is the only way:
                #TODO: in case of events, need to use append to prevent setting the events list
                #to all of the subjects data
                params = self.parent.collect_parameter_values()
                if 'events' in params.keys():
                    self.data[subject.subject_name]['events'].append(params['events'])
                    params_copy = deepcopy(params)
                    del params_copy['events']
                self.data[subject.subject_name] = params_copy
                """
                

    def on_pushButtonApplyAll_clicked(self, checked=None):
        """Saves parameters to selected subjects' eog parameters dictionaries.
        """
        if checked is None: return
        for i in range(self.ui.listWidgetSubjects.count()):
            item = self.ui.listWidgetSubjects.item(i)
            item.setCheckState(QtCore.Qt.Checked)
            for subject in self.caller.experiment.get_subjects():
                if str(item.text()) == subject.subject_name:
                    params = self.parent.collect_parameter_values()
                    if params is not None:
                        self.data[subject.subject_name] = params 

    def on_pushButtonRemove_clicked(self, checked=None):
        """Removes subject from the list of subjects to be processed."""
        if checked is None:
            return
        #item = self.ui.widget.ui.listWidgetSubjects.currentItem()
        item = self.ui.listWidgetSubjects.currentItem()
        if item is None:
            message = 'Select a subject to remove.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
        item.setCheckState(QtCore.Qt.Unchecked)

def main():
    app = QtGui.QApplication(sys.argv)
    
    widget = BatchingWidget()
    widget.show()

    sys.exit(app.exec_())
    


if __name__ == '__main__':
    main()
