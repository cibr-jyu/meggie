"""
Author: Jaakko Leppakangas
"""

from PyQt4 import QtCore, QtGui

from meggie.code_meggie.general.caller import Caller
from plotStcDialogUi import Ui_PlotStcDialog

class PlotStcDialog(QtGui.QDialog):
    """
    Dialog for making a source estimate.
    Args:
        parent: MainWindow.
        stc_name: Name of the stc to use..
    """

    def __init__(self, parent, stc_name):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_PlotStcDialog()
        self.ui.setupUi(self)

        self.ui.labelStc.setText(stc_name)

    def accept(self):
        """Plot the source estimate. Called on ok."""
        caller = Caller.Instance()
        stc = str(self.ui.labelStc.text())
        hemi = str(self.ui.comboBoxHemi.currentText())
        surf = str(self.ui.comboBoxSurface.currentText())
        smooth = int(self.ui.spinBoxSmooth.value())
        alpha = float(self.ui.doubleSpinBoxAlpha.value())
        caller.plotStc(stc, hemi, surf, smooth, alpha)
        self.close()
