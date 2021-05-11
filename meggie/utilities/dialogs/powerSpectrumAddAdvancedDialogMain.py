""" Contains a class for logic of the add advanced dialog.
"""
import logging

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.powerSpectrumAddAdvancedDialogUi import Ui_PowerSpectrumAddAdvancedDialog
from meggie.utilities.dialogs.bitSelectionDialogMain import BitSelectionDialog

from meggie.utilities.messaging import messagebox


class PowerSpectrumAddAdvancedDialog(QtWidgets.QDialog):
    """ Contains logic of the add advanced dialog.
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.intervals = []
        self.ui = Ui_PowerSpectrumAddAdvancedDialog()
        self.ui.setupUi(self)
        self.parent = parent

    def on_pushButtonStartEdit_clicked(self, checked=None):
        if checked is None:
            return
        self.bitDialog = BitSelectionDialog(self, self.ui.spinBoxStartMask,
                                            self.ui.spinBoxStartId)
        self.bitDialog.show()

    def on_pushButtonEndEdit_clicked(self, checked=None):
        if checked is None:
            return
        self.bitDialog = BitSelectionDialog(self, self.ui.spinBoxEndMask,
                                            self.ui.spinBoxEndId)
        self.bitDialog.show()

    def accept(self):
        average_group = str(self.ui.comboBoxAvgGroup.currentText())
        start_use_events = self.ui.radioButtonStartUseEvents.isChecked()
        end_use_events = self.ui.radioButtonEndUseEvents.isChecked()
        start_use_start = self.ui.radioButtonStartUseStart.isChecked()
        end_use_start = self.ui.radioButtonEndUseStart.isChecked()
        start_id = self.ui.spinBoxStartId.value()
        start_mask = self.ui.spinBoxStartMask.value()
        end_id = self.ui.spinBoxEndId.value()
        end_mask = self.ui.spinBoxEndMask.value()
        start_offset = self.ui.doubleSpinBoxStartOffset.value()
        end_offset = self.ui.doubleSpinBoxEndOffset.value()

        if start_use_events:
            start = ('events', start_id, start_mask, start_offset)
        elif start_use_start:
            start = ('start', None, None, start_offset)
        else:
            start = ('end', None, None, start_offset)

        if end_use_events:
            end = ('events', end_id, end_mask, end_offset)
        elif end_use_start:
            end = ('start', None, None, end_offset)
        else:
            end = ('end', None, None, end_offset)

        interval = (average_group, start, end)

        self.parent.add_intervals([('dynamic', interval)])
        self.close()
