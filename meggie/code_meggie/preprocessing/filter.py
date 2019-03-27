"""
"""

import logging

import meggie.code_meggie.general.fileManager as fileManager

from meggie.ui.utils.decorators import threaded


@threaded
def filter_data(experiment, dic, subject, preview=False, **kwargs):
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

    logging.getLogger('ui_logger').info("Filtering.")
    dataToFilter.filter(l_freq=lfreq, h_freq=hfreq, filter_length=length,
        l_trans_bandwidth=trans_bw, h_trans_bandwidth=trans_bw,
        method='fft', fir_design='firwin')

    freqs = list()
    if dic['bandstop1']:
        freqs.append(dic['bandstop1_freq'])
    if dic['bandstop2']:
        freqs.append(dic['bandstop2_freq'])
    if len(freqs) > 0:
        length = dic['bandstop_length']
        trans_bw = dic['bandstop_transbw']

        logging.getLogger('ui_logger').info("Band-stop filtering.")
        dataToFilter.notch_filter(freqs, picks=None, filter_length=length,
            notch_widths=dic['bandstop_bw'], trans_bandwidth=trans_bw)

    if not preview:
        fname = dataToFilter.filenames[0]
        fileManager.save_raw(experiment, dataToFilter,
                             fname, overwrite=True)

    return dataToFilter
