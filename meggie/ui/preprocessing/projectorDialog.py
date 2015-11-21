'''
Created on 8.9.2015

@author: Jaakko Leppakangas
'''
from PyQt4 import QtGui, QtCore

from code_meggie.general.caller import Caller
import messageBoxes


class ProjectorDialog(QtGui.QDialog):
    """
    Abstract class for combining the features of EOG and ECG dialogs.
    """
    caller = Caller.Instance()

    def __init__(self, parent, ui):
        QtGui.QDialog.__init__(self)
        self.ui = ui()
        self.ui.setupUi(self)
        self.parent = parent
        for subject in self.caller.experiment._subjects:
            item = QtGui.QListWidgetItem(subject._subject_name)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.listWidgetSubjects.addItem(item)

    def on_pushButtonRemove_clicked(self, checked=None):
        """Removes subject from the list of subjects to be processed."""
        if checked is None:
            return
        item = self.ui.listWidgetSubjects.currentItem()
        if item is None:
            message = 'Select a subject to remove.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
        item.setCheckState(QtCore.Qt.Unchecked)
