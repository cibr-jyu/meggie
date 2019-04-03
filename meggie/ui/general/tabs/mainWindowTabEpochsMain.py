import os
import logging
import shutil

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.ui.general.tabs.mainWindowTabEpochsUi import Ui_mainWindowTabEpochs  # noqa

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

from meggie.ui.epoching.eventSelectionDialogMain import EventSelectionDialog
from meggie.ui.analysis.visualizeEpochChannelDialogMain import VisualizeEpochChannelDialog

from meggie.ui.widgets.epochWidgetMain import EpochWidget

from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.utils.units import get_scaling

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabEpochs(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabEpochs()
        self.ui.setupUi(self)

        self.epochList = EpochWidget(self, 
            epoch_getter=self.parent.get_epochs,
            parameter_setter=self.show_epoch_collection_parameters)
        self.epochList.setParent(self.ui.groupBoxEpochCollections)

        mode = QtWidgets.QAbstractItemView.SingleSelection
        self.epochList.setSelectionMode(mode)

        self.initialize_ui()

    def initialize_ui(self):

        if not self.parent.experiment:
            return

        self.clear_epoch_collection_parameters()
        self.epochList.clear_items()

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        epochs_items = active_subject.epochs
        if epochs_items is not None:
            for name in sorted(epochs_items.keys()):
                self.epochList.add_item(name)

        # Select the first item on epoch list
        if self.epochList.ui.listWidgetEpochs.count() > 1:
            self.epochList.ui.listWidgetEpochs.setCurrentRow(0)

        # self.update_ui()

    def update_ui(self):
        self.parent.update_ui()

    def clear_epoch_collection_parameters(self):
        """
        Clears epoch collection parameters on mainWindow Epoching tab.
        """
        self.ui.textBrowserTmin.clear()
        self.ui.textBrowserTmax.clear()
        self.ui.textBrowserGrad.clear()
        self.ui.textBrowserMag.clear()
        self.ui.textBrowserEEG.clear()
        self.ui.textBrowserStim.clear()
        self.ui.textBrowserEOG.clear()
        self.ui.textBrowserWorkingFile.clear()

    def show_epoch_collection_parameters(self, epochs):
        """
        Shows parameters from the currently chosen epochs.

        Keyword arguments:
        epochs -- Epochs object
        """
        # Set default/empty values for epoch parameters.
        self.clear_epoch_collection_parameters()
        params = epochs.params

        if params is None:
            logging.getLogger('ui_logger').warning(
                'Epochs parameters not found!')
            return

        self.ui.textBrowserTmin.setText(str(params['tmin']) + ' s')
        self.ui.textBrowserTmax.setText(str(params['tmax']) + ' s')

        # Creates dictionary of strings instead of qstrings for rejections.
        params_rejections_str = dict((str(key), value) for key, value in
                                     params['reject'].items())

        if 'mag' in params_rejections_str:
            factor = params_rejections_str['mag']
            self.ui.textBrowserMag.setText(
                str(factor) + ' ' + get_unit('mag'))
        else:
            self.ui.textBrowserMag.setText('-1')

        if 'grad' in params_rejections_str:
            factor = params_rejections_str['grad']
            self.ui.textBrowserGrad.setText(
                str(factor) + ' ' + get_unit('grad'))
        else:
            self.ui.textBrowserGrad.setText('-1')

        if 'eeg' in params_rejections_str:
            factor = params_rejections_str['eeg']
            self.ui.textBrowserEEG.setText(
                str(factor) + ' ' + get_unit('eeg'))
        else:
            self.ui.textBrowserEEG.setText('-1')

        if 'eog' in params_rejections_str:
            factor = params_rejections_str['eog']
            self.ui.textBrowserEOG.setText(
                str(factor) + ' ' + get_unit('eog'))
        else:
            self.ui.textBrowserEOG.setText('-1')

        if 'stim' in params_rejections_str:
            self.ui.textBrowserStim.setText('Yes')
        else:
            self.ui.textBrowserStim.setText('-1')

        self.ui.textBrowserWorkingFile.setText(
            epochs.path)


    def on_pushButtonDeleteEpochs_clicked(self, checked=None):
        """Delete the selected epoch collection."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        if self.epochList.isEmpty():
            return

        if self.epochList.currentItem() is None:
            messagebox(self, 'No epochs selected')

        item_str = self.epochList.currentItem().text()

        message = 'Permanently remove epochs?'
        reply = QtWidgets.QMessageBox.question(self, 'delete epochs',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                experiment.active_subject.remove_epochs(
                    item_str,
                )
            except Exception as e:
                exc_messagebox(self, e)
	    
            experiment.save_experiment_settings()
            # update mainwindow ui, as epochs are shown in multiple tabs
            self.parent.initialize_ui()


    def on_pushButtonGroupDeleteEpochs_clicked(self, checked=None):

        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        if self.epochList.isEmpty():
            return

        if self.epochList.currentItem() is None:
            messagebox(self, 'No epochs selected')

        collection_name = self.epochList.currentItem().text()

        message = 'Permanently remove epoch collection from all subjects?'
        reply = QtWidgets.QMessageBox.question(self, 'delete epochs',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for subject in experiment.subjects.values():
                if collection_name in subject.epochs:
                    try:
                        subject.remove_epochs(
                            collection_name,
                        )
                    except Exception as exc:
                        logging.getLogger('ui_logger').warning(
                            'Could not remove epochs for ' +
                            subject.subject_name)

            experiment.save_experiment_settings()
            self.parent.initialize_ui()

    def on_pushButtonCreateEpochs_clicked(self, checked=None):
        """Open the epoch dialog."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.epochParameterDialog = EventSelectionDialog(self, experiment)
        self.epochParameterDialog.show()

    def on_pushButtonVisualizeEpochChannels_clicked(self, checked=None):
        """Plot image over epochs channel"""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        if self.epochList.isEmpty():
            messagebox(self, 'Create epochs before visualizing.')
            return

        if self.epochList.currentItem() is None:
            message = 'Please select an epoch collection from the list.'
            messagebox(self, message)
            return

        name = str(self.epochList.currentItem().text())
        epochs = experiment.active_subject.epochs.get(name)
        self.visualizeEpochs = VisualizeEpochChannelDialog(epochs)
        self.visualizeEpochs.show()

    def on_pushButtonEpochsPlot_clicked(self, checked=None):
        """Call ``epochs.plot``."""

        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        item = self.epochList.currentItem()
        if item is None:
            message = 'No epochs collection selected.'
            messagebox(self, message)
            return

        epochs_name = str(item.text())
        epochs = experiment.active_subject.epochs.get(epochs_name)

        def handle_close(event):
            fileManager.save_epoch(epochs, overwrite=True)
            self.initialize_ui()

        fig = epochs.raw.plot(block=True, show=True)

        fig.canvas.mpl_connect('close_event', handle_close)

