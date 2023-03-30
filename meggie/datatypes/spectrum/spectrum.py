""" Defines Spectrum class, stores numpy arrays representing PSDs.
"""

import os
import re
import logging

import numpy as np
import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.datatype import Datatype


class Spectrum(Datatype):
    """ Wraps numpy arrays of PSDs.

    MNE-python does not have a dedicated class for storing PSDs. However, for
    our purposes it is good to have similar interface as the evokeds, TFRs,
    etc. Data is stored in csv files.

    Parameters
    ----------
    name : str
        Name of the spectrum, used in the UI lists and in the .exp file.
    directory : str
        Absolute path to the data folder, usually workspace/experiment/subject/spectrums.
    params : dict
        Contains additional information about the spectrum.
    content : dict of np.array, optional
        The spectral content as a numpy array. If not provided,
        is assumed to be saved to file system earlier.
    freqs : np.array, optional
        Frequencies as a array of points in frequency. If not provided,
        is assumed to be saved to file system earlier.
    info : mne.Info, optional
        The info structure from the raw data. Is stored because contains
        channel names and locations. If not provided, is assumed 
        to be saved to file system earlier.

    """
    def __init__(self, name, directory, params,
                 content=None, freqs=None, info=None):
        # name has no group number and no '.fif'
        self._name = name
        self._directory = directory
        self._params = params

        self._content = {}
        if content is not None:
            self._content = content

        self._params['info_set'] = True

        self._freqs = freqs
        self._info = info

    def _load_content(self):
        """Gets content from the file system and 
        stores it to corresponding attributes."""
        data_dict, freqs, ch_names = self._get_content()
        info = self._get_info()
        self._info = info
        self._freqs = freqs
        self._content = data_dict

    def _get_info(self):
        """ Gets info from file system.
        """
        info_path = os.path.join(self._directory,
                                 self._name + '-info.fif')
        info = mne.io.meas_info.read_info(info_path)

        return info

    def _get_content(self):
        """Handles the file loading."""

        # load data
        data_dict = {}
        template = self.name + '_' + r'([a-zA-Z1-9_]+)\.csv'
        for fname in os.listdir(self._directory):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    raise Exception("Unknown file name format.")

                # if proper condition parameters set,
                # check if the key is in there.
                if 'conditions' in self._params:
                    if key not in [str(elem) for elem in
                                   self._params['conditions']]:
                        continue

                freqs, row_descs, psd = filemanager.load_csv(
                    os.path.join(self._directory, fname))

                ch_names = [desc[0] for desc in row_descs]

                # for backwards compatibility
                # (used to have possibility to have spectrum data
                # saved as log transformed)
                if 'log_transformed' in self._params:
                    if self._params['log_transformed'] is True:
                        if np.mean(psd) < 0:
                            psd = 10 ** (psd / 10.0)

                freqs = np.array(freqs).astype(float)
                data_dict[key] = np.array(psd)

        return data_dict, freqs, ch_names

    def save_content(self):
        """Saves spectral data and info structure to the spectrum directory.
        """
        try:
            # save info
            info_path = os.path.join(self._directory,
                                     self._name + '-info.fif')
            mne.io.meas_info.write_info(info_path, self._info)
            self._params['info_set'] = True

            # save data
            for key, psd in self._content.items():

                row_descs = [(ch_name,) for ch_name in self.ch_names]
                column_names = self._freqs.tolist()
                data = psd.tolist()

                path = os.path.join(self._directory,
                                    self._name + '_' + str(key) + '.csv')

                filemanager.save_csv(path, data, column_names, row_descs)
        except Exception as exc:
            raise Exception("Writing spectrums failed. Please check that the "
                            "entire experiment folder has write permissions.")

    def delete_content(self):
        """Removes spectral data and info structure from the
        file system.
        """

        # delete info
        info_path = os.path.join(self._directory,
                                 self._name + '-info.fif')
        if os.path.exists(info_path):
            os.remove(info_path)

        # delete data
        template = self.name + '_' + r'([a-zA-Z1-9_]+)\.csv'
        for fname in os.listdir(self._directory):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    continue

                # if proper condition parameters set,
                # check if the key is in there.
                if 'conditions' in self._params:
                    if key not in [str(elem) for elem in
                                   self._params['conditions']]:
                        continue

                os.remove(os.path.join(self._directory, fname))

    def set_info(self, subject):
        """Stores info structure to the spectrum object. 

        This is for backwards compatibility. We used to get sensor locations
        from the raw object. This was problematic as the raw could change
        after creation of the spectrum.
        """
        info = subject.get_raw(preload=False).info

        # filter to correct set of channels
        _, _, ch_names = self._get_content()
        picks = [ch_idx for ch_idx, ch_name in enumerate(info['ch_names'])
                 if ch_name in ch_names]
        info = mne.pick_info(info, sel=picks)

        self._info = info
        self.save_content()

    @property
    def data(self):
        """Returns the dict of numpy arrays (conditions as keys, PSDs as values).
        """
        return self.content

    @property
    def content(self):
        """Returns the dict of numpy arrays (conditions as keys, PSDs as values).
        """
        if not self._content:
            self._load_content()
        return self._content

    @property
    def freqs(self):
        """Returns freqs, must read the data to memory first.
        """
        if not self._content:
            self._load_content()
        return self._freqs

    @property
    def ch_names(self):
        """Returns channel names from the info structure, must
        read the data to memory first."""
        return self.info['ch_names']

    @property
    def info(self):
        """Returns the info structure, must read the data to
        memory first."""
        if not self._content:
            self._load_content()
        return self._info

    @property
    def name(self):
        """Returns name of the spectrum"""
        return self._name

    @property
    def params(self):
        """Returns additional information stored, for example
        the conditions that are looked for in the spectrums
        directory, when loading the data.
        """
        return self._params

