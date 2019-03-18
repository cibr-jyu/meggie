import os
import logging
import shutil

from PyQt5 import QtWidgets

from meggie.ui.general.tabs.mainWindowTabSpectrumsUi import Ui_mainWindowTabSpectrums  # noqa

from meggie.ui.analysis.powerSpectrumDialogMain import PowerSpectrumDialog

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

from meggie.code_meggie.analysis.spectral import plot_power_spectrum
from meggie.code_meggie.analysis.spectral import save_data_psd
from meggie.code_meggie.analysis.spectral import group_average_psd

from meggie.ui.analysis.outputOptionsMain import OutputOptions

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabSpectrums(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabSpectrums()
        self.ui.setupUi(self)

        self.initialize_ui()


    def initialize_ui(self):

        if not self.parent.experiment:
            return

        self.ui.listWidgetSpectrums.clear()

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        # update subjects list
        for name in active_subject.spectrums:
            item = QtWidgets.QListWidgetItem(name)
            self.ui.listWidgetSpectrums.addItem(item)


    def on_listWidgetSpectrums_currentItemChanged(self, item):
        if not item:
            self.ui.textBrowserSpectrumInfo.clear()
            return

        experiment = self.parent.experiment

        spectrum_name = str(item.text())
        spectrum = experiment.active_subject.spectrums.get(spectrum_name)
        info = 'Name: ' + str(spectrum_name) + '\n'

        freqs = spectrum.freqs
        fmin, fmax = "%.1f" % freqs[0], "%.1f" % freqs[-1]
        info += 'Freqs: ' + fmin + ' - ' + fmax + ' hz\n'

        keys = spectrum.data.keys()
        if keys:
            info += 'Condition labels: ' + ', '.join([str(key) for key in keys])
            info += '\n'

        log_transformed = spectrum.log_transformed 
        info += 'Log transformed: ' + str(log_transformed) + '\n'

        self.ui.textBrowserSpectrumInfo.setText(info) 


    def on_pushButtonComputeSpectrum_clicked(self, checked=None):
        """Open the power spectrum dialog."""
        if checked is None:
            return

        if self.parent.experiment.active_subject is None:
            return

        self.spectrumDialog = PowerSpectrumDialog(self, 
            self.parent.experiment)
        self.spectrumDialog.show()

    def on_pushButtonVisualizeSpectrum_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        spectrum_item = self.ui.listWidgetSpectrums.currentItem()
        if not spectrum_item:
            return

        def output_options_handler(row_setting):
            logging.getLogger('ui_logger').info('Plotting spectrum..')
            plot_power_spectrum(self.parent.experiment, spectrum_item.text(), 
                                output=row_setting)

        handler = output_options_handler
        self.output_options_dialog = OutputOptions(self, handler=handler)
        self.output_options_dialog.show()


    def on_pushButtonDeleteSpectrum_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        spectrum_item = self.ui.listWidgetSpectrums.currentItem()
        if not spectrum_item:
            return

        message = 'Permanently remove a spectrum?'
        reply = QtWidgets.QMessageBox.question(self, 'Delete spectrum',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.parent.experiment.active_subject.remove_spectrum(
                    spectrum_item.text()
                )
            except Exception as e:
                exc_messagebox(self, e)

            self.parent.experiment.save_experiment_settings()
            self.initialize_ui()


    def on_pushButtonGroupAverage_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        if experiment.active_subject is None:
            return
        
        if self.ui.listWidgetSpectrums.currentItem() is None:
            messagebox(self, 'No spectrum selected')

        spectrum_name = self.ui.listWidgetSpectrums.currentItem().text()

        @threaded
        def group_average(*args, **kwargs):
            group_average_psd(experiment, spectrum_name)

        group_average(do_meanwhile=self.update_ui)

        experiment.save_experiment_settings()
        self.initialize_ui()

    def on_pushButtonGroupDeleteSpectrum_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return 

        if experiment.active_subject is None:
            return

        if self.ui.listWidgetSpectrums.currentItem() is None:
            messagebox(self, 'No spectrum selected')

        spectrum_name = self.ui.listWidgetSpectrums.currentItem().text()

        message = 'Permanently remove spectrum from all subjects?'
        reply = QtWidgets.QMessageBox.question(self, 'Delete spectrums',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for subject in experiment.subjects.values():
                if spectrum_name in subject.spectrums:
                    subject.remove_spectrum(
                        spectrum_name,
                    )

        logging.getLogger('ui_logger').info('Removed spectrums.')
        experiment.save_experiment_settings()
        self.initialize_ui()


    def on_pushButtonGroupSaveSpectrum_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        spectrum_item = self.ui.listWidgetSpectrums.currentItem()
        if not spectrum_item:
            return

        subjects = list(experiment.subjects.values())
        logging.getLogger('ui_logger').info('Saving spectrum for all subjects')

        def output_options_handler(row_setting):
            logging.getLogger('ui_logger').info('Saving spectrum')
            save_data_psd(experiment, subjects, row_setting, spectrum_item.text())

        handler = output_options_handler
        self.output_options_dialog = OutputOptions(self, handler=handler)
        self.output_options_dialog.show()

    def on_pushButtonSaveSpectrum_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        active_subject = experiment.active_subject
        if not active_subject:
            return

        spectrum_item = self.ui.listWidgetSpectrums.currentItem()
        if not spectrum_item:
            return

        def output_options_handler(row_setting):
            logging.getLogger('ui_logger').info('Saving spectrum')
            save_data_psd(experiment, [active_subject], row_setting, spectrum_item.text())

        handler = output_options_handler
        self.output_options_dialog = OutputOptions(self, handler=handler)
        self.output_options_dialog.show()

    def update_ui(self):
        self.parent.update_ui()
