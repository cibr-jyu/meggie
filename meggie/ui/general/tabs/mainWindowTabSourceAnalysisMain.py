import os
import logging

import mne

from PyQt4 import QtGui

from meggie.ui.general.tabs.mainWindowTabSourceAnalysisUi import Ui_mainWindowTabSourceAnalysis

from meggie.ui.utils.messaging import messagebox

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

        self.initialize_ui()


    def update_tabs(self):

        while self.ui.tabWidgetSourceAnalysis.count() > 0:
            self.ui.tabWidgetSourceAnalysis.removeTab(0)

        self.ui.tabWidgetSourceAnalysis.insertTab(1, self.ui.tabSourcePreparation, "Source modelling preparation")
        self.ui.tabWidgetSourceAnalysis.insertTab(2, self.ui.tabCoregistration, "Coregistration")
        self.ui.tabWidgetSourceAnalysis.insertTab(3, self.ui.tabForwardModel, "Forward model creation")
        self.ui.tabWidgetSourceAnalysis.insertTab(4, self.ui.tabForwardSolution, "Forward solution creation")
        self.ui.tabWidgetSourceAnalysis.insertTab(5, self.ui.tabNoiseCovariance, "Noise covariance")
        self.ui.tabWidgetSourceAnalysis.insertTab(6, self.ui.tabInverseOperator, "Inverse operator")
        self.ui.tabWidgetSourceAnalysis.insertTab(7, self.ui.tabSourceEstimate, "Source estimate")
        self.ui.tabWidgetSourceAnalysis.insertTab(8, self.ui.tabAnalysis, "Analysis")


    def on_currentChanged(self):
        pass

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
            mne.bem.make_watershed_bem('reconFiles', atlas=use_atlas)
        except Exception as e:
            exc_messagebox(self, e)

# JOSSAIN VAIHEESSA MNE_SETUP_MRI

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


    def on_pushButtonMNECoregistration_clicked(self, checked=None):
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
        mne.gui.coregistration(inst=inst, subject='reconFiles', head_high_res=False)


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




## ===========
#
#
#
#class ForwardModelModel(QtCore.QAbstractTableModel):
#    """
#    Model class for forward model related views in MainWindow. Please don't get
#    confused by the "model" and "forward model" -
#    the former is model as in model-view-controller, the latter is an MNE term.
#    """
#    caller = Caller.Instance()
#
#    def __init__(self, parent=None):
#        QtCore.QAbstractTableModel.__init__(self)
#        self.parent = parent
#        
#        # Each dictionary in the list includes parameters for single forward
#        # model.
#        self.fmodelInfoList = []
#        
#        # Column headers i.e. names of parameters.
#        self.__headers = ['name', 'decim. method' , 'spacing', 'ico value', 
#                          'surfname', 'cps', 'atlas', 'triang. ico', 'homog',
#                          'innershift','outershift','skullshift', 'brainc',
#                          'skullc', 'scalpc', 'coregistered', 'fsolution',
#                          'includeMEG', 'includeEEG', 'minDist', 'ignoreRef']
#
#        # May well be None, if no experiment is loaded.
#        if self.caller.experiment == None:
#            return
#
#        self._fmodels_directory = None
#
#        # The experiment may not have an active subject, no need to try to
#        # initialize model in that case.
#        try:
#            self._fmodels_directory = self.caller._experiment._active_subject.\
#                      _forwardModels_directory
#        except AttributeError:
#            return
#
#        self.initialize_model()
#
#    def rowCount(self, parent):
#        """
#        The associated view should have as many rows as there are 
#        forward model names.
#        """
#        return len(self.fmodelInfoList)
#
#    def columnCount(self, parent):
#        """
#        The associated view should have as many columns as there are 
#        header fields, if we want to show all information.
#        """
#        return len(self.__headers)
#
#    def data(self, index, role=QtCore.Qt.DisplayRole):
#        """
#        Standard data method for the QAbstractTableModel.
#        """
#        if not index.isValid():
#            return QtCore.QVariant()
#        
#        # No need to use anything else but displayrole here. 
#        if role == QtCore.Qt.DisplayRole:
#            row = index.row()
#            column = index.column()
#            value = self.fmodelInfoList[row][column]
#            return value
#
#    def headerData(self, section, orientation, role):
#        
#        if role == QtCore.Qt.DisplayRole:
#            
#            if orientation == QtCore.Qt.Horizontal:
#                
#                if section < len(self.__headers):
#                    return self.__headers[section]
#                else:
#                    return "not implemented"
#
#    def removeRows(self, position, rows=1, parent= QtCore.QModelIndex()):
#        """
#        Removal of a single row from the model.
#        """
#        self.beginRemoveRows(parent, position, position + rows - 1)
#        singleFMitem = self.fmodelInfoList[position]
#        self.fmodelInfoList.remove(singleFMitem)
#        self.endRemoveRows()
#
#    def initialize_model(self):
#        """
#        Reads the active subject's forwardModels directory and populates the
#        data accordingly.
#        """
#        activeSubject = self.caller._experiment._active_subject
#        if activeSubject == None:
#            self._fmodels_directory = None
#            self.layoutAboutToBeChanged.emit()
#            del self.fmodelInfoList[:]
#            self.layoutChanged.emit()
#            return
#        
#        self._fmodels_directory = activeSubject._forwardModels_directory
#        fmsdir = self._fmodels_directory
#        
#        self.layoutAboutToBeChanged.emit()
#        
#        # Best to empty the list anyway, otherwise the forward models 
#        # from the previous active subject end up staying there.
#        del self.fmodelInfoList[:]
#            
#        for d in [name for name in os.listdir(fmsdir)
#                    if os.path.isdir(os.path.join(fmsdir, name))]:
#            
#            pmlist = self.create_single_FM_param_list(fmsdir, d)                
#            self.fmodelInfoList.append(pmlist)
#
#        self.layoutChanged.emit()
#
#    def create_single_FM_param_list(self, fmdir, fmname):
#        """
#        Creates a list of parameters corresponding to a single forward model.
#
#        Keyword arguments:
#        fmdir       -- the directory the forward models are located at.
#        fmname      -- the name of the forward model.
#        
#        Returns the list, or None if there is no such model.
#        
#        """ 
#        
#        # The param files don't exist by default, so lots of trying here.
#        try: 
#            sSpaceDict = fileManager.unpickle(os.path.join(fmdir, fmname, 
#                                              'setupSourceSpace.param'))
#        except Exception:
#            sSpaceDict = dict()
#            
#        try:
#            wshedDict = fileManager.unpickle(os.path.join(fmdir, fmname,
#                                         'wshed.param'))
#        except Exception:
#            wshedDict = dict()
#            
#        try:
#            setupFModelDict = fileManager.unpickle(os.path.join(fmdir, fmname, 
#                                               'setupFModel.param'))
#        except Exception:
#            setupFModelDict = dict()
#        
#        try:
#            fSolDict = fileManager.unpickle(os.path.join(fmdir, fmname, 
#                                                         'fSolution.param'))
#        except Exception:
#            fSolDict = dict()
#        
#        # Check if forward model has coregistration and forward solution
#        # files present (allows manual import of both from outside Meggie).
#        transFilePath = os.path.join(fmdir, fmname, 'reconFiles', 
#                                    'reconFiles-trans.fif')
#        
#        if os.path.isfile(transFilePath):
#            isCoreg = 'yes'
#        else:
#            isCoreg = 'no'
#        
#        fsolFilePath = os.path.join(fmdir, fmname, 'reconFiles',
#                                    'reconFiles-fwd.fif')
#        
#        if os.path.isfile(fsolFilePath):
#            isFsol = 'yes'
#        else:
#            isFsol = 'no'
#        
#        mergedDict = dict([('fmname', fmname)] + sSpaceDict.items() + \
#                          wshedDict.items() + \
#                          setupFModelDict.items() + \
#                          fSolDict.items() + \
#                          [('coregistered', isCoreg)] + [('fsolution', isFsol)])
#        
#        # No need to crash on missing forward model parameters files, just don't
#        # try to add anything to the list.
#        try:
#            fmDictList = self.fmodel_dict_to_list(mergedDict)
#            return fmDictList
#        except Exception:
#            return None
#    
#
#    def fmodel_dict_to_list(self, fmdict):
#        """
#        TODO: desc
#        """
#        
#        fmList = []
#        
#        # TODO: compartModel and decimMethod need some shortening
#        fmList.append(fmdict['fmname'])
#        
#        fmList.append(fmdict['surfaceDecimMethod'])
#        
#        if fmdict['surfaceDecimMethod'] == 'traditional (default)':
#            fmList.append(fmdict['spacing'])
#        else: fmList.append('--')
#        
#        if fmdict['surfaceDecimMethod'] == 'traditional (default)':
#            fmList.append('--')
#        else: fmList.append(fmdict['surfaceDecimValue'])
#        
#        fmList.append(fmdict['surfaceName'])
#        fmList.append(fmdict['computeCorticalStats'])
#        fmList.append(fmdict['useAtlas'])
#        fmList.append(fmdict['triangFilesIco'])
#        fmList.append(fmdict['compartModel'])
#        fmList.append(fmdict['innerShift'])
#        fmList.append(fmdict['outerShift'])
#        fmList.append(fmdict['skullShift'])
#        fmList.append(fmdict['brainc'])
#        fmList.append(fmdict['skullc'])
#        fmList.append(fmdict['scalpc'])
#        fmList.append(fmdict['coregistered'])
#        fmList.append(fmdict['fsolution'])
#        
#        # If there are no forward solution parameters, add dummy ones.
#        try:
#            fmList.append(fmdict['includeMEG'])
#        except Exception:
#            fmList.append('--')
#            
#        try:
#            fmList.append(fmdict['includeEEG'])
#        except Exception:
#            fmList.append('--')
#        
#        try:
#            fmList.append(fmdict['mindist'])
#        except Exception:
#            fmList.append('--')
#
#        try:   
#            fmList.append(fmdict['ignoreref'])
#        except Exception:
#            fmList.append('--')
#
#        return fmList
#
#    def add_fmodel(self, fmlist):
#        self.layoutAboutToBeChanged.emit()
#        self.fmodelInfoList.append(fmlist)
#        self.layoutChanged.emit()
#
#
##
