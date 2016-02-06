"""
Author: Jaakko Leppakangas
"""
from os import listdir
from os.path import join, isfile
from PyQt4 import QtCore, QtGui

from meggie.code_meggie.general.caller import Caller
from sourceEstimateDialogUi import Ui_SourceEstimateDialog

class SourceEstimateDialog(QtGui.QDialog):
    """
    Dialog for making a source estimate.
    Args:
        parent: MainWindow.
        inst_name: Name of the data instance to use.
        type: str to indicate type of data. One of ['raw', 'epochs', 'evoked'].
    """
    caller = Caller.Instance()
    stc_computed = QtCore.pyqtSignal()

    def __init__(self, parent, evoked_name, type):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_SourceEstimateDialog()
        self.ui.setupUi(self)

        self.ui.labelEvoked.setText(evoked_name)
        dir = self.caller.experiment.active_subject._source_analysis_directory
        operators = [f for f in listdir(dir) if
                     isfile(join(dir, f)) and f.endswith('-inv.fif') ]
        self.ui.comboBoxInverseOperator.addItems(operators)
        self.type = type

    def accept(self):
        """
        Method for performing source estimate computation. Called on ok.
        """
        inst_name = str(self.ui.labelEvoked.text())  # TODO: change label name
        inv_name = str(self.ui.comboBoxInverseOperator.currentText())
        method = str(self.ui.comboBoxMethod.currentText())
        stc = self.caller.make_source_estimate(inst_name, self.type,
                                               inv_name, method)
        self.stc_computed.emit()
        self.close()
