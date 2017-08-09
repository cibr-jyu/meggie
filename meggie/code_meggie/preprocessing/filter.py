""" This module provides functions for filtering
"""

from meggie.ui.utils.decorators import threaded
from meggie.code_meggie.general.wrapper import wrap_mne_call

import meggie.code_meggie.general.fileManager as fileManager


@threaded
def filter_data(experiment, dic, subject, n_jobs, preview=False, **kwargs):
    """
    Filters the data array in place according to parameters in paramDict.
    Depending on the parameters, the filter is one or more of
    lowpass, highpass and bandstop (notch) filter.
    """

    dataToFilter = subject.get_working_file()

    if preview:
        dataToFilter = dataToFilter.copy()

    hfreq = dic['low_cutoff_freq'] if dic['lowpass'] else None
    lfreq = dic['high_cutoff_freq'] if dic['highpass'] else None
    length = dic['length']
    trans_bw = dic['trans_bw']

    print "Filtering..."
    wrap_mne_call(experiment, dataToFilter.filter,
                  l_freq=lfreq, h_freq=hfreq, filter_length=length,
                  l_trans_bandwidth=trans_bw,
                  h_trans_bandwidth=trans_bw, n_jobs=n_jobs,
                  method='fft', verbose=True)

    freqs = list()
    if dic['bandstop1']:
        freqs.append(dic['bandstop1_freq'])
    if dic['bandstop2']:
        freqs.append(dic['bandstop2_freq'])
    if len(freqs) > 0:
        length = dic['bandstop_length']
        trans_bw = dic['bandstop_transbw']

        print "Band-stop filtering..."
        wrap_mne_call(experiment, dataToFilter.notch_filter,
                      freqs, picks=None, filter_length=length,
                      notch_widths=dic['bandstop_bw'],
                      trans_bandwidth=trans_bw, n_jobs=n_jobs,
                      verbose=True)

    if not preview:
        fileManager.save_raw(experiment, dataToFilter,
                             dataToFilter.info['filename'], overwrite=True)

    return dataToFilter
