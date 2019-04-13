import os
import logging
import shutil

from PyQt5 import QtWidgets

from meggie.ui.general.tabs.mainWindowTabInducedUi import Ui_mainWindowTabInduced  # noqa

from meggie.ui.analysis.TFRDialogMain import TFRDialog
from meggie.ui.analysis.TFRPlotTopologyDialogMain import TFRPlotTopologyDialog
from meggie.ui.analysis.TSEPlotDialogMain import TSEPlotDialog

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

from meggie.ui.widgets.epochWidgetMain import EpochWidget
from meggie.ui.general.groupAverageDialogMain import GroupAverageDialog

from meggie.code_meggie.analysis.spectral import group_average_tfr

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabInduced(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabInduced()
        self.ui.setupUi(self)

        self.epochList = EpochWidget(self, 
            epoch_getter=self.parent.get_epochs)
        self.epochList.setParent(self.ui.groupBoxEpochs)
        self.epochList.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)

        self.initialize_ui()


    def initialize_ui(self):

        if not self.parent.experiment:
            return

        self.epochList.clear_items()
        self.ui.listWidgetTFR.clear()

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        # populate epoch widget
        for epoch_name in sorted(active_subject.epochs.keys()):
            item = QtWidgets.QListWidgetItem(epoch_name)
            self.epochList.add_item(item)

        for name in sorted(active_subject.tfrs.keys()):
            item = QtWidgets.QListWidgetItem(name)
            self.ui.listWidgetTFR.addItem(item)

    def on_listWidgetTFR_currentItemChanged(self, item):
        if not item:
            self.ui.textBrowserTFRInfo.clear()
            return

        experiment = self.parent.experiment

        tfr_name = str(item.text())
        tfr = experiment.active_subject.tfrs.get(tfr_name)
        info = 'Name: ' + str(tfr_name) + '\n'

        conditions = list(tfr.tfrs.keys())
        if conditions and any(conditions):
            info += 'Conditions: ' + ', '.join(conditions) + '\n'

        try:
            freqs = list(tfr.tfrs.values())[0].freqs
            fmin, fmax = "%.1f" % freqs[0], "%.1f" % freqs[-1]
            info += 'Freqs: ' + fmin + ' - ' + fmax + ' hz\n'
        except:
            pass

        decim = tfr.decim
        info += 'Decim: ' + str(decim) + '\n'

        evoked_subtracted = tfr.evoked_subtracted
        info += 'Evoked subtracted: ' + str(evoked_subtracted) + '\n'

        n_cycles = tfr.n_cycles
        if type(n_cycles) is list:
            cmin, cmax = "%.1f" % n_cycles[0], "%.1f" % n_cycles[-1]
            info += 'Cycles: ' + cmin + ' - ' + cmax + '\n'
        else:
            info += 'Cycles: ' + str(n_cycles) + '\n'

        self.ui.textBrowserTFRInfo.setText(info)

    @property
    def preferencesHandler(self):
        return self.parent.preferencesHandler

    @property
    def update_ui(self):
        return self.parent.update_ui


    def on_pushButtonPlotTFR_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        tfr_item = self.ui.listWidgetTFR.currentItem()
        if not tfr_item:
            return

        self.tfr_plot_dialog = TFRPlotTopologyDialog(
            self, experiment, tfr_item.text())
        self.tfr_plot_dialog.show()

    def on_pushButtonPlotTSE_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        tfr_item = self.ui.listWidgetTFR.currentItem()
        if not tfr_item:
            return

        self.tse_plot_dialog = TSEPlotDialog(
            self, experiment, tfr_item.text())
        self.tse_plot_dialog.show()

    def on_pushButtonGroupAverage_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        if experiment.active_subject is None:
            return

        tfr_item = self.ui.listWidgetTFR.currentItem()
        if not tfr_item:
            return

        tfr_name = tfr_item.text()

        def average_groups_handler(groups):
            try:
                @threaded
                def group_average(*args, **kwargs):
                    group_average_tfr(experiment, tfr_name, groups)

                group_average(do_meanwhile=self.update_ui)
                self.initialize_ui()
                experiment.save_experiment_settings()
            except Exception as e:
                exc_messagebox(self, e)
                return

        handler = average_groups_handler
        self.group_average_dialog = GroupAverageDialog(experiment, handler) 
        self.group_average_dialog.show()


    def on_pushButtonDeleteTFR_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        tfr_item = self.ui.listWidgetTFR.currentItem()
        if not tfr_item:
            return

        message = 'Permanently remove a TFR?'
        reply = QtWidgets.QMessageBox.question(self, 'Delete TFR',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.parent.experiment.active_subject.remove_tfr(
                    tfr_item.text()
                )
            except Exception as e:
                exc_messagebox(self, e)

            self.parent.experiment.save_experiment_settings()
            self.initialize_ui()


    def on_pushButtonGroupDeleteTFR_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        tfr_item = self.ui.listWidgetTFR.currentItem()
        if not tfr_item:
            return

        tfr_name = tfr_item.text()

        message = 'Permanently remove TFR from all subjects?'
        reply = QtWidgets.QMessageBox.question(self, "Delete TFR's",
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for subject in experiment.subjects.values():
                if tfr_name in subject.tfrs:
                    subject.remove_tfr(
                        tfr_name,
                    )

        logging.getLogger('ui_logger').info("Removed TFR's.")
        experiment.save_experiment_settings()
        self.initialize_ui()


    def on_pushButtonComputeTFR_clicked(self, checked=None):
        """Open the dialog for plotting TFR from a single channel."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not experiment.active_subject:
            return
        
        if self.epochList.currentItem() is None:
            message = ('You must select at least one epochs collection '
                       'before TFR.')
            messagebox(self, message)
            return
        
        selected_items = self.epochList.ui.listWidgetEpochs.selectedItems()

        names = [item.text() for item in selected_items]
        
        self.tfr_dialog = TFRDialog(self, experiment, names)
        self.tfr_dialog.show()
        

