import os
import logging
import shutil

from PyQt4 import QtGui

from meggie.ui.general.tabs.mainWindowTabSourceAnalysisUi import Ui_mainWindowTabSourceAnalysis  # noqa
from meggie.ui.source_analysis.forwardSolutionDialogMain import ForwardSolutionDialog  # noqa
from meggie.ui.source_analysis.inverseOperatorDialogMain import InverseOperatorDialog  # noqa
from meggie.ui.source_analysis.covarianceRawDialogMain import CovarianceRawDialog  # noqa
from meggie.ui.source_analysis.covarianceEpochDialogMain import CovarianceEpochDialog  # noqa

from meggie.ui.utils.messaging import messagebox

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabSourceAnalysis(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
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

        self.ui.tabWidgetSourceAnalysis.insertTab(1, self.ui.tabSourcePreparation, "Source modelling preparation")
        self.ui.tabWidgetSourceAnalysis.insertTab(2, self.ui.tabCoregistration, "Coregistration")
        self.ui.tabWidgetSourceAnalysis.insertTab(3, self.ui.tabForwardSolution, "Forward solution creation")
        self.ui.tabWidgetSourceAnalysis.insertTab(4, self.ui.tabNoiseCovariance, "Noise covariance")
        self.ui.tabWidgetSourceAnalysis.insertTab(5, self.ui.tabInverseOperator, "Inverse operator")
        self.ui.tabWidgetSourceAnalysis.insertTab(6, self.ui.tabSourceEstimate, "Source estimate")
        self.ui.tabWidgetSourceAnalysis.insertTab(7, self.ui.tabAnalysis, "Analysis")


    def initialize_ui(self):

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        # Check if the reconstructions have been copied to experiment folder
        if active_subject.check_reconFiles_copied():
            self.ui.checkBoxCopyUnderSubject.setChecked(True)

        if active_subject.check_bem_surfaces():
            self.ui.checkBoxBem.setChecked(True)

        # populate forward solutions in forward solutions tab
        solutions = active_subject.get_forward_solution_names()
        self.ui.listWidgetForwardSolutionsFwd.clear()
        for solution in solutions:
            item = QtGui.QListWidgetItem(solution)
            self.ui.listWidgetForwardSolutionsFwd.addItem(item)

        # populate forward solutions in inverse operator tab
        solutions = active_subject.get_forward_solution_names()
        self.ui.listWidgetForwardSolutionsInv.clear()
        for solution in solutions:
            item = QtGui.QListWidgetItem(solution)
            self.ui.listWidgetForwardSolutionsInv.addItem(item)

        # populate inverse operators in inverse operator tab
        operators = active_subject.get_inverse_operator_names()
        self.ui.listWidgetInverseOperatorsInv.clear()
        for operator in operators:
            item = QtGui.QListWidgetItem(operator)
            self.ui.listWidgetInverseOperatorsInv.addItem(item)

        # set transfile state to selected if transfile exists
        if active_subject.check_transfile_exists():
            self.ui.checkBoxCoregistrationSelected.setChecked(True)

        # set covariance state to selected if covariance file exists
        if active_subject.check_covfile_exists():
            self.ui.checkBoxCovarianceComputed.setChecked(True)

        
    def on_pushButtonBrowseRecon_clicked(self, checked=None):
        """
        Copies reconstructed mri files from the directory supplied by the user
        to the corresponding directory under the active subject directory
        """
        if checked is None:
            return

        path = str(QtGui.QFileDialog.getExistingDirectory(self,
            "Select directory of the reconstructed MRI image"))

        if path == '':
            return

        self.ui.lineEditRecon.setText(path)

    def on_pushButtonCopyUnderSubject_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if active_subject.check_reconFiles_copied():
            reply = QtGui.QMessageBox.question(self, 'Please confirm',
                                               "Do you really want to change "
                                               "the reconstructed files?",
                                               QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.No:
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
            fileManager.copy_recon_files(active_subject, path)
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonBem_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        # set environment variables
        os.environ['SUBJECTS_DIR'] = active_subject.source_analysis_directory
        os.environ['SUBJECT'] = 'reconFiles'

        use_atlas = self.ui.checkBoxAtlas.isChecked()

        # create bem surfaces for later steps
        try:
            mne.make_watershed_bem('reconFiles', atlas=use_atlas)
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonCheckTalairach_clicked(self, checked=None):
        if checked is None:
            return

        logging.getLogger('ui_logger').info("Check Talairach clicked")


    def on_pushButtonSkullStrip_clicked(self, checked=None):
        if checked is None:
            return

        logging.getLogger('ui_logger').info("Skull Strip clicked")


    def on_pushButtonCheckSurfaces_clicked(self, checked=None):
        if checked is None:
            return

        logging.getLogger('ui_logger').info("Check surfaces clicked")

    def on_pushButtonCheckSegmentations_clicked(self, checked=None):
        if checked is None:
            return

        logging.getLogger('ui_logger').info("Check Segmentations clicked")


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
        os.environ['SUBJECT'] = 'reconFiles'

        inst = subject.working_file_path
        mne.coregistration(inst=inst, subject='reconFiles', head_high_res=False)

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

        path = str(QtGui.QFileDialog.getOpenFileName(self,
            "Select the coordinate MEG-MRI coordinate transformation file"))

        if path == '':
            return

        src = path
        dst = subject.transfile_path

        logging.getLogger('ui_logger').info('Copying ' + src + ' to ' + dst)
        try:
            shutil.copyfile(src, dst)
        except Exception as exc:
            exc_messagebox(exc)

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

        path = str(QtGui.QFileDialog.getOpenFileName(self,
            "Select a forward solution file"))

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
            exc_messagebox(exc)

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
            sol = str(self.ui.listWidgetForwardSolutionsFwd.currentItem().text())
        except AttributeError:
            return

        reply = QtGui.QMessageBox.question(self, 'Please confirm',
                                           "Do you really want to remove "
                                           "the the selected solution?",
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.No:
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

        self.covarianceRawDialog = CovarianceRawDialog(self.parent.experiment, 
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

        self.covarianceEpochDialog = CovarianceEpochDialog(
            self.parent.experiment, on_close=self.initialize_ui)

        self.covarianceEpochDialog.show()

    def on_pushButtonCovariancePlot_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        logging.getLogger('ui_logger').info("Covariance plot clicked")

    def on_pushButtonComputeInverse_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        active_subject = self.parent.experiment.active_subject

        fwd_name = str(self.ui.listWidgetForwardSolutionsInv.currentItem().text())

        if not fwd_name:
            return

        self.inverseOperatorDialog = InverseOperatorDialog(self,
            fwd_name, self.parent.experiment, on_close=self.initialize_ui)

        self.inverseOperatorDialog.show()


    def on_pushButtonVisStc_clicked(self, checked=None):
        """Visualize source estimates."""
        if checked is None:
            return
        if self.parent.experiment.active_subject is None:
            return

        stc = str(self.ui.listWidgetSourceEstimate.currentItem().text())
        self.plotStcDialog = PlotStcDialog(self, stc)
        self.plotStcDialog.show()


    def on_pushButtonStcFreq_clicked(self, checked=None):
        """
        """
        if checked is None:
            return
        self.stcFreqDialog = StcFreqDialog(self)
        self.stcFreqDialog.show()

    def on_pushButtonMakeSourceEstimate_clicked(self, checked=None):
        """Make source estimate clicked."""
        if checked is None:
            return
        if self.parent.experiment.active_subject is None:
            return

        ui = self.ui
        if ui.radioButtonRaw.isChecked():
            inst_name = self.parent.experiment.active_subject.subject_name
            type = 'raw'
        elif ui.radioButtonEpoch.isChecked():
            inst_name = str(self.epochList.currentItem().text())
            type = 'epochs'
        dir = self.parent.experiment.active_subject._source_analysis_directory
        self.sourceEstimateDialog = SourceEstimateDialog(self, inst_name, type)
        self.sourceEstimateDialog.stc_computed.connect(self.
            _update_source_estimates)
        self.sourceEstimateDialog.show()


