"""Defines TFR class, wraps mne.AverageTFR objects."""

import os
import re

import mne

from meggie.utilities.datatype import Datatype


class TFR(Datatype):
    """A wrapper for mne.AverageTFR objects.

    Parameters
    ----------
    name : str
        Name of the tfr, used in the UI lists and in the .exp file.
    directory : str
        Absolute path to the data folder, usually workspace/experiment/subject/tfrs.
    params : dict
        Contains additional information about the tfr.
    content : dict of mne.AverageTFR, optional
        Stores mne.AverageTFR objects as values, conditions as keys. If not provided,
        is assumed to be saved to file system earlier.
    """

    def __init__(self, name, directory, params, content=None):
        self._name = name
        self._params = params
        self._directory = directory

        # ensure comments are set to match the keys / conditions
        self._content = content
        if self._content:
            for key in self._content.keys():
                self._content[key].comment = key

    def _clean_condition_name(self, name):
        return str(name).replace(" ", "_")

    def save_content(self):
        """Saves the mne.AverageTFR to h5 files in the tfr directory."""
        try:
            for tfr_name, mne_tfr in self._content.items():

                # fail quickly for very old-style tfr's
                assert tfr_name

                fname = os.path.join(
                    self._directory,
                    self._name + "-" + self._clean_condition_name(tfr_name) + "-tfr.h5",
                )

                mne_tfr.save(fname, overwrite=True)
        except Exception:
            raise Exception(
                "Writing TFRs failed. Please ensure that the "
                "entire experiment folder has write permissions."
            )

    def delete_content(self):
        """Deletes the correct h5 files in the tfr directory"""

        template = self._name + "-" + r"([a-zA-Z1-9_-]+)\-tfr\.h5"
        for fname in os.listdir(self._directory):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception:
                    continue

                # if proper condition parameters set,
                # check if the key is in there
                if "conditions" in self._params:
                    if key not in [
                        self._clean_condition_name(elem)
                        for elem in self._params["conditions"]
                    ]:
                        continue

                os.remove(os.path.join(self._directory, fname))

    def _load_content(self):
        """Handle the loading of the content."""
        self._content = {}
        template = self._name + "-" + r"([a-zA-Z1-9_-]+)\-tfr\.h5"
        for fname in os.listdir(self._directory):
            match = re.match(template, fname)
            if match:
                try:
                    fname_key = str(match.group(1))
                except Exception:
                    raise Exception("Unknown file name format.")

                condition_key = fname_key

                # skip this for old-style tfrs
                if "conditions" in self._params:
                    for condition_name in self._params["conditions"]:
                        if fname_key == self._clean_condition_name(condition_name):
                            condition_key = condition_name
                            break
                    else:
                        continue

                path = os.path.join(self._directory, fname)
                self._content[condition_key] = mne.time_frequency.read_tfrs(path)

    @property
    def content(self):
        """Returns the actual mne.AverageTFR objects either
        from cache or from the file system.
        """
        if self._content is None:
            self._load_content()
        return self._content

    @property
    def params(self):
        """Returns additional information stored."""
        return self._params

    @property
    def data(self):
        """Returns the actual numerical data of TFRs."""
        data = {}
        for key in self.content.keys():
            data[key] = self.content[key].data
        return data

    @property
    def name(self):
        """Returns the name of the tfr."""
        return self._name

    @property
    def decim(self):
        """Returns the decimation factor used in the creation."""
        return self._params.get("decim")

    @property
    def n_cycles(self):
        """ "Returns the number of cycles in used in the creation."""
        return self._params.get("n_cycles")

    @property
    def ch_names(self):
        """Returns the channel names, must read the data first."""
        return list(self.content.values())[0].info["ch_names"]

    @property
    def times(self):
        """Returns the array of times, must read the data first."""
        return list(self.content.values())[0].times

    @property
    def freqs(self):
        """Returns the array of freqs, must read the data first."""
        return list(self.content.values())[0].freqs

    @property
    def info(self):
        """Returns the info structure, must read the data first."""
        return list(self.content.values())[0].info

    @property
    def evoked_subtracted(self):
        """Returns whether evoked was subtracted in the creation."""
        return self._params.get("evoked_subtracted")
