# coding: utf-8

"""
"""

import os
import json
import importlib
import shutil
import logging
import pkg_resources

from meggie.subject import Subject

from meggie.utilities.filemanager import copy_subject_raw
from meggie.utilities.dynamic import find_all_sources
from meggie.utilities.channels import get_default_channel_groups
from meggie.utilities.decorators import threaded
from meggie.utilities.validators import validate_name


class Experiment:

    """ A top-level class that contains structure of an experiment,
    all the subjects within, and so forth.
    """

    def __init__(self, name, author, path):
        """
        """
        self._name = name
        self._author = author
        self._path = path
        self._subjects = {}
        self._active_subject = None

        self._channel_groups = {
            'eeg': {},
            'meg': {},
        }

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

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
    def channel_groups(self):
        channel_groups = self._channel_groups.copy()

        # if channel groups not found, use defaults..
        if not channel_groups.get('eeg'):
            if self.active_subject:
                raw = self.active_subject.get_raw(preload=False)
                try:
                    channel_groups['eeg'] = get_default_channel_groups(raw.info, 'eeg')
                except Exception as exc:
                    logging.getLogger('ui_logger').debug(
                        'Could not get default channel groups for EEG')

        if not channel_groups.get('meg'):
            if self.active_subject:
                raw = self.active_subject.get_raw(preload=False)
                try:
                    channel_groups['meg'] = get_default_channel_groups(raw.info, 'meg')
                except Exception as exc:
                    logging.getLogger('ui_logger').debug(
                        'Could not get default channel groups for MEG')

        return channel_groups

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

        try:
            shutil.rmtree(subject.path)
        except OSError as exc:
            logging.getLogger('ui_logger').exception(str(exc))
            raise OSError(
                'Could not remove the contents of the subject folder.')

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
        """ Creates and adds subject object based on raw path
        """
        subject = Subject(self, subject_name, raw_fname)
        subject.ensure_folders()

        copy_subject_raw(subject, raw_path)
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
            'name': self._name,
            'author': self._author,
            'channel_groups': self._channel_groups
        }

        try:
            version = pkg_resources.get_distribution("meggie").version
        except BaseException:
            version = ''

        save_dict['version'] = version

        try:
            os.makedirs(self.path)
        except OSError:
            pass

        path = os.path.join(self._path, os.path.basename(self._path) + '.exp')
        # let's backup previous exp file with version number
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    old_data = json.load(f)

                version = str(old_data['version']).replace('.', '-')

                backup_path = os.path.join(self._path, 
                    os.path.basename(self._path) + '_' + version + '.exp.bak')

                shutil.copy(path, backup_path)

            except Exception as exc:
                logging.getLogger('ui_logger').exception(str(exc))
                logging.getLogger('ui_logger').warning(
                    'Could not backup experiment file. Please check your permissions..')

        # save to file
        try:
            with open(path, 'w') as f:
                json.dump(save_dict, f, sort_keys=True, indent=4)
        except Exception as exc:
            logging.getLogger('ui_logger').exception(str(exc))
            logging.getLogger('ui_logger').error(
                'Could not save the experiment file. Please check your permissions..')

def initialize_new_experiment(name, author, prefs):
    """
    Initializes new experiment object with given data.
    """
    path = os.path.join(prefs.workspace, name)
    if os.path.exists(path):
        raise Exception('Experiment with same name already exists.')

    experiment = Experiment(name, author, path)
    experiment.save_experiment_settings()

    prefs.previous_experiment_name = experiment.path
    prefs.write_preferences_to_disk()
    return experiment


def open_existing_experiment(prefs, path=None):
    """
    """

    if path:
        exp_file = os.path.join(path, os.path.basename(path) + '.exp')
    else:
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
        logging.getLogger('ui_logger').exception(str(exc))
        raise ValueError('Experiment from ' + exp_file + ' could not be ' +
                         'opened. There might be a problem with ' +
                         'cohesion of the experiment file.')

    if not path:
        path = os.path.dirname(exp_file)

    experiment = Experiment(data['name'], data['author'], path)

    if 'channel_groups' in data.keys() and data['channel_groups'] != 'MNE':
        experiment.channel_groups = data['channel_groups']
    else:
        experiment.channel_groups = {
            'eeg': {},
            'meg': {},
        }

    if len(data['subjects']) == 0:
        return experiment

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

    return experiment
