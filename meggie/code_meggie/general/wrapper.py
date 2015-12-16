"""
Created on 13.12.2015

@author: talli
"""

from meggie.ui.utils.decorators import logged, batched#, logged2

@logged
def wrap_mne_call(logger, mne_func, *args, **kwargs):
    return

@batched
def batch_mne_call():
    return