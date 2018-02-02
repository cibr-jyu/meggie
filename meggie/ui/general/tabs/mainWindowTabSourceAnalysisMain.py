from PyQt4 import QtGui
from meggie.ui.general.tabs.mainWindowTabSourceAnalysisUi import Ui_mainWindowTabSourceAnalysis

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.source_analysis as source_analysis

class MainWindowTabSourceAnalysis(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabSourceAnalysis()
        self.ui.setupUi(self)

        self.ui.tabWidgetSourceAnalysis.currentChanged.connect(
            self.on_currentChanged)

        # self.initialize()

        # self.ui.tableViewForwardModels.setModel(self.forwardModelModel)
        # for colnum in range(17, 21):
        #     self.ui.tableViewForwardModels.setColumnHidden(colnum, True)

        # self.ui.tableViewFModelsForCoregistration.setModel(self.forwardModelModel)
        # for colnum in range(16, 21):
        #     self.ui.tableViewFModelsForCoregistration.setColumnHidden(colnum,
        #                                                               True)

    def update_tabs(self):

        while self.ui.tabWidgetSourceAnalysis.count() > 0:
            self.ui.tabWidgetSourceAnalysis.removeTab(0)

        self.ui.tabWidgetSourceAnalysis.insertTab(1, self.ui.tabSourcePreparation, "Source modelling preparation")
        self.ui.tabWidgetSourceAnalysis.insertTab(2, self.ui.tabForwardModel, "Forward model creation")
        self.ui.tabWidgetSourceAnalysis.insertTab(3, self.ui.tabCoregistration, "Coregistration")
        self.ui.tabWidgetSourceAnalysis.insertTab(4, self.ui.tabForwardSolution, "Forward solution creation")
        self.ui.tabWidgetSourceAnalysis.insertTab(5, self.ui.tabNoiseCovariance, "Noise covariance")
        self.ui.tabWidgetSourceAnalysis.insertTab(6, self.ui.tabInverseOperator, "Inverse operator")
        self.ui.tabWidgetSourceAnalysis.insertTab(7, self.ui.tabSourceEstimate, "Source estimate")
        self.ui.tabWidgetSourceAnalysis.insertTab(8, self.ui.tabAnalysis, "Analysis")


    def on_currentChanged(self):
        pass

    def initialize(self):

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        # Check if the reconstructions have been copied to experiment folder
        if active_subject.check_reconFiles_copied():
            self.ui.lineEditRecon.setText('Reconstructed mri image already '
                                          'copied.')
        
        # Check if MRI's have been converted
        if active_subject.check_mne_setup_mri_run():
            self.ui.checkBoxConvertedToMNE.setChecked(True)

    def on_pushButtonBrowseRecon_clicked(self, checked=None):
        """
        Copies reconstructed mri files from the directory supplied by the user
        to the corresponding directory under the active subject directory
        """
        if checked is None:
            return

        if self.parent.experiment.active_subject is None:
            return

        activeSubject = self.parent.experiment.active_subject

        if activeSubject.check_reconFiles_copied():
            reply = QtGui.QMessageBox.question(self, 'Please confirm',
                                               "Do you really want to change "
                                               "the reconstructed files? This "
                                               "will invalidate all later "
                                               "source analysis work and "
                                               "clear the results of the "
                                               "later phases",
                                               QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.No:
                return

        path = str(QtGui.QFileDialog.getExistingDirectory(self,
                                                          "Select directory "
                                                          "of the "
                                                          "reconstructed "
                                                          "MRI image"))
        if path == '':
            return

        mriDir = os.path.join(path, 'mri')
        surfDir = os.path.join(path, 'surf')
        if not (os.path.isdir(mriDir) and os.path.isdir(surfDir)):
            msg = ("Reconstructed image directory should have both 'surf' "
                   "and 'mri' directories in it.")
            messagebox(self, msg)
            return

        try:
            fileManager.copy_recon_files(activeSubject, path)
            self.ui.lineEditRecon.setText(path)
        except Exception:
            msg = ('Could not copy files.')
            messagebox(self, msg)

        # initialize_ui

    def on_pushButtonCheckTalairach_clicked(self, checked=None):
        if checked is None:
            return

        print "Check Talairach clicked"


    def on_pushButtonSkullStrip_clicked(self, checked=None):
        if checked is None:
            return

        print "Skull Strip clicked"


    def on_pushButtonCheckSurfaces_clicked(self, checked=None):
        if checked is None:
            return

        print "Check surfaces clicked"

    def on_pushButtonCheckSegmentations_clicked(self, checked=None):
        if checked is None:
            return

        print "Check Segmentations clicked"


    def on_pushButtonConvertToMNE_clicked(self, checked=None):
        if checked is None:
            return

        active_subject = self.parent.experiment.active_subject
        if active_subject is None:
            return

        try:
            source_analysis.convert_mri_to_mne(active_subject)
        except Exception as e:
            exc_messagebox(self, e)

        # self.initialize_ui()



    def on_pushButtonCheckSurfaces_clicked(self, checked=None):
        if checked is None:
            return

        subject = self.caller.experiment.active_subject
        mne.viz.plot_bem(subject='', subjects_dir=subject.reconFiles_directory, orientation='coronal')

    def _update_source_estimates(self):
        """Helper for updating source estimates to list."""
        self.ui.listWidgetSourceEstimate.clear()
        subject = self.caller.experiment.active_subject
        dir = subject._stc_directory
        stcs = [f for f in os.listdir(dir) if
                os.path.isfile(os.path.join(dir, f)) and f.endswith('lh.stc')]
        for stc in stcs:
            if os.path.isfile(os.path.join(dir, stc[:-6] + 'rh.stc')):
                self.ui.listWidgetSourceEstimate.addItem(stc[:-7])

        for stc_dir in [f for f in os.listdir(dir) if
                        os.path.isdir(os.path.join(dir, f))]:  # epochs dirs
            for stc_file in os.listdir(os.path.join(dir, stc_dir)):
                if stc_file.endswith('lh.stc'):
                    continue  # don't add duplicates
                if os.path.isfile(os.path.join(dir, stc_dir,
                                               stc_file[:-6] + 'rh.stc')):
                    self.ui.listWidgetSourceEstimate.addItem(os.path.join(
                        stc_dir, stc_file[:-7]))


    def on_pushButtonVisStc_clicked(self, checked=None):
        """Visualize source estimates."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
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


    def on_pushButtonPlotCov_clicked(self, checked=None):
        """Plots the covariance matrix."""
        if checked is None:
            return
        self.caller.plot_covariance()

    def on_pushButtonComputeInverse_clicked(self, checked=None):
        """Compute inverse operator clicked."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        fwd_name = str(self.ui.listWidgetForwardSolution.currentItem().text())
        inv = self.caller.compute_inverse(fwd_name)
        _initializeInverseOperatorList(self.ui.listWidgetInverseOperator,
                                       self.caller.experiment.active_subject)

    def on_pushButtonMakeSourceEstimate_clicked(self, checked=None):
        """Make source estimate clicked."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        ui = self.ui
        if ui.radioButtonRaw.isChecked():
            inst_name = self.caller.experiment.active_subject.subject_name
            type = 'raw'
        elif ui.radioButtonEpoch.isChecked():
            inst_name = str(self.epochList.currentItem().text())
            type = 'epochs'
        # elif ui.radioButtonEvoked.isChecked():
        #    inst_name = str(ui.listWidgetInverseEvoked.currentItem().text())
        #    type = 'evoked'
        dir = self.caller.experiment.active_subject._source_analysis_directory
        self.sourceEstimateDialog = SourceEstimateDialog(self, inst_name, type)
        self.sourceEstimateDialog.stc_computed.connect(self.
            _update_source_estimates)
        self.sourceEstimateDialog.show()


    def on_pushButtonMNE_AnalyzeCoregistration_clicked(self, checked=None):
        if checked is None:
            return
        return

    def on_pushButtonComputeCovarianceRaw_clicked(self, checked=None):
        """
        Open a dialog for computing noise covariance matrix based on raw file
        (measurement file with a subject but without epochs, or an empty room
        measurement).
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.covarianceRawDialog = CovarianceRawDialog(self)
        self.covarianceRawDialog.show()

    def on_pushButtonComputeCovarianceEpochs_clicked(self, checked=None):
        """
        Open a dialog for computing noise covariance matrix based on data
        before epochs.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.covarianceEpochDialog = CovarianceEpochDialog(self)
        self.covarianceEpochDialog.show()


    def on_pushButtonMNECoregistration_clicked(self, checked=None):
        """
        Open a dialog for coregistering the currently selected
        forward model in tableViewFModelsForCoregistration.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.tableViewFModelsForCoregistration.selectedIndexes() == []:
            msg = 'Please select a forward model to (re-)coregister.'
            messagebox(self, msg)
            return

        self.caller.coregister_with_mne_gui_coregistration()

    def on_pushButtonCreateForwardSolution_clicked(self, checked=None):
        """
        Open a dialog for creating a forward solution for the currently
        selected forward model in tableViewFModelsForSolution.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.tableViewFModelsForSolution.selectedIndexes() == []:
            message = ('Please select a forward model to (re)create a forward '
                       'solution for.')
            messagebox(self, message)
            return

        self.fSolutionDialog = ForwardSolutionDialog(self)
        self.fSolutionDialog.fwd_sol_computed.connect(self.initialize_ui)
        self.fSolutionDialog.show()



    def on_pushButtonBrowseCoregistration_clicked(self, checked=None):
        """
        Open a file browser dialog for the user to choose
        a translated coordinate file to use with the currently selected forward
        model.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        activeSubject = self.caller.experiment._active_subject
        tableView = self.ui.tableViewFModelsForCoregistration

        # Selection for the view is SingleSelection / SelectRows, so this
        # should return indexes for single row.
        selectedRowIndexes = tableView.selectedIndexes()
        selectedFmodelName = selectedRowIndexes[0].data()

        subjectPath = activeSubject._subject_path
        targetName = os.path.join(subjectPath, 'sourceAnalysis',
                                  'forwardModels', selectedFmodelName,
                                  'reconFiles', 'reconFiles-trans.fif')

        path = QtGui.QFileDialog.getOpenFileName(self, 'Select the existing '
                                                 'coordinate file (the file '
                                                 'should end with '
                                                 '"-trans.fif")')
        if path == '':
            return
        else:
            try:
                shutil.copyfile(path, targetName)
            except IOError:
                msg = 'There was a problem while copying the coordinate file.'
                messagebox(self, msg)

        self.forwardModelModel.initialize_model()



    def on_pushButtonRemoveSelectedForwardModel_clicked(self, checked=None):
        """
        Removes selected forward model from the forward model list and
        from the disk.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.tableViewForwardModels.selectedIndexes() == []:
            message = 'Please select a forward model to remove.'
            messagebox(self, message)
            return

        reply = QtGui.QMessageBox.question(self, 'Removing forward model',
                                           'Do you really want to remove the '
                                           'selected forward model, including '
                                           'the coregistration and forward '
                                           'solution files related to it?',
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.No:
            return

        tableView = self.ui.tableViewForwardModels

        # Selection for the view is SingleSelection / SelectRows, so this
        # should return indexes for single row.
        selectedRowIndexes = tableView.selectedIndexes()
        selectedRowNumber = selectedRowIndexes[0].row()
        fmname = selectedRowIndexes[0].data()
        subject = self.caller.experiment.active_subject

        try:
            fileManager.remove_fModel_directory(fmname, subject)
            self.forwardModelModel.removeRows(selectedRowNumber)
            self.initialize_ui()
        except Exception:
            msg = ('There was a problem removing forward model. Nothing was '
                   'removed.')
            messagebox(self, msg)



    def on_pushButtonCreateNewForwardModel_clicked(self, checked=None):
        """
        Open up a dialog for creating a new forward model.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.fmodelDialog = ForwardModelDialog(self)
        self.fmodelDialog.show()


    def update_covariance_info_box(self):
        """
        Fills the info box in the covariance tab with info about the
        current covariance matrix info for the active subject, if said info
        exists.
        """
        path = self.caller.experiment.active_subject._source_analysis_directory
        cvParamFilePath = os.path.join(path, 'covariance.param')

        cvdict = None
        if os.path.isfile(cvParamFilePath):
            try:
                cvdict = fileManager.unpickle(cvParamFilePath)
            except Exception:
                pass

        if self.ui.frameCovarianceInfoWidget.layout() is not None:
            sip.delete(self.ui.frameCovarianceInfoWidget.layout())

        for child in self.ui.frameCovarianceInfoWidget.children():
            child.setParent(None)

        covLayout = QtGui.QGridLayout()
        self.ui.frameCovarianceInfoWidget.setLayout(covLayout)

        if cvdict is None:
            covarianceWidgetNone = CovarianceWidgetNone()
            covLayout.addWidget(covarianceWidgetNone)
            return


        if cvdict['covarianceSource'] == 'raw':
            covarianceWidgetRaw = CovarianceWidgetRaw()
            cvwui = covarianceWidgetRaw.ui
            if cvdict['rawsubjectname'] is not None:
                cvwui.textBrowserBasedOn.setText(cvdict['rawsubjectname'])
            else:
                cvwui.textBrowserBasedOn.setText(cvdict['rawfilepath'])
            cvwui.textBrowserTmin.setText(str(cvdict['starttime']))
            cvwui.textBrowserTmax.setText(str(cvdict['endtime']))
            cvwui.textBrowserTstep.setText(str(cvdict['tstep']))
            if cvdict['reject'] is not None:
                txt = str(cvdict.get('reject').get('grad', ''))
                cvwui.textBrowserGradPeakCovariance.setText(txt)
                txt = str(cvdict.get('reject').get('mag', ''))
                cvwui.textBrowserMagPeakCovariance.setText(txt)
                txt = str(cvdict.get('reject').get('eeg', ''))
                cvwui.textBrowserEEGPeakCovariance.setText(txt)
                txt = str(cvdict.get('reject').get('eog', ''))
                cvwui.textBrowserEOGPeakCovariance.setText(txt)
            if cvdict['flat'] is not None:
                txt = str(cvdict.get('flat').get('grad', ''))
                cvwui.textBrowserFlatGrad.setText(txt)
                txt = str(cvdict.get('flat').get('mag', ''))
                cvwui.textBrowserFlatMag.setText(txt)
                txt = str(cvdict.get('flat').get('eeg', ''))
                cvwui.textBrowserFlatEEG.setText(txt)
                txt = str(cvdict.get('flat').get('eog', ''))
                cvwui.textBrowserFlatEOG.setText(txt)
                txt = str(cvdict.get('flat').get('ecg', 'Not used'))
                cvwui.textBrowserFlatECG.setText(txt)
            covLayout.addWidget(covarianceWidgetRaw)


        if cvdict['covarianceSource'] == 'epochs':
            covarianceWidgetEpochs = CovarianceWidgetEpochs()
            cvwui = covarianceWidgetEpochs.ui

            for collection_name in cvdict['collection_names']:
                cvwui.listWidgetEpochs.addItem(collection_name)

            cvwui.textBrowserTmin.setText(str(cvdict['tmin']))
            cvwui.textBrowserTmax.setText(str(cvdict['tmax']))

            if cvdict['keep_sample_mean'] == True:
                cvwui.labelKeepSampleValue.setText('True')
            else:
                cvwui.labelKeepSampleValue.setText('False')

            cvwui.labelMethodValue.setText(cvdict['method'])
            covLayout.addWidget(covarianceWidgetEpochs)
