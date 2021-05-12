""" Contains a class for logic of the Subjects.
"""

import os
import logging
import json
import pkg_resources

import meggie.utilities.filemanager as filemanager

from meggie.mainwindow.dynamic import find_all_sources


class Subject:
    """ The class for holding subject-specific information
    and subject-specific data.

    Parameters
    ----------
    experiment : meggie.experiment.Experiment
        The experiment to which the subject is created.
    name : str
        Name of the subject.
    raw_fname : str
        Path to the subject data.
    ica_applied : bool
        Whether ICA has been applied (at least once) to this data.
    rereferenced : bool
        Whether the data has been rereferenced (at least once).
    """

    def __init__(self, experiment, name, raw_fname,
                 ica_applied=False, rereferenced=False):
        self.name = name
        self.raw_fname = raw_fname

        self._raw = None

        self.ica_applied = ica_applied
        self.rereferenced = rereferenced

        self.path = os.path.join(experiment.path,
                                 name)

        for source in find_all_sources():
            datatype_path = pkg_resources.resource_filename(source, 'datatypes')
            if not os.path.exists(datatype_path):
                continue
            for package in os.listdir(datatype_path):
                config_path = os.path.join(
                    datatype_path, package, 'configuration.json')
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        datatype = config['id']
                        dir_ = config['dir']

                        # for example: self.epochs
                        setattr(self, datatype, dict())
                        # for example: self.epochs_directory
                        setattr(self, datatype + '_directory',
                                os.path.join(self.path, dir_))

    def add(self, dataobject, datatype):
        """ Adds a dataobject of type datatype to the subject.

        Parameters
        ----------
        dataobject : instance of a datatype
            A data object.
        datatype : str
            Name of the datatype.
        """
        container = getattr(self, datatype)
        name = dataobject.name
        container[name] = dataobject

    def remove(self, name, datatype):
        """ Removes a dataobject by name from the subject. 

        Parameters
        ----------
        name : str
            Name of the data object.
        datatype : str
            Name of the datatype.

        """
        container = getattr(self, datatype)
        dataobject = container.pop(name, None)
        try:
            dataobject.delete_content()
        except Exception as exc:
            logging.getLogger('ui_logger').exception('')
            raise IOError('Could not delete ' + str(datatype) +
                          ' from folders')

    @property
    def raw_path(self):
        """ Returns the raw path."""
        path = os.path.join(self.path,
                            self.raw_fname)
        return path

    def get_raw(self, preload=True, verbose='info'):
        """ Gets the raw object for the subject.

        Reads from the file system if not in the memory already.

        Parameters
        ----------
        preload : bool
            Whether to read the data or only the metadata.
        verbose : str
            Verbose level of read_raw.

        Returns
        -------
        mne.io.Raw
            The raw object.
        """
        if self._raw is not None:
            if preload:
                self._raw.load_data()
            return self._raw
        else:
            try:
                raw = filemanager.open_raw(self.raw_path, preload=preload, 
                                           verbose=verbose)
            except OSError:
                raise IOError("Could not find the raw file.")
            self._raw = raw
            return raw

    def save(self):
        """ Saves the data to the existing path. """
        filemanager.save_raw(self._raw, self.raw_path)

    def release_memory(self):
        """ Releases data from the memory.
        """
        if self._raw is not None:
            self._raw = None

    @property
    def sss_applied(self):
        """Checks if sss applied.
        """

        try:
            raw = self.get_raw()
            for item in raw.info['proc_history']:
                if 'maxfilter' in item.get('creator', []):
                    return True
        except Exception as exc:
            return False

        return False

    def ensure_folders(self):
        """ When called, checks that the subject folder with all datatype folders
        exist and if not, creates them.
        """
        paths = []
        for source in find_all_sources():
            datatype_path = pkg_resources.resource_filename(source, 'datatypes')
            if not os.path.exists(datatype_path):
                continue
            for package in os.listdir(datatype_path):
                config_path = os.path.join(datatype_path, package,
                                           'configuration.json')
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        datatype = config['id']
                        path = getattr(self, datatype + '_directory')
                        paths.append(path)

        try:
            filemanager.ensure_folders(
                [self.path] + paths)
        except OSError:
            raise OSError("Couldn't create all the necessary folders. "
                          "Do you have the necessary permissions?")
