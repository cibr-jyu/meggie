'''
Created on 16.6.2016

@author: jaolpeso
'''

from PyQt4 import QtCore
from PyQt4 import QtGui

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import fileManager

from meggie.ui.general.layoutDialogUi import Ui_Layout

class LayoutDialog(QtGui.QDialog):
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Layout()
        self.ui.setupUi(self)
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)
        self.ui.labelLayoutActive.setText(self.parent.caller.experiment.layout)
        
    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """
        Called when browse layout button is clicked.
        Opens a file dialog for selecting a file.
        """
        if checked is None:
            return
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                      '/home/', "Layout-files "
                                                      "(*.lout *.lay);;All "
                                                      "files (*.*)"))
        self.ui.labelLayout.setText(fname)

    @QtCore.pyqtSlot(int)
    def on_comboBoxLayout_currentIndexChanged(self, index):
        self.ui.labelLayout.setText(self.ui.comboBoxLayout.currentText())

    def accept(self):
        self.parent.caller.experiment.layout = self.ui.labelLayout.text()
        self.parent.caller.experiment.save_experiment_settings()
        self.close()