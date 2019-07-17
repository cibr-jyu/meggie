# coding: utf-8

"""
"""

import os
import re
import json
import shutil
import logging

import meggie.utilities.fileManager as fileManager

from meggie.utilities.decorators import threaded
from meggie.utilities.validators import validate_name
from meggie.subject import Subject

from PyQt5.QtCore import QObject


class Experiment(QObject):

    """A top-level class that contains structure of an experiment,
    all the subjects within, and so forth.
    """

    def __init__(self):
        """
        """
        QObject.__init__(self)

        # set some defaults
        self._name = 'experiment'
        self._author = 'unknown author'
        self._description = 'no description'
        self._subjects = {}
        self._active_subject = None
        self._workspace = None
        self._layout = 'Infer from data'
        self._channel_groups = 'MNE'

    @property
    def workspace(self):
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        self._workspace = workspace

    @property
    def name(self):
        """
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        """
        self._name = validate_name(
            name, fieldname='name')

    @property
    def author(self):
        """
        """
        return self._author

    @author.setter
    def author(self, author):
        """
        """
        self._author = validate_name(author, minlength=0, fieldname='author')

    @property
    def description(self):
        """
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        """
        if len(description) <= 1000:

            if (re.match(
                r"^[A-Za-zäÄöÖåÅ0-9 \t\r\n\v\f\]\[!\"#$%&'()*+,./:;<=>?@\^_`{|}~-]+$",
                    description) or len(description) == 0):
                self._description = description
            else:
                raise ValueError("Use only letters and " +
                                 "numbers in your description")
        else:
            raise ValueError("Too long description")

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        self._layout = layout

    @property
    def channel_groups(self):
        return self._channel_groups

    @channel_groups.setter
    def channel_groups(self, channel_groups):
        self._channel_groups = channel_groups

    @property
    def active_subject(self):
        """
        """
        return self._active_subject

    @active_subject.setter
    def active_subject(self, subject):
        """
        """
        self._active_subject = subject

    def add_subject(self, subject):
        """
        """
        self.subjects[subject.name] = subject

    @property
    def subjects(self):
        """
        """
        return self._subjects

    def remove_subject(self, name):
        """
        Removes the subject folder and its contents under experiment tree.
        Removes the subject information from experiment properties and updates
        the experiment settings file.
        """

        if getattr(self, 'active_subject',
                   None) and self.active_subject.subject_name == name:
            self.active_subject = None

        subject = self.subjects.pop(name)

        @threaded
        def remove_data():
            try:
                shutil.rmtree(subject.path)
            except OSError:
                raise OSError(
                    'Could not remove the contents of the subject folder.')
        remove_data()

    def activate_subject(self, subject_name):
        """Activates a subject from the existing subjects
        """
        # remove raw files from memory before activating new subject.
        if self.active_subject:
            self.active_subject.release_memory()

        self.active_subject = self.subjects[subject_name]
        return self.active_subject

    def create_subject(self, subject_name, experiment,
                       raw_fname, raw_path=None):
        """
        """
        subject = Subject(experiment, subject_name, raw_fname)
        if raw_path:
            subject.ensure_folders()
            fileManager.copy_subject_raw(subject, raw_path)
        self.add_subject(subject)

    def save_experiment_settings(self):
        """
        Saves the experiment settings into a file in the root of
        the experiment directory structure.
        """
        subjects = []

        for subject in self.subjects.values():
            subject_dict = {
                'subject_name': subject.name,
                'raw_fname': subject.raw_fname,
                'ica_applied': subject.ica_applied,
                'rereferenced': subject.rereferenced,
                'epochs': [],
                'evokeds': [],
                'spectrums': [],
                'tfrs': [],
            }

            datatypes = []
            datatype_path = pkg_resources.resource_filename('meggie', 'datatypes')
            for package in os.listdir(datatype_path):
                config_path = os.path.join(datatype_path, package, 'configuration.json')
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        datatype = config['id']
                        key = config['save_key']
                        datatypes.append((key, datatype))

            for save_key, datatype in datatypes:
                for inst in getattr(subject, datatype).values():
                    datatype_dict = inst.params.deepcopy()
                    datatype_dict['name'] = inst.name

                    if save_key not in subject_dict.keys():
                        subject_dict[save_key] = []

                    subject_dict[save_key].append(datatype_dict)

            # for epoch in subject.epochs.values():
            #     try:
            #         epoch_dict = {
            #             'collection_name': epoch.collection_name,
            #             'params': epoch.params
            #         }
            #         subject_dict['epochs'].append(epoch_dict)
            #     except IOError:
            #         del subject.epochs[epoch.collection_name]
            #         message = 'Missing epochs response file. Experiment updated.'
            #         logging.getLogger('ui_logger').warning(message)

            # for evoked in subject.evokeds.values():
            #     try:
            #         evoked_dict = {
            #             'name': evoked.name,
            #             'event_names': list(evoked.mne_evokeds.keys()),
            #             'info': evoked.info,
            #         }
            #         subject_dict['evokeds'].append(evoked_dict)
            #     except IOError:
            #         del subject.evokeds[evoked.name]
            #         message = 'Missing evoked response file. Experiment updated.'
            #         logging.getLogger('ui_logger').warning(message)

            # for spectrum in subject.spectrums.values():
            #     spectrum_dict = {
            #         'name': spectrum.name,
            #         'log_transformed': spectrum.log_transformed,
            #     }
            #     subject_dict['spectrums'].append(spectrum_dict)

            # for tfr in subject.tfrs.values():
            #     tfr_dict = {
            #         'name': tfr.name,
            #         'decim': tfr.decim,
            #         'n_cycles': tfr.n_cycles,
            #         'evoked_subtracted': tfr.evoked_subtracted,
            #     }
            #     subject_dict['tfrs'].append(tfr_dict)

            subjects.append(subject_dict)

        save_dict = {
            'subjects': subjects,
            'name': self.name,
            'author': self.author,
            'description': self.description,
            'layout': self.layout,
            'channel_groups': self.channel_groups
        }

        version = ''
        try:
            import pkg_resources
            version = pkg_resources.get_distribution("meggie").version
        except BaseException:
            version = ''

        save_dict['version'] = version

        try:
            os.makedirs(os.path.join(self.workspace, self.name))
        except OSError:
            pass

        # save to file
        with open(os.path.join(self.workspace, self.name, self.name + '.exp'), 'w') as f:  # noqa
            json.dump(save_dict, f, sort_keys=True, indent=4)


class ExperimentHandler(QObject):
    """
    Class for handling the creation of a new experiment.
    """

    def __init__(self, parent):
        """
        Constructor
        Keyword arguments:
        parent        -- Parent of this object.
        """
        self.parent = parent

    def initialize_new_experiment(self, expDict):
        """
        Initializes the experiment object with the given data.

        """
        prefs = self.parent.preferencesHandler

        try:
            experiment = Experiment()
            experiment.author = expDict['author']
            experiment.name = os.path.basename(expDict['name'])
            experiment.description = expDict['description']
        except AttributeError:
            raise Exception('Cannot assign attribute to experiment.')

        experiment.workspace = prefs.working_directory

        if os.path.exists(os.path.join(experiment.workspace,
                                       experiment.name)):
            raise Exception('Experiment with same name already exists.')

        experiment.save_experiment_settings()

        prefs.previous_experiment_name = os.path.join(
            experiment.workspace, experiment.name)
        prefs.write_preferences_to_disk()

        return experiment

    def open_existing_experiment(self, prefs, path=None):
        """
        Opens an existing experiment, which is assumed to be in the working
        directory.

        Keyword arguments:

        name        -- name of the existing experiment to be opened
        """

        if path:
            if path.endswith('.exp'):
                exp_file = path
            else:
                exp_file = os.path.join(path, os.path.basename(path) + '.exp')
        else:
            if prefs.previous_experiment_name == '':
                return

            exp_file = os.path.join(
                prefs.previous_experiment_name,
                os.path.basename(prefs.previous_experiment_name) + '.exp'
            )

        if not os.path.isfile(exp_file):
            raise ValueError(
                'Trying to open experiment without settings file (.exp).')

        try:
            with open(exp_file, 'r') as f:
                data = json.load(f)
        except ValueError as exc:
            import traceback
            traceback.print_exc()

            raise ValueError('Experiment from ' + exp_file + ' could not be ' +
                             'opened. There might be a problem with ' +
                             'coherence of the experiment file.')

        prefs = self.parent.preferencesHandler
        experiment = Experiment()
        experiment.author = data['author']
        experiment.name = data['name']
        experiment.description = data['description']

        if 'layout' in data.keys():
            experiment.layout = data['layout']
        else:
            experiment.layout = 'Infer from data'

        if 'channel_groups' in data.keys():
            experiment.channel_groups = data['channel_groups']
        else:
            experiment.channel_groups = 'MNE'

        if path:
            experiment.workspace = os.path.dirname(path)
        else:
            experiment.workspace = os.path.dirname(
                prefs.previous_experiment_name)

        if len(data['subjects']) > 0:

            for subject_data in data['subjects']:

                subject_name = subject_data['subject_name']

                # backward compatibility
                raw_fname = subject_data.get('raw_fname')
                if not raw_fname:
                    raw_fname = subject_data.get('working_file_name')
                if not raw_fname:
                    raise Exception('raw_fname not set in the exp file')

                subject = Subject(experiment,
                                  subject_name,
                                  raw_fname,
                                  subject_data.get('ica_applied', False),
                                  subject_data.get('rereferenced', False)
                                  )

                for epoch_data in subject_data.get('epochs', []):
                    epochs = Epochs(epoch_data['collection_name'], subject,
                                    epoch_data['params'])
                    epochs.collection_name = epoch_data['collection_name']
                    epochs.params = epoch_data['params']
                    subject.add_epochs(epochs)

                for evoked_data in subject_data.get('evokeds', []):
                    mne_evokeds = dict([(name, None)
                                        for name in evoked_data['event_names']])
                    evoked = Evoked(evoked_data['name'], subject, mne_evokeds)
                    if 'info' in evoked_data:
                        evoked.info = evoked_data['info']
                    subject.add_evoked(evoked)

                for spectrum_data in subject_data.get('spectrums', []):
                    spectrum = Spectrum(spectrum_data['name'], subject,
                                        spectrum_data['log_transformed'], None, None, None)
                    subject.add_spectrum(spectrum)

                for tfr_data in subject_data.get('tfrs', []):
                    tfr = TFR(None, tfr_data['name'], subject,
                              tfr_data['decim'], tfr_data['n_cycles'],
                              tfr_data['evoked_subtracted'])
                    subject.add_tfr(tfr)

                experiment.add_subject(subject)

                # ensure that the folder structure exists
                # (to not crash on updates)
                subject.ensure_folders()

        prefs.previous_experiment_name = os.path.join(
            experiment.workspace, experiment.name)

        return experiment
