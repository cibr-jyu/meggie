import os
import logging
import shutil

import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.ui.general.tabs.mainWindowTabEvokedUi import Ui_mainWindowTabEvoked  # noqa

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

from meggie.ui.widgets.epochWidgetMain import EpochWidget
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget

from meggie.code_meggie.structures.evoked import Evoked

from meggie.code_meggie.analysis.epoching import draw_evoked_potentials
from meggie.code_meggie.analysis.epoching import group_average

from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.utils.units import get_scaling

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabEvoked(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabEvoked()
        self.ui.setupUi(self)

        self.epochList = EpochWidget(self, 
            epoch_getter=self.parent.get_epochs,
            parameter_setter=None)
        self.epochList.setParent(self.ui.groupBoxEpochs)

        mode = QtWidgets.QAbstractItemView.MultiSelection
        self.epochList.setSelectionMode(mode)

        # self.ui.listWidgetEvoked.setMinimumWidth(346)
        # self.ui.listWidgetEvoked.setMaximumWidth(346)

        self.evokeds_batching_widget = BatchingWidget(
            self.parent.experiment,
            self, self.ui.widgetBatchContainer,
            self.ui.pushButtonCreateEvoked,
            self.ui.pushButtonCreateEvokedBatch,
            self.evoked_selection_changed,
            self.collect_evoked_parameter_values,
        )

        self.initialize_ui()

    def initialize_ui(self):

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        self.epochList.clearItems()
        epochs_items = active_subject.epochs
        if epochs_items is not None:
            for name in sorted(epochs_items.keys()):
                self.epochList.add_item(name)

        evokeds_items = active_subject.evokeds
        self.ui.listWidgetEvoked.clear()
        if evokeds_items is not None:
            for name in sorted(evokeds_items.keys()):
                self.ui.listWidgetEvoked.addItem(name)

        # Select the first item on epoch list
        if self.epochList.ui.listWidgetEpochs.count() > 1:
            self.epochList.ui.listWidgetEpochs.setCurrentRow(0)

        # Update the batching widget ui
        if self.parent.experiment:
            self.evokeds_batching_widget.update(self.parent.experiment, False)

    def update_ui(self):
        self.parent.update_ui()


    def on_pushButtonCreateEvoked_clicked(self, checked=None):
        """
        Create averaged epoch collection (evoked dataset).
        Plot the evoked data as a topology.
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        selected_items = self.epochList.ui.listWidgetEpochs.selectedItems()
        collection_names = [str(item.text()) for item in selected_items]

        # If no collections are selected, show a message to to the user and return.
        if len(collection_names) == 0:
            messagebox(self, 'Please select an epoch collection to average.')
            return

        subject = experiment.active_subject

        try:
            self.calculate_evokeds(subject, collection_names)
        except Exception as e:
            exc_messagebox(self, e)

        self.evokeds_batching_widget.cleanup(self)
        self.initialize_ui()



    def on_pushButtonCreateEvokedBatch_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        subject_names = self.evokeds_batching_widget.selected_subjects

        recently_active_subject_name = experiment.active_subject.subject_name

        for subject_name, collection_names in self.evokeds_batching_widget.data.items():
            if subject_name in subject_names:
                try:
                    subject = experiment.activate_subject(subject_name)
                    self.calculate_evokeds(subject, collection_names)
                except Exception as e:
                    failed_subjects = self.evokeds_batching_widget.failed_subjects
                    failed_subjects.append((subject, str(e)))
                    logging.getLogger('ui_logger').exception(str(e))

        experiment.activate_subject(recently_active_subject_name)
        experiment.save_experiment_settings()
        self.evokeds_batching_widget.cleanup(self)
        self.initialize_ui()


    def on_pushButtonGroupSaveEvoked_clicked(self, checked=None):
        if checked is None:
            return

        if not self.parent.experiment:
            return

        if not self.parent.experiment.active_subject:
            return

        subjects = self.parent.experiment.subjects
        self.save_evoked_data(subjects)

    def on_pushButtonSaveEvoked_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment:
            return

        if not experiment.active_subject:
            return

        subjects = dict([
            (experiment.active_subject.subject_name,
             experiment.active_subject),
        ])

        self.save_evoked_data(subjects)


    def on_pushButtonEvokedTopomaps_clicked(self, checked=None):
        if checked is None:
            return

   
        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return

        evoked_name = str(item.text())
        evoked = experiment.active_subject.evokeds[evoked_name]
        mne_evokeds = evoked.mne_evokeds

        logging.getLogger('ui_logger').info("Plotting evoked topomaps.")

        try:
            number_of_timepoints = 20
            for idx in range(len(list(mne_evokeds.keys()))):
                evoked = list(mne_evokeds.values())[idx]
                evoked_name = list(mne_evokeds.keys())[idx]
                for ch_type in ['mag', 'grad', 'eeg']:
                    n_eeg_channels = len(list(mne.pick_types(evoked.info, eeg=True)))
                    n_mag_channels = len(list(mne.pick_types(evoked.info, meg='mag')))
                    n_grad_channels = len(list(mne.pick_types(evoked.info, meg='grad')))

                    # if mixed data, plot only mag and grad
                    if ch_type == 'eeg' and (n_eeg_channels == 0 or
                                             n_mag_channels > 0 or
                                             n_grad_channels > 0):
                        continue
                    if ch_type == 'grad' and n_grad_channels == 0:
                        continue
                    if ch_type == 'mag' and n_mag_channels == 0:
                        continue

                    times = np.linspace(0,
                                        evoked.times[-1],
                                        number_of_timepoints+1)[:-1]

                    fig, axes = plt.subplots(2, int(number_of_timepoints/2))
                    axes = axes.reshape(-1)

                    title = evoked_name + ' (' + ch_type + ')'
                    fig.suptitle(title)

                    layout = experiment.layout
                    layout = fileManager.read_layout(layout)

                    evoked.plot_topomap(
                        times=times, ch_type=ch_type,
                        axes=axes, show=False, colorbar=False,
                        layout=layout)
            plt.show()

        except Exception as e:
            exc_messagebox(self, e)


    def on_pushButtonVisualizeEvokedDataset_clicked(self, checked=None):
        """Plot the evoked data as a topology."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return

        evoked_name = str(item.text())
        evoked = experiment.active_subject.evokeds[evoked_name]
        mne_evokeds = evoked.mne_evokeds

        message = 'Visualizing evoked collection %s...\n' % evoked_name
        logging.getLogger('ui_logger').info(message)

        try:
            draw_evoked_potentials(
                experiment,
                list(mne_evokeds.values()),
                title=evoked_name)
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonGroupAverageEvoked_clicked(self, checked=None):
        """
        Plots topology view of evoked response group averages. Saves the
        results as ascii to ``output`` folder. Uses event names for determining
        which responses to average across subjects.
        """
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return

        evoked_name = str(item.text())

        try:
            evokeds, group_epoch_info = group_average(
                experiment, evoked_name, update_ui=self.update_ui)

        except Exception as e:
            exc_messagebox(self, e)
            return

        self.save_evoked(experiment.active_subject, evokeds, 
                         'group_' + evoked_name, 
                         group_epoch_info=group_epoch_info)

        self.initialize_ui()


    def on_pushButtonDeleteEvoked_clicked(self, checked=None):
        """Delete the selected evoked."""
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        if self.ui.listWidgetEvoked.count() == 0:
            return

        elif self.ui.listWidgetEvoked.currentItem() is None:
            messagebox(self, 'No evokeds selected.')
            return

        item_str = self.ui.listWidgetEvoked.currentItem().text()

        message = 'Permanently remove evokeds?'
        reply = QtWidgets.QMessageBox.question(self, 'delete evokeds',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                experiment.active_subject.remove_evoked(
                    item_str,
                )
            except Exception as e:
                exc_messagebox(self, e)

            item = self.ui.listWidgetEvoked.currentItem()
            row = self.ui.listWidgetEvoked.row(item)
            self.ui.listWidgetEvoked.takeItem(row)
            experiment.save_experiment_settings()
            self.initialize_ui()


    def on_pushButtonGroupDeleteEvoked_clicked(self, checked=None):
        if checked is None:
            return

        experiment = self.parent.experiment
        if not experiment or experiment.active_subject is None:
            return

        if self.ui.listWidgetEvoked.currentItem() is None:
            messagebox(self, 'No evokeds selected')
            return

        collection_name = self.ui.listWidgetEvoked.currentItem().text()

        message = 'Permanently remove evokeds from all subjects?'
        reply = QtWidgets.QMessageBox.question(self, 'delete evokeds',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for subject in experiment.subjects.values():
                if collection_name in subject.evokeds:
                    subject.remove_evoked(collection_name)

        if collection_name not in experiment.active_subject.evokeds:
            self.ui.listWidgetEvoked.takeItem(
                self.ui.listWidgetEvoked.currentRow())

        experiment.save_experiment_settings()
        self.initialize_ui()

    def evoked_selection_changed(self, subject_name, data_dict):
        epoch_widget = self.epochList.ui.listWidgetEpochs

        epoch_widget.clear()
        epochs = self.parent.experiment.subjects[subject_name].epochs
        for name in sorted(epochs.keys()):
            item = QtWidgets.QListWidgetItem()
            item.setText(name)
            epoch_widget.addItem(item)
            if name in data_dict:
                item.setSelected(True)


    def on_listWidgetEvoked_currentItemChanged(self, item):
        if not item:
            self.ui.textBrowserEvokedInfo.clear()
            return
  
        experiment = self.parent.experiment

        evoked_name = str(item.text())
        evoked = experiment.active_subject.evokeds.get(evoked_name)
        info = 'Subjects:\n'

        if 'subjects' not in evoked.info:
            self.ui.textBrowserEvokedInfo.clear()
            return

        for subject_name in evoked.info['subjects']:
            info += subject_name + '\n'

        info += '\nEpoch collection info:\n'

        for collection_name, events in evoked.info['epoch_collections'].items():
            info += collection_name
            for key, value in events.items():
                info += ' [' + key + ', ' + str(value) + '] '
            info += '\n\n'

        self.ui.textBrowserEvokedInfo.setText(info)


    def collect_evoked_parameter_values(self):
        collection_names = [str(item.text()) for item
                in self.epochList.ui.listWidgetEpochs.selectedItems()]
        return collection_names


    def calculate_evokeds(self, subject, collection_names):

        # check that lengths are same
        time_arrays = []
        for name in collection_names:
            collection = subject.epochs.get(name)
            if collection:
                time_arrays.append(collection.raw.times)

        for i, i_times in enumerate(time_arrays):
            for j, j_times in enumerate(time_arrays):
                if i != j:
                    try:
                        np.testing.assert_array_almost_equal(i_times, j_times)
                    except AssertionError:
                        raise Exception('Epochs collections of different time'
                                        'scales are not allowed')

        evokeds = {}
        for name in collection_names:



            try:
                collection = subject.epochs[name]
            except KeyError:
                raise KeyError('No epoch collection called ' + str(name))

            epoch = collection.raw

            @threaded
            def average():
                return epoch.average()

            evoked = average(do_meanwhile=self.update_ui)

            evoked.comment = name
            evokeds[name] = evoked

        evoked_name = (
            '-'.join(collection_names) +
            '_evoked.fif'
        )

        self.save_evoked(subject, evokeds, evoked_name)


    def save_evoked(self, subject, evokeds, evoked_name, group_epoch_info={}):
        # Save evoked into evoked (average) directory with name evoked_name
        saveFolder = subject.evokeds_directory
        if not os.path.exists(saveFolder):
            try:
                os.mkdir(saveFolder)
            except IOError:
                message = ('Writing to selected folder is not allowed. You can'
                           ' still process the evoked file (visualize etc.).')
                raise IOError(message)

        try:
            message = 'Writing evoked data as ' + evoked_name + ' ...'
            logging.getLogger('ui_logger').info(message)

            mne.write_evokeds(os.path.join(saveFolder, evoked_name), list(evokeds.values()))
        except IOError:
            message = ('Writing to selected folder is not allowed. You can '
                       'still process the evoked file (visualize etc.).')
            raise IOError(message)

        new_evoked = Evoked(evoked_name, subject, evokeds)


        epoch_info = {}
        subject_names = []

        if not group_epoch_info:
            for key in evokeds:
                epoch = getattr(subject.epochs.get(key, object()), 'raw', None)
                events = epoch.event_id
                epoch_info[key] = dict([(name, str(len(epoch[name])) + ' events')
                                        for name in events])
            subject_names = [subject.subject_name]
        else:
            for subject_name, info in group_epoch_info.items():
                epoch_info[subject_name] = info['epoch_collections']
                subject_names = ['group evoked']

        new_evoked.info['subjects'] = subject_names
        new_evoked.info['epoch_collections'] = epoch_info
        subject.add_evoked(new_evoked)
        self.parent.experiment.save_experiment_settings()

    def save_evoked_data(self, subjects):
        try:
            evoked_name = str(self.ui.listWidgetEvoked.currentItem().text())
        except AttributeError:
            messagebox(self, "Please select evoked data from the list")
            return

        path = fileManager.create_timestamped_folder(
            self.parent.experiment)

        for sub_name, subject in subjects.items():
            names = []
            evokeds = []
            meggie_evoked = subject.evokeds.get(evoked_name)
            if meggie_evoked:
                for name, evoked in meggie_evoked.mne_evokeds.items():
                    if evoked:
                        evokeds.append(evoked)
                        names.append(name)
            if evokeds:
                cleaned_evoked_name = evoked_name.split('.')[0]
                filename = cleaned_evoked_name + '_' + sub_name + '.csv'  # noqa
                fileManager.group_save_evokeds(os.path.join(path, filename),
                                               evokeds, names)

