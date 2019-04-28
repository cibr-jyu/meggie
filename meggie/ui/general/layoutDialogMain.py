"""
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.code_meggie.general import fileManager
from meggie.code_meggie.general.fileManager import homepath

from meggie.ui.general.layoutDialogUi import Ui_Layout


class LayoutDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Layout()
        self.ui.setupUi(self)
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)
        self.ui.labelLayoutActive.setText(self.parent.experiment.layout)

    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """
        Called when browse layout button is clicked.
        Opens a file dialog for selecting a file.
        """
        if checked is None:
            return

        home = homepath()

        fname = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                                      home, "Layout-files "
                                                      "(*.lout *.lay);;All "
                                                      "files (*.*)")[0]))
        self.ui.labelLayout.setText(fname)

    @QtCore.pyqtSlot(int)
    def on_comboBoxLayout_currentIndexChanged(self, index):
        self.ui.labelLayout.setText(self.ui.comboBoxLayout.currentText())

    def accept(self):
        self.parent.experiment.layout = self.ui.labelLayout.text()
        self.parent.experiment.save_experiment_settings()
        self.close()
