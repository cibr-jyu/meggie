""" Contains controlling logic for the filter.
"""

import logging

def filter_data(subject, params, preview=False):
    """
    Filters the data array in place according to parameters in paramDict.
    Depending on the parameters, the filter is one or more of
    lowpass, highpass and bandstop (notch) filter.
    """

    raw = subject.get_raw()

    if preview:
        raw = raw.copy()

    hfreq = params['low_cutoff_freq'] if params['lowpass'] else None
    lfreq = params['high_cutoff_freq'] if params['highpass'] else None
    length = params['length']
    trans_bw = params['trans_bw']

    raw.filter(l_freq=lfreq, h_freq=hfreq, filter_length=length,
               l_trans_bandwidth=trans_bw, h_trans_bandwidth=trans_bw,
               method='fft', fir_design='firwin')

    freqs = list()
    if params['bandstop1']:
        freqs.append(params['bandstop1_freq'])
    if params['bandstop2']:
        freqs.append(params['bandstop2_freq'])
    if len(freqs) > 0:
        length = params['bandstop_length']
        trans_bw = params['bandstop_transbw']

        raw.notch_filter(freqs, picks=None, filter_length=length,
                         notch_widths=params['bandstop_bw'], trans_bandwidth=trans_bw)

    if not preview:
        subject.save()

    return raw
