""" Contains a class for logic of the evoked topomap dialog.
"""
from PyQt5 import QtWidgets

from meggie.actions.evoked_plot_topomap.dialogs.evokedTopomapDialogUi import Ui_evokedTopomapDialog

from meggie.utilities.messaging import exc_messagebox


class EvokedTopomapDialog(QtWidgets.QDialog):
    """ Contains logic for the evoked topomap dialog.
    """
    def __init__(self, parent, evoked, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_evokedTopomapDialog()
        self.ui.setupUi(self)
        self.handler = handler
        self.evoked = evoked

        times = list(evoked.content.values())[0].times
        tmin, tmax = times[0], times[-1]

        self.ui.doubleSpinBoxStart.setValue(tmin)
        self.ui.doubleSpinBoxStart.setMinimum(tmin)
        self.ui.doubleSpinBoxStart.setMaximum(tmax)
        self.ui.doubleSpinBoxEnd.setMinimum(tmin)
        self.ui.doubleSpinBoxEnd.setMaximum(tmax)
        self.ui.doubleSpinBoxEnd.setValue(tmax)

    def accept(self):
        tmin = self.ui.doubleSpinBoxStart.value()
        tmax = self.ui.doubleSpinBoxEnd.value()
        step = self.ui.doubleSpinBoxStep.value()

        radius = None
        if self.ui.checkBoxRadius.isChecked():
            radius = self.ui.doubleSpinBoxRadius.value()

        try:
            self.handler(tmin, tmax, step, radius)
        except Exception as exc:
            exc_messagebox(self.parent, exc)

        self.close()

