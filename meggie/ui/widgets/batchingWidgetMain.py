'''
Created on 22.1.2016

@author: jaolpeso
'''
import sys
from PyQt4 import QtGui, QtCore

from meggie.code_meggie.general.caller import Caller

from meggie.ui.widgets.batchingWidgetUi import Ui_BatchingWidget
from meggie.ui.general import messageBoxes

class BatchingWidget(QtGui.QWidget):
    """Generic widget for handling batching in several dialogs.
    The parent dialogs need to implement the following methods:
        - selection_changed
        - collect_parameter_values 
    """
    caller = Caller.Instance()
    
    def __init__(self, parent, replaceable_widget, *args, **kwargs):
        super(BatchingWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_BatchingWidget()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.groupBoxBatch.hide()
        self.adjustSize()
        self.data = {}
        
        widget_margins = replaceable_widget.geometry()
        self.setGeometry(widget_margins)
        
        for subject in self.caller.experiment._subjects:
            item = QtGui.QListWidgetItem(subject._subject_name)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.listWidgetSubjects.addItem(item)


    def on_listWidgetSubjects_currentItemChanged(self, item):
        print str(item.text())
        #self.parent.selection_changed(item.text())
    
    def showWidget(self, disabled):
        if disabled:
            self.ui.groupBoxBatch.show()
            self.adjustSize()
            #TODO: self.parent.adjustSize() (doesnt work with scrollArea?)
        else:
            self.ui.groupBoxBatch.hide()
            self.adjustSize()
            #TODO: self.parent.adjustSize() (doesnt work with scrollArea?)

    def on_pushButtonApply_clicked(self, checked=None):
        """Saves parameters to selected subject's eog parameters dictionary.
        """
        if checked is None: return
        item = self.ui.listWidgetSubjects.currentItem()
        if item is None:
            return
        item.setCheckState(QtCore.Qt.Checked)
        dictionary = self.parent.collect_parameter_values(True)
        for subject in self.caller.experiment._subjects:
            if subject._subject_name == str(item.text()):
                #subject._eog_params = dictionary
                #self.params[]
                pass

    def on_pushButtonApplyAll_clicked(self, checked=None):
        """Saves parameters to selected subjects' eog parameters dictionaries.
        """
        if checked is None: return
        for i in range(self.ui.listWidgetSubjects.count()):
            item = self.ui.listWidgetSubjects.item(i)
            item.setCheckState(QtCore.Qt.Checked)
            for subject in self.caller.experiment._subjects:
                if str(item.text()) == subject._subject_name:
                    subject._eog_params = self.parent.collect_parameter_values(True)

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
