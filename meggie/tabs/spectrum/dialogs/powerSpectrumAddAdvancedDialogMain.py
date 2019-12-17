"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.tabs.spectrum.dialogs.powerSpectrumAddAdvancedDialogUi import Ui_PowerSpectrumAddAdvancedDialog
from meggie.utilities.dialogs.bitSelectionDialogMain import BitSelectionDialog

from meggie.utilities.messaging import messagebox


class PowerSpectrumAddAdvancedDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        """
        """
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
        average_group = int(self.ui.comboBoxAvgGroup.currentText())
        use_events_start = self.ui.radioButtonStartUseEvents.isChecked()
        use_events_end = self.ui.radioButtonEndUseEvents.isChecked()
        start_id = self.ui.spinBoxStartId.value()
        start_mask = self.ui.spinBoxStartMask.value()
        end_id = self.ui.spinBoxEndId.value()
        end_mask = self.ui.spinBoxEndMask.value()
        start_offset = self.ui.doubleSpinBoxStartOffset.value()
        end_offset = self.ui.doubleSpinBoxEndOffset.value()

        if use_events_start:
            start = (start_id, start_mask, start_offset)
        else:
            start = (None, None, start_offset)

        if use_events_end:
            end = (end_id, end_mask, end_offset)
        else:
            end = (None, None, end_offset)

        interval = (average_group, start, end)

        self.parent.add_intervals([('dynamic', interval)])
        self.close()
