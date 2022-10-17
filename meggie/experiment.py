""" Contains classes and functions for experiments.
"""

import os
import json
import importlib
import shutil
import logging
import pkg_resources

from meggie.subject import Subject

from meggie.utilities.filemanager import open_raw
from meggie.utilities.filemanager import save_raw
from meggie.utilities.channels import get_default_channel_groups
from meggie.utilities.validators import validate_name
from meggie.utilities.uid import generate_uid

from meggie.mainwindow.dynamic import find_all_datatype_specs


class Experiment:
    """ A top-level class that contains structure of an experiment,
    all the subjects within, and so forth.

    Parameters
    ----------
    name : str
        Name of the experiment
    author : str
        Name of the author
    path : str
        Path to the experiment folder.
    """
    def __init__(self, name, author, path):
        self._name = name
        self._author = author
        self._path = path
        self._subjects = {}
        self._active_subject = None

        self._channel_groups = {
            'eeg': {},
            'meg': {},
        }
        self._selected_pipeline = 'classic'

    @property
    def path(self):
        """ Returns the path. """
        return self._path

    @path.setter
    def path(self, path):
        """ Sets the path. """
        self._path = path

    @property
    def name(self):
        """ Returns the name. """
        return self._name

    @name.setter
    def name(self, name):
        """ Sets the name. """
        self._name = validate_name(
            name, fieldname='name')

    @property
    def author(self):
        """ Returns the author."""
        return self._author

    @author.setter
    def author(self, author):
        """ Sets the author."""
        self._author = validate_name(author, minlength=0, fieldname='author')

    @property
    def channel_groups(self):
        """ Returns channel groups for experiment. If not set,
        uses defaults."""
        channel_groups = self._channel_groups.copy()

        # if channel groups not found, use defaults..
        if not channel_groups.get('eeg'):
            if self.active_subject:
                raw = self.active_subject.get_raw(preload=False)
                try:
                    channel_groups['eeg'] = get_default_channel_groups(raw, 'eeg')
                except Exception as exc:
                    pass

        if not channel_groups.get('meg'):
            if self.active_subject:
                raw = self.active_subject.get_raw(preload=False)
                try:
                    channel_groups['meg'] = get_default_channel_groups(raw, 'meg')
                except Exception as exc:
                    pass

        return channel_groups

    @channel_groups.setter
    def channel_groups(self, channel_groups):
        """ Sets the channel groups."""
        self._channel_groups = channel_groups

    @property
    def selected_pipeline(self):
        """ Returns selected pipeline
        """
        return self._selected_pipeline

    @selected_pipeline.setter
    def selected_pipeline(self, selected_pipeline):
        """ Sets selected pipeline """
        self._selected_pipeline = selected_pipeline

    @property
    def active_subject(self):
        """ Returns the active subject.
        """
        return self._active_subject

    @active_subject.setter
    def active_subject(self, subject):
        """ Sets the active subject.
        """
        self._active_subject = subject

    def add_subject(self, subject):
        """ Adds subject to the experiment.

        Parameters
        ----------
        subject : meggie.subject.Subject
            A subject object.
        """
        self.subjects[subject.name] = subject

    @property
    def subjects(self):
        """ Returns contained subjects.
        """
        return self._subjects

    def remove_subject(self, name):
        """Removes a subject.

        Removes the subject folder and its contents under experiment tree, and
        removes the subject from the experiment.

        Parameters
        ----------
        name : str
            Name of the subject to be removed.
        
        """

        if getattr(self, 'active_subject',
                   None) and self.active_subject.name == name:
            self.active_subject = None

        subject = self.subjects.pop(name)

        try:
            shutil.rmtree(subject.path)
        except Exception as exc:
            raise Exception(
                'Could not remove the contents of the subject folder.')

    def activate_subject(self, subject_name):
        """Activates a subject from the existing subjects

        Parameters
        ----------
        subject_name : str
            Name of the subject.

        Returns
        -------
        meggie.subject.Subject
            The activated subject.
        """
        # remove raw files from memory before activating new subject.
        if self.active_subject:
            self.active_subject.release_memory()

        self.active_subject = self.subjects[subject_name]

        # test validity
        self.active_subject.get_raw(preload=False)

        return self.active_subject

    def create_subject(self, subject_name, raw_path):
        """ Creates a subject object and copies the raw file
        inside it (by reading and saving).

        Parameters
        ----------
        subject_name : str
            Name of the new subject.
        raw_path : str
            Path to the data file.
        """
        bname = os.path.basename(raw_path)
        stem, ext = os.path.splitext(bname)
        new_fname = stem + '.fif'

        uid = generate_uid()

        subject = Subject(self, subject_name, new_fname, uid)
        subject.ensure_folders()

        raw = open_raw(raw_path)

        new_path = os.path.join(subject.path, new_fname)
        save_raw(raw, new_path)

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
                'uid': subject.uid,
                'ica_applied': subject.ica_applied,
                'rereferenced': subject.rereferenced,
            }

            datatype_specs = find_all_datatype_specs()

            for source, package, datatype_spec in datatype_specs.values():
                save_key = datatype_spec['save_key']
                datatype = datatype_spec['id']

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
            'channel_groups': self._channel_groups,
            'selected_pipeline': self._selected_pipeline
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
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    old_data = json.load(f)

                version = str(old_data['version']).replace('.', '-')

                backup_path = os.path.join(self._path, 
                    os.path.basename(self._path) + '_' + version + '.exp.bak')

                shutil.copy(path, backup_path)
        except Exception as exc:
            message = ("Could not backup experiment file to {0}. "
                       "Please check that the experiment folder "
                       "has write permissions everywhere.")
            raise Exception(message.format(backup_path))

        # and then overwrite the current exp file
        try:
            with open(path, 'w') as f:
                json.dump(save_dict, f, sort_keys=True, indent=4)
        except Exception as exc:
            message = ("Could not save experiment file {0}. "
                       "Please check that the experiment folder "
                       "has write permissions everywhere.")
            raise Exception(message.format(path))

def initialize_new_experiment(name, author, prefs, set_previous_experiment=True):
    """Initializes new experiment object with given data.

    Parameters
    ----------
    name : str
        Name of the experiment.
    author : str
        Name of the author.
    prefs : meggie.mainwindow.preferences.PreferencesHandler
        A preferences object.

    Returns
    -------
    meggie.experiment.Experiment
        The new experiment.

    """
    path = os.path.join(prefs.workspace, name)
    if os.path.exists(path):
        raise Exception('Experiment with same name already exists.')

    experiment = Experiment(name, author, path)
    experiment.save_experiment_settings()

    if set_previous_experiment:
        prefs.previous_experiment_name = experiment.path
        prefs.write_preferences_to_disk()
    return experiment


def open_existing_experiment(prefs, path=None):
    """ Reads and opens existing experiment.

    Parameters
    ----------
    prefs : meggie.mainwindow.preferences.PreferencesHandler
        A preferences object.
    path : str, optional
        Path to the experiment folder.

    Returns
    -------
    meggie.experiment.Experiment
        The opened experiment.
    """

    experiment_updated = False

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
        logging.getLogger('ui_logger').exception('')
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

    if 'selected_pipeline' in data.keys():
        experiment.selected_pipeline = data['selected_pipeline']

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

        uid = subject_data.get('uid')
        if not uid:
            uid = generate_uid()
            experiment_updated = True

        subject = Subject(experiment,
                          subject_name,
                          raw_fname,
                          uid,
                          ica_applied=subject_data.get('ica_applied', False),
                          rereferenced=subject_data.get('rereferenced', False)
                          )

        datatype_specs = find_all_datatype_specs()

        for source, package, datatype_spec in datatype_specs.values():
            save_key = datatype_spec['save_key']
            entry = datatype_spec['entry']
            datatype = datatype_spec['id']

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
                        params.copy(),
                    )
                    subject.add(inst, datatype)

                    # for backwards compatibility,
                    # ensure spectrum objects contain info
                    if datatype == 'spectrum' and not params.get('info_set'):
                        inst.set_info(subject)

        experiment.add_subject(subject)

        # ensure that the folder structure exists
        # (to not crash on updates)
        subject.ensure_folders()

    if experiment_updated:
        experiment.save_experiment_settings()

    return experiment
