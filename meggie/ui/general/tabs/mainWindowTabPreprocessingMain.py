import os
import logging
import shutil

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtWidgets import QAbstractItemView


from meggie.ui.general.tabs.mainWindowTabPreprocessingUi import Ui_mainWindowTabPreprocessing  # noqa

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

from meggie.ui.preprocessing.eogParametersDialogMain import EogParametersDialog
from meggie.ui.preprocessing.ecgParametersDialogMain import EcgParametersDialog
from meggie.ui.preprocessing.eegParametersDialogMain import EegParametersDialog
from meggie.ui.preprocessing.addECGProjectionsMain import AddECGProjections
from meggie.ui.preprocessing.addEOGProjectionsMain import AddEOGProjections
from meggie.ui.preprocessing.badChannelsDialogMain import BadChannelsDialog
from meggie.ui.preprocessing.filterDialogMain import FilterDialog
from meggie.ui.preprocessing.icaDialogMain import ICADialog
from meggie.ui.preprocessing.resamplingDialogMain import ResamplingDialog
from meggie.ui.preprocessing.cropDialogMain import CropDialog
from meggie.ui.preprocessing.rereferencingDialogMain import RereferencingDialog

from meggie.code_meggie.preprocessing.projections import plot_projs_topomap

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabPreprocessing(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabPreprocessing()
        self.ui.setupUi(self)

        # Set bads not selectable
        self.ui.listWidgetBads.setSelectionMode(QAbstractItemView.NoSelection)

        self.initialize_ui()


    def initialize_ui(self):

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        self.ui.listWidgetProjs.clear()
        self.ui.listWidgetBads.clear()
        self.ui.checkBoxMaxFilterApplied.setChecked(False)
        self.ui.checkBoxICAApplied.setChecked(False)
        self.ui.checkBoxRereferenced.setChecked(False)
        self.ui.pushButtonApplyECG.setEnabled(False)
        self.ui.pushButtonApplyEOG.setEnabled(False)

        # Check whether ECG projections are calculated
        if active_subject.check_ecg_projs():
            self.ui.pushButtonApplyECG.setEnabled(True)

        # Check whether EOG (and old EEG) projections are calculated
        if active_subject.check_eog_projs():
            self.ui.pushButtonApplyEOG.setEnabled(True)

        # Check whether sss/tsss method is applied.
        if active_subject.check_sss_applied():
            self.ui.checkBoxMaxFilterApplied.setChecked(True)

        # Check whether ICA method is applied.
        if active_subject.ica_applied:
            self.ui.checkBoxICAApplied.setChecked(True)

        # Check whether Rereferenceing is applied.
        if active_subject.rereferenced:
            self.ui.checkBoxRereferenced.setChecked(True)

        raw = active_subject.get_working_file()

        projs = raw.info['projs']
        for proj in projs:
            self.ui.listWidgetProjs.addItem(str(proj))

        bads = raw.info['bads']
        for bad in bads:
            self.ui.listWidgetBads.addItem(bad)

    def update_ui(self):
        self.parent.update_ui()


    class RawBadsPlot(object):
        def __init__(self, parent, experiment):

            if parent.ui.checkBoxShowEvents.isChecked():
                events = experiment.active_subject.get_events()
            else:
                events = None
            try:
                raw = experiment.active_subject.get_working_file()  # noqa
                self.raw = raw.copy()
                fig = self.raw.plot(events=events)
                fig.canvas.mpl_connect('close_event', self.handle_close)
            except Exception as err:
                exc_messagebox(parent, err)
                return

        def handle_close(self, event):
            self.raw = None


    def on_pushButtonRawPlot_clicked(self, checked=None):
        """Call ``raw.plot``."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        # Create a plot where bad channels are not set by clicking them
        self.plot = MainWindowTabPreprocessing.RawBadsPlot(
            self, self.parent.experiment)

    def on_pushButtonCustomChannels_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.badChannelsDialog = BadChannelsDialog(self, experiment)
        self.badChannelsDialog.show()


    def on_pushButtonPlotProjections_clicked(self, checked=None):
        """Plots added projections as topomaps."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        raw = experiment.active_subject.get_working_file()
        if not raw.info['projs']:
            messagebox(self, "No added projections.")
            return

        try:
            plot_projs_topomap(experiment, raw)
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonEOG_clicked(self, checked=None):
        """Open the dialog for calculating the EOG PCA."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.eogDialog = EogParametersDialog(self, experiment)
        self.eogDialog.show()


    def on_pushButtonECG_clicked(self, checked=None):
        """Open the dialog for calculating the ECG PCA."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.ecgDialog = EcgParametersDialog(self, experiment)
        self.ecgDialog.show()

    def on_pushButtonApplyEOG_clicked(self, checked=None):
        """Open the dialog for applying the EOG-projections to the data."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        info = experiment.active_subject.get_working_file().info
        self.addEogProjs = AddEOGProjections(self, info['projs'],
                                             experiment)
        self.addEogProjs.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.addEogProjs.show()


    def on_pushButtonApplyECG_clicked(self, checked=None):
        """Open the dialog for applying the ECG-projections to the data."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        info = experiment.active_subject.get_working_file().info
        self.addEcgProjs = AddECGProjections(self, info['projs'],
                                             experiment)
        self.addEcgProjs.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.addEcgProjs.show()


    def on_pushButtonRemoveProj_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        if self.ui.listWidgetProjs.currentItem() is None:
            message = 'Select projection to remove.'
            messagebox(self, message)
            return

        selected_items = self.ui.listWidgetProjs.selectedItems()
        raw = experiment.active_subject.get_working_file()
        str_projs = [str(proj) for proj in raw.info['projs']]

        for item in selected_items:
            proj_name = item.text()
            if proj_name in str_projs:
                index = str_projs.index(proj_name)
                str_projs.pop(index)
                raw.info['projs'].pop(index)
                row = self.ui.listWidgetProjs.row(item)
                self.ui.listWidgetProjs.takeItem(row)

        directory = experiment.active_subject.subject_path
        subject_name = experiment.active_subject.working_file_name
        fname = os.path.join(directory, subject_name)
        fileManager.save_raw(experiment, raw, fname)
        self.initialize_ui()


    def on_pushButtonICA_clicked(self, checked=None):
        """
        Show the dialog for ICA preprocessing.
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.icaDialog = ICADialog(self, experiment)
        self.icaDialog.show()

    def on_pushButtonFilter_clicked(self, checked=None):
        """
        Show the dialog for filtering.
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.filterDialog = FilterDialog(self, experiment,
                                         self.parent.preferencesHandler)
        self.filterDialog.show()


    def on_pushButtonResampling_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.resamplingDialog = ResamplingDialog(self, experiment)
        self.resamplingDialog.show()

    def on_pushButtonCrop_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.cropDialog = CropDialog(self, experiment)
        self.cropDialog.show()

    def on_pushButtonRereferencing_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        self.rereferencingDialog = RereferencingDialog(self, experiment)
        self.rereferencingDialog.show()

