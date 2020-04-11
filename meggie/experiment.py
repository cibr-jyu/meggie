# coding: utf-8

"""
"""

import os
import re
import json
import importlib
import shutil
import logging
import pkg_resources
import copy

import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.dynamic import find_all_sources

from meggie.utilities.decorators import threaded
from meggie.utilities.validators import validate_name
from meggie.subject import Subject

from PyQt5.QtCore import QObject


class Experiment(QObject):

    """A top-level class that contains structure of an experiment,
    all the subjects within, and so forth.
    """

    def __init__(self, name, author):
        """
        """
        QObject.__init__(self)

        self._name = name
        self._author = author
        self._subjects = {}
        self._active_subject = None
        self._workspace = None

        self._layout = ''
        self._channel_groups = {
            'eeg': {},
            'meg': dict([(sel, mne.read_selection(sel)) for sel in 
                               mne.selection._SELECTIONS])
        }



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
                   None) and self.active_subject.name == name:
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

        # test validity
        self.active_subject.get_raw(preload=False)

        return self.active_subject

    def create_subject(self, subject_name, raw_fname, raw_path):
        """
        """
        subject = Subject(self, subject_name, raw_fname)
        subject.ensure_folders()

        filemanager.copy_subject_raw(subject, raw_path)
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
            for source in find_all_sources():
                datatype_path = pkg_resources.resource_filename(
                    source, 'datatypes')
                if not os.path.exists(datatype_path):
                    continue
                for package in os.listdir(datatype_path):
                    config_path = os.path.join(
                        datatype_path, package, 'configuration.json')
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as f:
                            config = json.load(f)
                            datatype = config['id']
                            key = config['save_key']
                            datatypes.append((key, datatype))

            for save_key, datatype in datatypes:
                for inst in getattr(subject, datatype).values():
                    datatype_dict = {
                        'name': inst.name,
                        'params': inst.params
                    }

                    if save_key not in subject_dict.keys():
                        subject_dict[save_key] = []

                    subject_dict[save_key].append(datatype_dict)

            subjects.append(subject_dict)

        save_dict = {
            'subjects': subjects,
            'name': self.name,
            'author': self.author,
            'layout': self.layout,
            'channel_groups': self.channel_groups
        }

        try:
            version = pkg_resources.get_distribution("meggie").version
        except BaseException:
            version = ''

        save_dict['version'] = version

        try:
            os.makedirs(os.path.join(self.workspace, self.name))
        except OSError:
            pass

        path = os.path.join(self.workspace, self.name, self.name + '.exp')

        # let's backup file with version number
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    old_data = json.load(f)

                version = str(old_data['version']).replace('.', '-')

                backup_path = os.path.join(self.workspace, self.name, self.name + '_' + version + '.exp.bak')

                shutil.copy(path, backup_path)

            except ValueError as exc:
                raise Exception('Could not backup experiment file. Aborting saving..')

        # save to file
        with open(os.path.join(self.workspace, self.name,
                               self.name + '.exp'), 'w') as f:
            json.dump(save_dict, f, sort_keys=True, indent=4)


class ExperimentHandler(QObject):
    """
    Class for handling the creation of a new experiment.
    """

    def __init__(self, parent):
        """
        """
        self.parent = parent

    def initialize_new_experiment(self, exp_dict):
        """
        Initializes the experiment object with the given data.

        """
        prefs = self.parent.preferencesHandler

        experiment = Experiment(exp_dict['author'], 
                                os.path.basename(exp_dict['name']))

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
        """

        if path:
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
                             'cohesion of the experiment file.')

        prefs = self.parent.preferencesHandler
        experiment = Experiment(data['name'], data['author'])

        if 'layout' in data.keys() and data['layout'] != 'Infer from data':
            experiment.layout = data['layout']
        else:
            experiment.layout = ''

        if 'channel_groups' in data.keys() and data['channel_groups'] != 'MNE':
            experiment.channel_groups = data['channel_groups']
        else:

            meg_selections = dict([(sel, mne.read_selection(sel)) for sel in 
                                   mne.selection._SELECTIONS])

            experiment.channel_groups = {
                'eeg': {},
                'meg': meg_selections
            }

        # if opening old experiment manually
        if path:
            experiment.workspace = os.path.dirname(path)
        # if opening old experiment automatically on open
        else:
            experiment.workspace = os.path.dirname(
                prefs.previous_experiment_name)

        if len(data['subjects']) > 0:

            for subject_data in data['subjects']:

                subject_name = subject_data['subject_name']

                raw_fname = subject_data.get('raw_fname')
                # for backwards compatibility
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

                datatypes = []
                for source in find_all_sources():
                    datatype_path = pkg_resources.resource_filename(
                        source, 'datatypes')
                    if not os.path.exists(datatype_path):
                        continue
                    for package in os.listdir(datatype_path):
                        config_path = os.path.join(
                            datatype_path, package, 'configuration.json')
                        if os.path.exists(config_path):
                            with open(config_path, 'r') as f:
                                config = json.load(f)
                                datatype = config['id']
                                key = config['save_key']
                                entry = config['entry']
                                datatypes.append((key, source, package, entry, datatype))

                for save_key, source, package, entry, datatype in datatypes:
                    for inst_data in subject_data.get(save_key, []):
                        module_name, class_name = entry.split('.')
                        module = importlib.import_module(
                            '.'.join([source, 'datatypes', package, module_name]))
                        inst_class = getattr(module, class_name, None)

                        name = inst_data.get('name')
                        # backward compatibility
                        if not name and 'collection_name' in inst_data:
                            name = inst_data.get('collection_name')
                        if not name:
                            raise Exception('No name attribute found')

                        directory = getattr(subject, datatype + '_directory')
                        params = inst_data.get('params', {})

                        # for backwards compatibility
                        if datatype == 'evoked':
                            if not params.get(
                                    'conditions') and 'event_names' in inst_data:
                                params['conditions'] = inst_data['event_names']
                            params['bwc_path'] = os.path.join(
                                subject.path, 'epochs/average')
                        if datatype == 'spectrum':
                            if not params.get(
                                    'log_transformed') and 'log_transformed' in inst_data:
                                params['log_transformed'] = inst_data['log_transformed']
                        if datatype == 'tfr':
                            if not params.get(
                                    'decim') and 'decim' in inst_data:
                                params['decim'] = inst_data['decim']
                            if not params.get(
                                    'n_cycles') and 'n_cycles' in inst_data:
                                params['n_cycles'] = inst_data['n_cycles']
                            if not params.get(
                                    'evoked_subtracted') and 'evoked_subtracted' in inst_data:
                                params['evoked_subtracted'] = inst_data['evoked_subtracted']

                        if inst_class:
                            inst = inst_class(
                                name,
                                directory,
                                params,
                            )
                            subject.add(inst, datatype)

                experiment.add_subject(subject)

                # ensure that the folder structure exists
                # (to not crash on updates)
                subject.ensure_folders()

        prefs.previous_experiment_name = os.path.join(
            experiment.workspace, experiment.name)

        return experiment
