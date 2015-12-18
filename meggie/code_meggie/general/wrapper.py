"""
Created on 13.12.2015

@author: talli
"""

from meggie.ui.utils.decorators import logged, batched#, logged2

@logged
def wrap_mne_call(mne_func, *args, **kwargs):
    return mne_func(*args, **kwargs)

@batched
def batch_mne_call():
    return