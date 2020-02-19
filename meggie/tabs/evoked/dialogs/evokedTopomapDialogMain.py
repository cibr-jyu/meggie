"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.tabs.evoked.dialogs.evokedTopomapDialogUi import Ui_evokedTopomapDialog


class EvokedTopomapDialog(QtWidgets.QDialog):

    def __init__(self, parent, evoked, handler):
        """
        """
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
        """
        """

        tmin = self.ui.doubleSpinBoxStart.value()
        tmax = self.ui.doubleSpinBoxEnd.value()
        step = self.ui.doubleSpinBoxStep.value()

        self.handler(tmin, tmax, step, self.evoked)

        self.close()
