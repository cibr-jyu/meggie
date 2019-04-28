import os
import logging
import shutil

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.ui.general.tabs.mainWindowTabSourceAnalysisUi import Ui_mainWindowTabSourceAnalysis  # noqa
from meggie.ui.source_analysis.forwardSolutionDialogMain import ForwardSolutionDialog  # noqa
from meggie.ui.source_analysis.linearSourceEstimateDialogMain import LinearSourceEstimateDialog  # noqa
from meggie.ui.source_analysis.lcmvDialogMain import LCMVDialog
from meggie.ui.source_analysis.covarianceRawDialogMain import CovarianceRawDialog  # noqa
from meggie.ui.source_analysis.covarianceEpochDialogMain import CovarianceEpochDialog  # noqa
from meggie.ui.source_analysis.stcPlotDialogMain import stcPlotDialog

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabSourceAnalysis(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabSourceAnalysis()
        self.ui.setupUi(self)

        self.ui.tabWidgetSourceAnalysis.currentChanged.connect(
            self.on_currentChanged)

        self.initialize_ui()

    def on_currentChanged(self):
        pass

    def update_tabs(self):

        while self.ui.tabWidgetSourceAnalysis.count() > 0:
            self.ui.tabWidgetSourceAnalysis.removeTab(0)

        self.ui.tabWidgetSourceAnalysis.insertTab(
            1, self.ui.tabSourcePreparation, "Source modelling preparation")
        self.ui.tabWidgetSourceAnalysis.insertTab(
            2, self.ui.tabCoregistration, "Coregistration")
        self.ui.tabWidgetSourceAnalysis.insertTab(
            3, self.ui.tabForwardSolution, "Forward solution")
        self.ui.tabWidgetSourceAnalysis.insertTab(
            4, self.ui.tabNoiseCovariance, "Covariance matrix")
        self.ui.tabWidgetSourceAnalysis.insertTab(
            5, self.ui.tabSourceEstimate, "Source estimate")
        self.ui.tabWidgetSourceAnalysis.insertTab(
            6, self.ui.tabAnalysis, "Analysis")

    def initialize_ui(self):

        if not self.parent.experiment:
            return

        self.ui.listWidgetForwardSolutionsFwd.clear()
        self.ui.listWidgetForwardSolutionsStc.clear()
        self.ui.listWidgetStcEpochs.clear()
        self.ui.listWidgetStcEvoked.clear()
        self.ui.listWidgetSourceEstimatesStc.clear()
        self.ui.listWidgetSourceEstimatesAna.clear()
        self.ui.listWidgetCovariances.clear()

        active_subject = self.parent.experiment.active_subject

        if not active_subject:
            return

        # Check if the reconstructions have been copied to experiment folder
        if active_subject.check_reconFiles_copied():
            self.ui.checkBoxCopyUnderSubject.setChecked(True)

        if active_subject.check_bem_surfaces():
            self.ui.checkBoxBem.setChecked(True)

        # populate forward solutions in forward solutions tab
        solutions = active_subject.get_forward_solution_names()
        for solution in solutions:
            item = QtWidgets.QListWidgetItem(solution)
            self.ui.listWidgetForwardSolutionsFwd.addItem(item)

        # populate forward solutions in source estimate tab
        solutions = active_subject.get_forward_solution_names()
        for solution in solutions:
            item = QtWidgets.QListWidgetItem(solution)
            self.ui.listWidgetForwardSolutionsStc.addItem(item)

        # populate epochs in source estimate tab
        for collection in active_subject.epochs:
            item = QtWidgets.QListWidgetItem(collection)
            self.ui.listWidgetStcEpochs.addItem(item)

        # populate evoked in source estimate tab
        for evoked in active_subject.evokeds:
            item = QtWidgets.QListWidgetItem(evoked)
            self.ui.listWidgetStcEvoked.addItem(item)

        # populate stc in source estimate tab
        for stc in active_subject.stcs:
            item = QtWidgets.QListWidgetItem(stc)
            self.ui.listWidgetSourceEstimatesStc.addItem(item)

        # populate stc in analysis tab
        for stc in active_subject.stcs:
            item = QtWidgets.QListWidgetItem(stc)
            self.ui.listWidgetSourceEstimatesAna.addItem(item)

        # populate covfiles in cov tab
        for covfile in active_subject.get_covfiles():
            item = QtWidgets.QListWidgetItem(covfile)
            self.ui.listWidgetCovariances.addItem(item)

        # set transfile state to selected if transfile exists
        if active_subject.check_transfile_exists():
            self.ui.checkBoxCoregistrationSelected.setChecked(True)

    def on_pushButtonBrowseRecon_clicked(self, checked=None):
        """
        Copies reconstructed mri files from the directory supplied by the user
        to the corresponding directory under the active subject directory
        """
        if checked is None:
            return

        path = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(self,
                                                           "Select directory of the reconstructed MRI image")))

        if path == '':
            return

        self.ui.lineEditRecon.setText(path)

    def on_pushButtonCopyUnderSubject_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if not active_subject:
            return

        if active_subject.check_reconFiles_copied():
            reply = QtWidgets.QMessageBox.question(self, 'Please confirm',
                                                   "Do you really want to change "
                                                   "the reconstructed files?",
                                                   QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return

        path = self.ui.lineEditRecon.text()

        mri_dir = os.path.join(path, 'mri')
        surf_dir = os.path.join(path, 'surf')
        if not os.path.isdir(mri_dir) or not os.path.isdir(surf_dir):
            msg = ("Reconstructed image directory should have both 'surf' "
                   "and 'mri' directories in it.")
            messagebox(self, msg)
            return

        # copy files
        try:
            @threaded
            def copy_recon():
                fileManager.copy_recon_files(active_subject, path)
            copy_recon(do_meanwhile=self.parent.update_ui)
        except Exception as e:
            exc_messagebox(self, e)

        self.initialize_ui()

    def on_pushButtonBem_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if not active_subject:
            return

        # set environment variables
        os.environ['SUBJECTS_DIR'] = active_subject.source_analysis_directory
        os.environ['SUBJECT'] = active_subject.mri_subject_name

        use_atlas = self.ui.checkBoxAtlas.isChecked()

        # create bem surfaces for later steps
        try:
            @threaded
            def watershed_bem():
                mne.make_watershed_bem(
                    active_subject.mri_subject_name, atlas=use_atlas, overwrite=True)
            watershed_bem(do_meanwhile=self.parent.update_ui)
        except Exception as e:
            exc_messagebox(self, e)

        self.initialize_ui()

    def on_pushButtonCoregistrationGUI_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment

        if experiment and experiment.active_subject:
            subject = experiment.active_subject
        else:
            return

        # set environment variables for coregistration gui
        os.environ['SUBJECTS_DIR'] = subject.source_analysis_directory
        os.environ['SUBJECT'] = subject.mri_subject_name

        inst = subject.working_file_path
        try:
            mne.coregistration(inst=inst, subject=subject.mri_subject_name,
                               head_high_res=False)
        except Exception as exc:
            exc_messagebox(self, exc)

    def on_pushButtonCoregistrationBrowse_clicked(self, checked=None):
        """
        Copies reconstructed mri files from the directory supplied by the user
        to the corresponding directory under the active subject directory
        """
        if checked is None:
            return

        if self.parent.experiment and self.parent.experiment.active_subject:
            subject = self.parent.experiment.active_subject
        else:
            return

        path = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getOpenFileName(self,
                                                      "Select the coordinate MEG-MRI coordinate transformation file")[0]))

        if path == '':
            return

        src = path
        dst = subject.transfile_path

        logging.getLogger('ui_logger').info('Copying ' + src + ' to ' + dst)
        try:
            shutil.copyfile(src, dst)
        except Exception as exc:
            exc_messagebox(self, exc)

        self.ui.lineEditCoregistrationBrowse.setText(path)

        self.initialize_ui()

    def on_pushButtonCreateForwardSolution_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        self.forwardSolutionDialog = ForwardSolutionDialog(self,
                                                           experiment=self.parent.experiment, on_close=self.initialize_ui)
        self.forwardSolutionDialog.show()

    def on_pushButtonImportForwardSolution_clicked(self, checked=None):
        if checked is None:
            return

        if self.parent.experiment and self.parent.experiment.active_subject:
            subject = self.parent.experiment.active_subject
        else:
            return

        path = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getOpenFileName(self,
                                                      "Select a forward solution file")[0]))

        if not path.endswith('fwd.fif'):
            messagebox(self, "Forward solution file should end with -fwd.fif")
            return

        src = path
        dst = os.path.join(subject.forward_solutions_directory,
                           os.path.basename(path))

        logging.getLogger('ui_logger').info('Copying ' + src + ' to ' + dst)
        try:
            shutil.copyfile(src, dst)
        except Exception as exc:
            exc_messagebox(self, exc)

        self.initialize_ui()

    def on_pushButtonRemoveForwardSolution_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        active_subject = self.parent.experiment.active_subject

        try:
            sol = str(
                self.ui.listWidgetForwardSolutionsFwd.currentItem().text())
        except AttributeError:
            return

        reply = QtWidgets.QMessageBox.question(self, 'Please confirm',
                                               "Do you really want to remove "
                                               "the the selected solution?",
                                               QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.No:
            return

        path = os.path.join(active_subject.forward_solutions_directory,
                            sol)

        logging.getLogger('ui_logger').info(
            'Removing solution file from ' + path)

        os.remove(path)

        self.initialize_ui()

    def on_pushButtonCovarianceRaw_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        self.covarianceRawDialog = CovarianceRawDialog(self,
                                                       self.parent.experiment,
                                                       on_close=self.initialize_ui)

        self.covarianceRawDialog.show()

    def on_pushButtonCovarianceEpochs_clicked(self, checked=None):
        """
        Open a dialog for computing noise covariance matrix based on data
        before epochs.
        """
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        self.covarianceEpochDialog = CovarianceEpochDialog(self,
                                                           self.parent.experiment, on_close=self.initialize_ui)

        self.covarianceEpochDialog.show()

    def on_pushButtonLinear_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        active_subject = self.parent.experiment.active_subject

        try:
            fwd_name = str(
                self.ui.listWidgetForwardSolutionsStc.currentItem().text())
        except BaseException:
            messagebox(self, "Have you selected the forward solution?")
            return

        try:
            if self.ui.radioButtonStcRaw.isChecked():
                inst_type = 'raw'
                inst_name = active_subject.working_file_name
            elif self.ui.radioButtonStcEpochs.isChecked():
                inst_type = 'epochs'
                inst_name = str(
                    self.ui.listWidgetStcEpochs.currentItem().text())
            elif self.ui.radioButtonStcEvoked.isChecked():
                inst_type = 'evoked'
                inst_name = str(
                    self.ui.listWidgetStcEvoked.currentItem().text())
        except Exception as e:
            messagebox(self, "Have you selected the dataset?")
            return

        self.linearSourceEstimateDialog = LinearSourceEstimateDialog(self,
                                                                     fwd_name, inst_type, inst_name, self.parent.experiment,
                                                                     on_close=self.initialize_ui)

        self.linearSourceEstimateDialog.show()

    def on_pushButtonLCMV_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        active_subject = self.parent.experiment.active_subject

        try:
            fwd_name = str(
                self.ui.listWidgetForwardSolutionsStc.currentItem().text())
        except BaseException:
            messagebox(self, "Have you selected the forward solution?")
            return

        try:
            if self.ui.radioButtonStcRaw.isChecked():
                inst_type = 'raw'
                inst_name = active_subject.working_file_name
            elif self.ui.radioButtonStcEpochs.isChecked():
                inst_type = 'epochs'
                inst_name = str(
                    self.ui.listWidgetStcEpochs.currentItem().text())
            elif self.ui.radioButtonStcEvoked.isChecked():
                inst_type = 'evoked'
                inst_name = str(
                    self.ui.listWidgetStcEvoked.currentItem().text())
        except Exception as e:
            messagebox(self, "Have you selected the dataset?")
            return

        self.lcmvDialog = LCMVDialog(self,
                                     fwd_name, inst_type, inst_name, self.parent.experiment,
                                     on_close=self.initialize_ui)

        self.lcmvDialog.show()

    def on_pushButtonStcRemove_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        stc = str(self.ui.listWidgetSourceEstimatesStc.currentItem().text())
        try:
            self.parent.experiment.active_subject.remove_stc(stc)
        except Exception as exc:
            exc_messagebox(self, exc)

        self.parent.experiment.save_experiment_settings()
        self.initialize_ui()

    def on_pushButtonCovariancePlot_clicked(self, checked=None):
        """ """
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        active_subject = self.parent.experiment.active_subject

        info = active_subject.get_working_file(preload=False).info

        current_covfile = str(
            self.ui.listWidgetCovariances.currentItem().text())

        path = os.path.join(active_subject.cov_directory,
                            current_covfile)
        cov = mne.read_cov(path)
        cov.plot(info)

    def on_pushButtonCovarianceRemove_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        active_subject = self.parent.experiment.active_subject

        try:

            current_covfile = str(
                self.ui.listWidgetCovariances.currentItem().text())
        except AttributeError:
            return

        reply = QtWidgets.QMessageBox.question(self, 'Please confirm',
                                               "Do you really want to remove the the selected covariance matrix?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.No:
            return

        path = os.path.join(active_subject.cov_directory,
                            current_covfile)

        logging.getLogger('ui_logger').info(
            'Removing covariance matrix file from ' + path)

        os.remove(path)

        self.initialize_ui()

    def on_pushButtonPlotSourceEstimate_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        logging.getLogger('ui_logger').info("Plotting source estimate..")

        stc_item = self.ui.listWidgetSourceEstimatesAna.currentItem()
        try:
            stc_name = str(stc_item.text())
        except AttributeError as e:
            messagebox(self, "You should select the source estimate first.")
            return

        self.stcPlotDialog = stcPlotDialog(self.parent.experiment, stc_name)
        self.stcPlotDialog.show()
