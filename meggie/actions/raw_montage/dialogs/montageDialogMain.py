""" Contains a class for logic of montage dialog.
"""

import os
import pkg_resources
import logging

import mne

from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import meggie.utilities.filemanager as filemanager

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.actions.raw_montage.dialogs.montageDialogUi import Ui_montageDialog


class MontageDialog(QtWidgets.QDialog):
    """ Contains logic for montage dialog.
    """
    def __init__(self, parent, experiment, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_montageDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment
        self.handler = handler

        montage_dir = pkg_resources.resource_filename(
            'mne', os.path.join('channels', 'data', 'montages'))

        for fname in sorted(os.listdir(montage_dir)):
            self.ui.comboBoxSelectFromList.addItem(fname)
         
        self.current_montage_fname = None
        self.ui.radioButtonMontageFromList.setChecked(True)

        # find out if montage already set.

        self.batching_widget = BatchingWidget(
            experiment_getter=self._experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def _experiment_getter(self):
        return self.experiment

    def on_pushButtonSelectFromFile_clicked(self, checked=None):
        if checked is None:
            return

        home = filemanager.homepath()

        fname = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getOpenFileName(
                self, 'Open file', home, 
                "Montage-files (*.txt *.elc *.sfp);;"
                "All files (*.*)")[0]))

        self.current_montage_fname = fname
        if self.ui.radioButtonMontageFromFile.isChecked():
            self.ui.labelCurrentContent.setText(self.current_montage_fname)

    def on_radioButtonMontageFromFile_toggled(self, checked):
        if checked:
            self.ui.labelCurrentContent.setText(self.current_montage_fname)

    def on_comboBoxSelectFromList_currentIndexChanged(self, item):
        if self.ui.radioButtonMontageFromList.isChecked():
            self.ui.labelCurrentContent.setText(str(item))

    def on_radioButtonMontageFromList_toggled(self, checked):
        if checked:
            selection = self.ui.comboBoxSelectFromList.currentText()
            self.ui.labelCurrentContent.setText(selection)

    def _get_params(self):
        params = {}
        head_size = float(self.ui.doubleSpinBoxHeadSize.value())
        if self.ui.radioButtonMontageFromList.isChecked():
            selection = self.ui.comboBoxSelectFromList.currentText()
            selection = os.path.splitext(selection)[0]
            params['custom'] = False
            params['selection'] = selection
        else:
            params['custom'] = True
            params['selection'] = self.current_montage_fname

        params['head_size'] = head_size

        return params

    def accept(self):
        subject = self.experiment.active_subject

        params = self._get_params()

        try:
            self.handler(subject, params)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):
        experiment = self.experiment
        selected_subject_names = self.batching_widget.selected_subjects

        params = self._get_params()

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.handler(subject, params)
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        self.parent.initialize_ui()
        self.close()

