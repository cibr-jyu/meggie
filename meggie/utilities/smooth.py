"""
from: http://scipy.org/Cookbook/SignalSmooth
"""

import numpy as np
import matplotlib.pyplot as plt

def smooth_signal(x, window_len=10, window='hanning'):
    """
    """

    if x.ndim != 1:
        raise ValueError("Smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s=np.r_[2*x[0]-x[window_len:1:-1], x, 2*x[-1]-x[-1:-window_len:-1]]
    
    if window == 'flat':
        w = np.ones(window_len,'d')
    else:
        w = getattr(np, window)(window_len)

    y = np.convolve(w/w.sum(), s, mode='same')
    return y[window_len-1:-window_len+1]
