"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox

from meggie.utilities.dialogs.permutationTestDialogUi import Ui_permutationTestDialog
from meggie.utilities.dialogs.groupSelectionDialogMain import GroupSelectionDialog


class PermutationTestDialog(QtWidgets.QDialog):

    def __init__(self, experiment, parent, handler, meggie_item,
                 limit_frequency=False, limit_time=False, limit_location=True, limit_location_vals=[]):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_permutationTestDialog()
        self.ui.setupUi(self)

        self.handler = handler
        self.experiment = experiment

        self.limit_frequency = limit_frequency
        self.limit_time = limit_time
        self.limit_location = limit_location

        if not limit_location:
            self.ui.groupBoxLocation.hide()
        else:
            for loc in limit_location_vals:
                self.ui.comboBoxLocation.addItem(loc)

        if not limit_time:
            self.ui.groupBoxTime.hide()
        else:
            self.ui.doubleSpinBoxFrequencyTmin.setValue(meggie_item.times[0])
            self.ui.doubleSpinBoxFrequencyTmax.setValue(meggie_item.times[-1])

        if not limit_frequency:
            self.ui.groupBoxFrequency.hide()
        else:
            self.ui.doubleSpinBoxFrequencyFmin.setValue(meggie_item.freqs[0])
            self.ui.doubleSpinBoxFrequencyFmax.setValue(meggie_item.freqs[-1])

        self.meggie_item = meggie_item

        self.groups = {}

    def on_pushButtonGroups_clicked(self, checked=None):
        if checked is None:
            return

        def handler(groups):
            if not groups:
                return

            self.groups = groups
            self.ui.listWidgetGroups.clear()
            for key, names in sorted(groups.items(), key=lambda x: x[0]):
                for name in sorted(names):
                    item_name = str(key) + ": " + str(name)
                    self.ui.listWidgetGroups.addItem(item_name)

        dialog = GroupSelectionDialog(self.experiment, self, handler)
        dialog.show()

    def accept(self):
        """
        """
        if not self.groups:
            messagebox(self, "You should select some groups first")
            return

        if self.ui.radioButtonWithinSubjects.isChecked():
            design = 'within-subjects'
        else:
            design = 'between-subjects'

        if design == 'between-subjects' and len(self.groups) <= 1:
            messagebox(self, "At least two groups are needed for between-subjects design")
            return

        if design == 'within-subjects':
            conditions = self.meggie_item.content.keys()
            if len(conditions) <= 1:
                messagebox(self, "At least two conditions are needed for within-subjects design")
                return

        time_limits = None
        frequency_limits = None
        location_limits = None

        if self.limit_time and self.ui.radioButtonTimeEnabled.isChecked():
            tmin = self.ui.doubleSpinBoxTimeTmin.value()
            tmax = self.ui.doubleSpinBoxTimeTmax.value()
            time_limits = tmin, tmax

        if self.limit_frequency and self.ui.radioButtonFrequencyEnabled.isChecked():
            fmin = self.ui.doubleSpinBoxFrequencyFmin.value()
            fmax = self.ui.doubleSpinBoxFrequencyFmax.value()
            frequency_limits = fmin, fmax

        if self.limit_location and self.ui.radioButtonLocationEnabled.isChecked():
            location_limits = self.ui.comboBoxLocation.currentText()

        threshold = self.ui.doubleSpinBoxClusterThreshold.value()
        significance = self.ui.doubleSpinBoxClusterSignificance.value()
        n_permutations = self.ui.spinBoxNPermutations.value()

        self.handler(self.groups, time_limits, frequency_limits, location_limits, threshold,
                     significance, n_permutations, design)
        self.close()
