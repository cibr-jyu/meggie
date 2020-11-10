"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.tabs.evoked.dialogs.singleChannelDialogUi import Ui_singleChannelDialog


class SingleChannelDialog(QtWidgets.QDialog):

    def __init__(self, parent, evoked, handler):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_singleChannelDialog()
        self.ui.setupUi(self)
        self.handler = handler
        self.evoked = evoked

        # times = list(evoked.content.values())[0].times
        # tmin, tmax = times[0], times[-1]

        # self.ui.doubleSpinBoxStart.setValue(tmin)
        # self.ui.doubleSpinBoxStart.setMinimum(tmin)
        # self.ui.doubleSpinBoxStart.setMaximum(tmax)
        # self.ui.doubleSpinBoxEnd.setMinimum(tmin)
        # self.ui.doubleSpinBoxEnd.setMaximum(tmax)
        # self.ui.doubleSpinBoxEnd.setValue(tmax)

    def accept(self):
        """
        """

        ymax = self.ui.doubleSpinBoxMax.value()
        ymin = self.ui.doubleSpinBoxMin.value()
        yscale = (ymin, ymax)

        smoothing = self.ui.doubleSpinBoxSmoothing.value()

        title = ''

        ch_name = ''

        legend = None

        self.handler(ch_name, smoothing, title, legend, yscale)

        self.close()
