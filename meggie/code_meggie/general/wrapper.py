"""
Created on 13.12.2015

@author: talli
"""

from meggie.ui.utils.decorators import logged#, logged2

@logged
def wrap_mne_call(logger, mne_func, *args, **kwargs):
    return