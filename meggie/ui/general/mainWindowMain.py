# coding: utf-8

"""
"""

import os
import sys
import warnings
import gc
import logging

import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.Qt import QApplication

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.ui.icons import mainWindowIcons_rc
from meggie.ui.general.mainWindowUi import Ui_MainWindow
from meggie.ui.general.createExperimentDialogMain import CreateExperimentDialog
from meggie.ui.general.addSubjectDialogMain import AddSubjectDialog
from meggie.ui.general.layoutDialogMain import LayoutDialog
from meggie.ui.general.infoDialogMain import InfoDialog
from meggie.ui.preprocessing.eogParametersDialogMain import EogParametersDialog
from meggie.ui.preprocessing.ecgParametersDialogMain import EcgParametersDialog
from meggie.ui.preprocessing.eegParametersDialogMain import EegParametersDialog
from meggie.ui.preprocessing.badChannelsDialogMain import BadChannelsDialog
from meggie.ui.general.preferencesDialogMain import PreferencesDialog
from meggie.ui.preprocessing.addECGProjectionsMain import AddECGProjections
from meggie.ui.preprocessing.addEOGProjectionsMain import AddEOGProjections
from meggie.ui.preprocessing.filterDialogMain import FilterDialog
from meggie.ui.preprocessing.icaDialogMain import ICADialog
from meggie.ui.preprocessing.resamplingDialogMain import ResamplingDialog
from meggie.ui.preprocessing.rereferencingDialogMain import RereferencingDialog
from meggie.ui.general.aboutDialogMain import AboutDialog
from meggie.ui.general.experimentInfoDialogMain import ExperimentInfoDialog
from meggie.ui.general.logDialogMain import LogDialog
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.decorators import threaded

from meggie.ui.general.tabs.mainWindowTabSourceAnalysisMain import MainWindowTabSourceAnalysis
from meggie.ui.general.tabs.mainWindowTabSpectrumsMain import MainWindowTabSpectrums
from meggie.ui.general.tabs.mainWindowTabInducedMain import MainWindowTabInduced
from meggie.ui.general.tabs.mainWindowTabEpochsMain import MainWindowTabEpochs
from meggie.ui.general.tabs.mainWindowTabEvokedMain import MainWindowTabEvoked

from meggie.code_meggie.general.experiment import ExperimentHandler
from meggie.code_meggie.general.experiment import Experiment
from meggie.code_meggie.general.preferences import PreferencesHandler
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.preprocessing.projections import plot_projs_topomap


class MainWindow(QtWidgets.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """

    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.experiment = None

        self.setup_loggers()        

        # Direct output to console
        if 'debug' not in sys.argv:
            self.directOutput()
            self.ui.actionDirectToConsole.triggered.connect(self.directOutput)
        # For storing and handling program wide prefences.
        self.preferencesHandler = PreferencesHandler()
        self.preferencesHandler.set_env_variables()

        # For handling initialization and switching of experiments.
        self.experimentHandler = ExperimentHandler(self)

        # Create the tab contents
        self.mainWindowTabSpectrums = MainWindowTabSpectrums(self)
        self.mainWindowTabEpochs = MainWindowTabEpochs(self)
        self.mainWindowTabEvoked = MainWindowTabEvoked(self)
        self.mainWindowTabSourceAnalysis = MainWindowTabSourceAnalysis(self)
        self.mainWindowTabInduced = MainWindowTabInduced(self)

        # Creates a label on status bar to show current working file message.
        self.statusLabel = QtWidgets.QLabel()
        self.ui.statusbar.addWidget(self.statusLabel)

        # If the user has chosen to open the previous experiment automatically.
        if self.preferencesHandler.auto_load_last_open_experiment:
            exp = None
            
            try:
                exp = self.experimentHandler.open_existing_experiment(
                    self.preferencesHandler)
            except Exception as e:
                exc_messagebox(self, e)
            
            if exp:
                self.experiment = exp
                self.initialize_ui()
            else:
                self.preferencesHandler.previous_experiment_name = ''
                self.preferencesHandler.write_preferences_to_disk()


        # Set bads not selectable
        self.ui.listWidgetBads.setSelectionMode(QAbstractItemView.NoSelection)


    def get_epochs(self, epoch_name):
        experiment = self.experiment
        if not experiment:
            return
        
        active_subject = experiment.active_subject
        if not active_subject:
            return

        return active_subject.epochs.get(epoch_name)


    def on_actionQuit_triggered(self, checked=None):
        """Closes the program, possibly after a confirmation by the user."""
        if checked is None:
            return

        if self.preferencesHandler.confirm_quit:
            reply = QtWidgets.QMessageBox.question(self, 'Close Meggie',
                'Are you sure you want to quit Meggie?', 
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def on_actionCreate_experiment_triggered(self, checked=None):
        """Create a new CreateExperimentDialog and show it"""
        if checked is None:
            return

        if self.preferencesHandler.working_directory != '':
            self.dialog = CreateExperimentDialog(self)
            self.dialog.experimentCreated.connect(self.setExperiment)
            self.dialog.show()
        else:
            self.check_workspace()
            if self.preferencesHandler.working_directory != '':
                self.dialog = CreateExperimentDialog(self)
                self.dialog.experimentCreated.connect(self.setExperiment)
                self.dialog.show()

    def on_actionOpen_experiment_triggered(self, checked=None):
        """ Open an existing _experiment. """

        if checked is None:
            return

        if self.experiment is not None:
            directory = self.experiment.workspace
        else:
            directory = ''

        path = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(self, 
                "Select experiment directory", directory)))

        if path == '':
            return
        
        logging.getLogger('ui_logger').info('Opening experiment ' + path)

        try:
            exp = self.experimentHandler.open_existing_experiment(
                self.preferencesHandler, path=path)
            self.experiment = exp
            self.initialize_ui()
        except Exception as e:
            exc_messagebox(self, e)

        # Saves at least the previous experiment name
        self.preferencesHandler.write_preferences_to_disk()

    def on_pushButtonAddSubjects_clicked(self, checked=None):
        """Open subject dialog."""

        if checked is None:
            return

        # Check that we have an experiment that we can add a subject to
        if self.experiment is None:
            msg = ('No active experiment to add a subject to. Load an '
                   'experiment or make a new one, then try again.')
            messagebox(self, msg)
            return

        self.subject_dialog = AddSubjectDialog(self)
        self.subject_dialog.exec_()

    def on_pushButtonRemoveSubject_clicked(self, checked=None):
        """Delete the selected subject item and the files related to it."""
        if checked is None:
            return

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()

        if selIndexes == []:
            return

        message = 'Permanently remove the selected subjects and the related files?'
        reply = QtWidgets.QMessageBox.question(self, 'Delete selected subjects',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        failures = []
        if reply == QtWidgets.QMessageBox.Yes:
            for index in selIndexes:
                subject_name = index.data()
        
                try:
                    self.experiment.remove_subject(subject_name, self)
                except Exception:
                    failures.append(subject_name)

        if failures:
            msg = ''.join(['Could not remove the contents of the subject ',
                           'folder for following subjects: ',
                           '\n'.join(failures)])
            messagebox(self, msg)

        self.experiment.save_experiment_settings()
        self.initialize_ui()

    def closeEvent(self, event):
        """Redefine window close event to allow confirming on quit."""

        if self.preferencesHandler.confirm_quit:
            reply = QtWidgets.QMessageBox.question(self, 'Close Meggie',
                                               'Are you sure you want to '
                                               'quit?', QtWidgets.QMessageBox.Yes | 
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def on_actionSet_workspace_triggered(self, checked=None):
        """
        Open the preferences dialog the for specific purpose of initial setting
        of workspace.
        """
        if checked is None:
            return

        self.check_workspace()

    def on_actionShow_log_triggered(self, checked=None):
        if checked is None:
            return

        if self.experiment is None:
            message = 'Please open an experiment first.'
            messagebox(self, message)
            return

        self.log_dialog = LogDialog(self)
        self.log_dialog.show()

    def on_actionPreferences_triggered(self, checked=None):
        """Open the preferences-dialog."""
        if checked is None:
            return

        self.dialogPreferences = PreferencesDialog(self)
        self.dialogPreferences.show()

    def on_actionAbout_triggered(self, checked=None):
        """Open the About-dialog."""
        if checked is None:
            return

        self.dialogAbout = AboutDialog()
        self.dialogAbout.show()

    def on_actionShowExperimentInfo_triggered(self, checked=None):
        """Open the experiment info dialog """
        if checked is None:
            return
        if self.experiment is None:
            messagebox(self, 'You do not currently have an experiment activated.')  # noqa
            return

        self.expInfoDialog = ExperimentInfoDialog(self)
        self.expInfoDialog.show()

    def on_actionHide_Show_subject_list_and_info_triggered(self, checked=None):
        if checked is None:
            return
        if self.ui.dockWidgetSubjects.isVisible():
            self.ui.dockWidgetSubjects.hide()
        else:
            self.ui.dockWidgetSubjects.show()

    def on_pushButtonLayout_clicked(self, checked=None):
        if checked is None:
            return

        if not self.experiment:
            return
        
        self.layoutDialog = LayoutDialog(self)
        self.layoutDialog.show()


    class RawBadsPlot(object):
        def __init__(self, parent):
            self.parent = parent
            
            if parent.ui.checkBoxShowEvents.isChecked():
                events = parent.experiment.active_subject.get_events()
            else:
                events = None
            try:
                raw = parent.experiment.active_subject.get_working_file()  # noqa
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

        if not self.experiment or self.experiment.active_subject is None:
            return

        # Create a plot where bad channels are not set by clicking them
        self.plot = MainWindow.RawBadsPlot(self)
        
    def on_pushButtonCustomChannels_clicked(self, checked=None):
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return
        
        self.badChannelsDialog = BadChannelsDialog(self)
        self.badChannelsDialog.show()
        
    def on_pushButtonPlotProjections_clicked(self, checked=None):
        """Plots added projections as topomaps."""
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return

        raw = self.experiment.active_subject.get_working_file()
        if not raw.info['projs']:
            messagebox(self, "No added projections.")
            return
        
        try:
            plot_projs_topomap(self.experiment, raw)
        except Exception as e:
            exc_messagebox(self, e)
       
    def on_pushButtonEOG_clicked(self, checked=None):
        """Open the dialog for calculating the EOG PCA."""
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return

        self.eogDialog = EogParametersDialog(self)
        self.eogDialog.show()

    def on_pushButtonECG_clicked(self, checked=None):
        """Open the dialog for calculating the ECG PCA."""
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return

        self.ecgDialog = EcgParametersDialog(self)
        self.ecgDialog.show()

    def on_pushButtonApplyEOG_clicked(self, checked=None):
        """Open the dialog for applying the EOG-projections to the data."""
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return

        info = self.experiment.active_subject.get_working_file().info
        self.addEogProjs = AddEOGProjections(self, info['projs'])
        self.addEogProjs.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.addEogProjs.show()
        
    def on_pushButtonApplyECG_clicked(self, checked=None):
        """Open the dialog for applying the ECG-projections to the data."""
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return
        
        info = self.experiment.active_subject.get_working_file().info
        self.addEcgProjs = AddECGProjections(self, info['projs'])
        self.addEcgProjs.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.addEcgProjs.show()
        
    def on_pushButtonRemoveProj_clicked(self, checked=None):
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return
        
        if self.ui.listWidgetProjs.currentItem() is None:
            message = 'Select projection to remove.'
            messagebox(self, message)
            return
        
        selected_items = self.ui.listWidgetProjs.selectedItems()
        raw = self.experiment.active_subject.get_working_file()
        str_projs = [str(proj) for proj in raw.info['projs']]
        
        for item in selected_items:
            proj_name = item.text()
            if proj_name in str_projs:
                index = str_projs.index(proj_name)
                str_projs.pop(index)
                raw.info['projs'].pop(index)
                row = self.ui.listWidgetProjs.row(item)
                self.ui.listWidgetProjs.takeItem(row)

        directory = self.experiment.active_subject.subject_path
        subject_name = self.experiment.active_subject.working_file_name
        fname = os.path.join(directory, subject_name)        
        fileManager.save_raw(self.experiment, raw, fname)
        self.initialize_ui()


    def on_pushButtonICA_clicked(self, checked=None):
        """
        Show the dialog for ICA preprocessing.
        """
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return

        self.icaDialog = ICADialog(self)
        self.icaDialog.show()

    def on_pushButtonFilter_clicked(self, checked=None):
        """
        Show the dialog for filtering.
        """
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return

        self.filterDialog = FilterDialog(self)
        self.filterDialog.show()

    def on_pushButtonResampling_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        if not self.experiment or self.experiment.active_subject is None:
            return

        self.resamplingDialog = ResamplingDialog(self)
        self.resamplingDialog.show()

    def on_pushButtonRereferencing_clicked(self, checked=None):
        """
        """
        if checked is None:
            return
        if not self.experiment or self.experiment.active_subject is None:
            return
        self.rereferencingDialog = RereferencingDialog(self)
        self.rereferencingDialog.show()

    def on_pushButtonActivateSubject_clicked(self, checked=None):
        """
        Activates a subject.
        """
        if checked is None:
            return

        if self.ui.listWidgetSubjects.selectedIndexes() == []:
            return

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()
        
        if len(selIndexes) > 1:
            return
        
        subject_name = selIndexes[0].data()

        if self.experiment.active_subject:
            if subject_name == self.experiment.active_subject.subject_name:
                return

        previous_subject = self.experiment.active_subject
        try:
            @threaded
            def activate(subject_name):
                self.experiment.activate_subject(subject_name)
            activate(subject_name, do_meanwhile=self.update_ui)

        except Exception as e:
            self.experiment.active_subject = None
            exc_messagebox(self, "Couldn't activate the subject.")
            if previous_subject:
                message = "Couldn't activate the subject, resuming to previous one."
                logging.getLogger('ui_logger').info(message)
                self.experiment.activate_subject(previous_subject.subject_name)

        self.initialize_ui()

    #####################

    def update_ui(self):
        """
        Method for repainting the ui.
        Used for keeping the ui responsive when threading.
        """
        QApplication.processEvents()

    @QtCore.pyqtSlot(Experiment)
    def setExperiment(self, newExperiment):
        """Temporary setter for experiment."""
        self.experiment = newExperiment
        gc.collect()
        
        self.initialize_ui()


    def initialize_ui(self):
        """
        Method for setting up the GUI. Called whenever a subject is activated,
        either via creation of a new subject or change of an active subject.
        Also called when anything that can affect UI state has been run.
        Checks the existence of a ton of files and sets the GUI fields to
        reflect the state of the experiment and subject according to them.
        """

        self.update_tabs()

        self.setup_loggers()

        self.ui.listWidgetSubjects.clear()
        self.ui.textBrowserEvents.clear()
        self.ui.labelDateValue.clear()
        self.ui.labelLengthValue.clear()
        self.ui.labelEEGValue.clear()
        self.ui.labelGradMEGValue.clear()
        self.ui.labelHighValue.clear()
        self.ui.labelLowValue.clear()
        self.ui.labelMagMEGValue.clear()
        self.ui.labelSamplesValue.clear()
        self.ui.labelSubjectValue.clear()
        self.ui.listWidgetProjs.clear()
        self.ui.listWidgetBads.clear()
        self.ui.checkBoxMaxFilterApplied.setChecked(False)
        self.ui.checkBoxECGApplied.setChecked(False)
        self.ui.checkBoxEOGApplied.setChecked(False)
        self.ui.checkBoxICAApplied.setChecked(False)
        self.ui.checkBoxRereferenced.setChecked(False)
        self.ui.pushButtonApplyECG.setEnabled(False)
        self.ui.pushButtonApplyEOG.setEnabled(False)

        self.setWindowTitle('Meggie - ' + self.experiment.experiment_name)

        self.populate_subject_list()

        active_subject = self.experiment.active_subject
        
        if active_subject is None:
            self.statusLabel.setText('Add or activate subjects before '
                                     'continuing.')
            return        
        
        raw = active_subject.get_working_file()
        
        name = active_subject.working_file_name
        status = "Current working file: " + name
        
        self.statusLabel.setText(status)

        # Check whether ECG projections are calculated
        if active_subject.check_ecg_projs():
            self.ui.pushButtonApplyECG.setEnabled(True)
        
        # Check whether EOG (and old EEG) projections are calculated
        if active_subject.check_eog_projs() or active_subject.check_eeg_projs():
            self.ui.pushButtonApplyEOG.setEnabled(True)
        
        # Check whether ECG projections are applied
        if active_subject.check_ecg_applied():
            self.ui.checkBoxECGApplied.setChecked(True)
        
        # Check whether EOG (and old EEG) projections are applied
        if active_subject.check_eog_applied() or active_subject.check_eeg_applied():
            self.ui.checkBoxEOGApplied.setChecked(True)

        # Check whether sss/tsss method is applied.
        if active_subject.check_sss_applied():
            self.ui.checkBoxMaxFilterApplied.setChecked(True)
             
        if active_subject.ica_applied:
            self.ui.checkBoxICAApplied.setChecked(True)
        if active_subject.rereferenced:
            self.ui.checkBoxRereferenced.setChecked(True)

        # This updates the 'Subject info' section below the subject list.
        try:
            InfoDialog(raw, self.ui, False)
            self.populate_raw_tab_event_list()
        except Exception as err:
            exc_messagebox(self, err)
            return

        projs = raw.info['projs']
        for proj in projs:
            self.ui.listWidgetProjs.addItem(str(proj))

        bads = raw.info['bads']
        for bad in bads:
            self.ui.listWidgetBads.addItem(bad)

    def populate_subject_list(self):
        """ """
        active_subject_name = None
        if self.experiment and self.experiment.active_subject:
            active_subject_name = self.experiment.active_subject.subject_name

        for subject_name in sorted(self.experiment.subjects.keys()):
            item = QtWidgets.QListWidgetItem()
            item.setText(subject_name)
            if subject_name == active_subject_name:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            self.ui.listWidgetSubjects.addItem(item)

        
    def populate_raw_tab_event_list(self):
        """
        Fill the raw tab event list with info about event IDs and
        amount of events with those IDs.
        """
        events = self.experiment.active_subject.create_event_set()

        if events is None:
            return

        events_string = ''
        for key, value in events.items():
            events_string += 'Trigger %s, %s events\n' % (str(key), str(value))

        self.ui.textBrowserEvents.setText(events_string)

    def update_tabs(self):
        """Method for initializing the tabs."""

        current_tab = self.ui.tabWidget.currentIndex()                                  
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)

        self.ui.tabWidget.insertTab(1, self.ui.tabPreprocessing, "Preprocessing")
        self.ui.tabWidget.insertTab(2, self.mainWindowTabSpectrums, "Spectrums")
        self.ui.tabWidget.insertTab(3, self.mainWindowTabEpochs, "Epoching")
        self.ui.tabWidget.insertTab(4, self.mainWindowTabEvoked, "Evoked responses")
        self.ui.tabWidget.insertTab(5, self.mainWindowTabInduced, "Induced responses")
        self.ui.tabWidget.insertTab(6, self.mainWindowTabSourceAnalysis, "Source Analysis")

        self.ui.tabWidget.setCurrentIndex(current_tab)

        self.mainWindowTabSourceAnalysis.update_tabs()
        self.mainWindowTabSourceAnalysis.initialize_ui()

        self.mainWindowTabSpectrums.initialize_ui()
        self.mainWindowTabEpochs.initialize_ui()
        self.mainWindowTabEvoked.initialize_ui()
        self.mainWindowTabInduced.initialize_ui()
        
    def directOutput(self):
        """
        Method for directing stdout to the console and back.
        """
        if self.ui.actionDirectToConsole.isChecked():
            stdout_stream = EmittingStream(textWritten=self.normalOutputWritten)
            stdout_stream.orig_stream = sys.__stdout__
            stderr_stream = EmittingStream(textWritten=self.errorOutputWritten)
            stderr_stream.orig_stream = sys.__stderr__

            sys.stdout = stdout_stream
            sys.stderr = stderr_stream
        else:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def check_workspace(self):
        """
        Open the preferences dialog, in this case for choosing the workspace.
        """
        preferencesDialog = PreferencesDialog(self)
        preferencesDialog.exec_()

    def __del__(self):
        """
        Restores stdout at the end.
        """
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
 
    def normalOutputWritten(self, text):
        """
        Appends text to 'console' at the bottom of the dialog.
        Used for redirecting stdout.
        Parameters:
        text - Text to write to the console.
        """
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()
 
    def errorOutputWritten(self, text):
        """
        Appends text to 'console' at the bottom of the dialog.
        Used for redirecting stderr.
        Parameters:
        text - Text to write to the console.
        """
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()

    def setup_loggers(self):

        # hide warnings-module warnings,
        # most of these are still contained
        # in mne-level logging
        warnings.simplefilter('ignore')

        logging.getLogger().setLevel(logging.DEBUG)

        # logger for mne wrapper functions
        mne_wrapper_logger = logging.getLogger('mne_wrapper_logger')
        formatter = logging.Formatter('MNE call: %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        mne_wrapper_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.experiment_name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            mne_wrapper_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('INFO')
        mne_wrapper_logger.addHandler(stream_handler)

        # logger for ui output
        ui_logger = logging.getLogger('ui_logger')
        formatter = logging.Formatter('Meggie: %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        ui_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.experiment_name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            ui_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('INFO')
        ui_logger.addHandler(stream_handler)

        # logger for real mne
        mne_logger = logging.getLogger('mne')
        formatter = logging.Formatter('MNE: %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        mne_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.experiment_name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            mne_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('ERROR')
        mne_logger.addHandler(stream_handler)

        # TODO: trait logger ..


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

    def fileno(self):
        return self.orig_stream.fileno()



def main():

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)

    window.showMaximized()
    
    sys.exit(app.exec_())
