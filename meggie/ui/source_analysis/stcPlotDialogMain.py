"""
"""

import logging
import os

from PyQt5 import QtWidgets

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.ui.source_analysis.stcPlotDialogUi import Ui_stcPlotDialog

from meggie.code_meggie.general.source_analysis import plot_source_estimate


from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox


class stcPlotDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, experiment, stc_name):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_stcPlotDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.stc_name = stc_name

        meggie_stc = experiment.active_subject.stcs[stc_name]

        if meggie_stc.type == 'raw':
            self.ui.comboBoxSource.setEnabled(False)
            self.ui.labelSource.setEnabled(False)
        else:
            for key in meggie_stc.keys(experiment):
                self.ui.comboBoxSource.addItem(key)

           
    def accept(self):
        """
        """

        meggie_stc = self.experiment.active_subject.stcs[self.stc_name]

        if meggie_stc.type == 'evoked':
            source = str(self.ui.comboBoxSource.currentText())
            stc = meggie_stc.get_data(self.experiment)[source]
        elif meggie_stc.type == 'epochs':
            source = str(self.ui.comboBoxSource.currentText())
            stc = meggie_stc.get_data(self.experiment)[int(source)]
        else:
            stc = meggie_stc.get_data(self.experiment)

        if self.ui.radioButtonInitialTime.isChecked():
            initial_time = self.ui.doubleSpinBoxInitialTime.value()
        else:
            _, initial_time = stc.get_peak(hemi=None)

        try:
            plot_source_estimate(self.experiment, stc, initial_time)
        except ImportError:
            message = ("You need to install pysurfer for 3d visualization."
                       "This can be done with e.g `pip install pysurfer`")
            messagebox(self, message, exec_=True)

        
