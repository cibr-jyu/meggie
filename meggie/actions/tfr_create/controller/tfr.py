""" Contains controlling logic for tfr create
"""

import mne

from meggie.utilities.threading import threaded
from meggie.utilities.validators import assert_arrays_same

from meggie.datatypes.tfr.tfr import TFR


@threaded
def create_tfr(subject, tfr_name, epochs_names,
               freqs, decim, n_cycles, subtract_evoked):
    """ Handles tfr item creation.
    """

    time_arrays = []
    for name in epochs_names:
        collection = subject.epochs.get(name)
        if collection:
            time_arrays.append(collection.content.times)
    assert_arrays_same(time_arrays)

    tfrs = {}
    for epoch_name in epochs_names:
        epochs = subject.epochs[epoch_name].content
        if subtract_evoked:
            epochs = epochs.copy().subtract_evoked()

        tfr = mne.time_frequency.tfr.tfr_morlet(epochs, 
                                                freqs=freqs, 
                                                n_cycles=n_cycles,
                                                decim=decim, 
                                                average=True,
                                                return_itc=False)
        tfrs[epoch_name] = tfr

    # convert list-like to list
    if hasattr(n_cycles, '__len__'):
        n_cycles = list(n_cycles)

    params = {
        'decim': decim,
        'n_cycles': n_cycles,
        'evoked_subtracted': subtract_evoked,
        'conditions': epochs_names
    }

    meggie_tfr = TFR(tfr_name, subject.tfr_directory, params, tfrs)

    meggie_tfr.save_content()
    subject.add(meggie_tfr, "tfr")

