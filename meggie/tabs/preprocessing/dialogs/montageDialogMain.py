"""
"""

import os
import pkg_resources
import logging

from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.decorators import threaded

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.tabs.preprocessing.dialogs.montageDialogUi import Ui_montageDialog


class MontageDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_montageDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        montage_dir = pkg_resources.resource_filename(
            'mne', os.path.join('channels', 'data', 'montages'))

        for fname in sorted(os.listdir(montage_dir)):
            self.ui.comboBoxSelectFromList.addItem(fname)
         
        self.current_montage_fname = None
        self.ui.radioButtonMontageFromList.setChecked(True)

        # find out if montage already set.

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def on_pushButtonSelectFromFile_clicked(self, checked=None):
        """
        Called when browse montage button is clicked.
        Opens a file dialog for selecting a file.
        """
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
        """
        """
        if checked:
            self.ui.labelCurrentContent.setText(self.current_montage_fname)

    def on_comboBoxSelectFromList_currentIndexChanged(self, item):
        """
        """
        if self.ui.radioButtonMontageFromList.isChecked():
            self.ui.labelCurrentContent.setText(str(item))

    def on_radioButtonMontageFromList_toggled(self, checked):
        """
        """
        if checked:
            selection = self.ui.comboBoxSelectFromList.currentText()
            self.ui.labelCurrentContent.setText(selection)


    @threaded
    def set_montage(self, subject):
        """
        """
        head_size = float(self.ui.doubleSpinBoxHeadSize.value())
        raw = subject.get_raw()
        if self.ui.radioButtonMontageFromList.isChecked():
            selection = self.ui.comboBoxSelectFromList.currentText()
            selection = os.path.splitext(selection)[0]
            montage = mne.channels.make_standard_montage(
                selection, head_size=head_size)
            raw.set_montage(montage)
        else:
            selection = self.current_montage_fname
            montage = mne.channels.read_custom_montage(selection,
                head_size=head_size)
            raw.set_montage(montage)

    def accept(self):
        """
        """
        subject = self.experiment.active_subject
        try:
            self.set_montage(subject, do_meanwhile=self.parent.update_ui)
            subject.save()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        logging.getLogger('ui_logger').info('Finished setting montage.')
        self.close()

    def acceptBatch(self):
        """
        """
        experiment = self.experiment
        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.set_montage(subject, 
                                     do_meanwhile=self.parent.update_ui)
                    subject.save()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception(str(exc))

        self.batching_widget.cleanup()

        logging.getLogger('ui_logger').info('Finished setting montage.')
        self.close()

