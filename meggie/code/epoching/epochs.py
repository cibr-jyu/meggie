# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 12, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen
Contains the Epochs-class for handling epochs created from the MEG data.
"""
from PyQt4.QtCore import QObject

import mne

import pylab as pl

class Epochs(QObject):
    
    """
    A class for creating and handling epochs.
    
    Public functions:
    
    create_epochs(raw, events, mag, grad, eeg, stim, eog, reject,
                  category, tmin, tmax)
    """

    def __init__(self):
        """
        Constructor
        """
        QObject.__init__(self)
        
    def create_epochs(self, raw, events, mag, grad, eeg, stim,
                      eog, reject, category, tmin, tmax):
        """Create a new set of epochs.
        
        Keyword arguments:
        raw           = A raw data object.
        events        = Array of events.
        mag           = Boolean telling if magnetometers will be used.
        grad          = Boolean telling if whether gradiometers will be used.
        eeg           = Boolean telling if whether eeg-channels will be used.
        stim          = Boolean telling if whether stim-channels will be used.
        eog           = Boolean telling if whether eog-channels will be used.
        reject        = Rejection parameter for epochs.
        category      = Dictionary of categories.
        tmin          = Start time before event
        tmax          = End time after the event
        
        Exceptions:
        Raises TypeError if the raw object isn't of type mne.fiff.Raw.
        Raises Exception if picks are empty.
        
        Returns a set of epochs
        """
        if mag and grad:
            meg = True
        elif mag:
            meg = 'mag'
        elif grad:
            meg = 'grad'
        else:
            meg = False
        if isinstance(raw, mne.fiff.raw.Raw):
            picks = mne.fiff.pick_types(raw.info, meg=meg, eeg=eeg,
                                        stim=stim, eog=eog)
            if picks is None:
                raise Exception('Picks cannot be empty. ' + 
                                'Select picks by checking the checkboxes.')
            epochs = mne.Epochs(raw, events, category,
                                tmin, tmax, picks=picks, reject=reject)
            return epochs
        else:
            raise TypeError('Not a Raw object.')
        
    def create_epochs_from_dict(self, dict, raw):
        """Create a set of epochs with parameters stored in a dict.
        
        Keyword arguments:
        
        dict = A dictionary containing the parameter values for epoching minus
               the raw data object.
        raw  = the raw data object
        
        Return a set of epochs.
        """
        events = dict['events']
        mag = dict['mag']
        grad = dict['grad']
        eeg = dict['eeg']
        stim = dict['stim']
        eog = dict['eog']
        reject = dict['reject']
        category = dict['category']
        tmin = dict['tmin']
        tmax = dict['tmax']
        
        epochs = self.create_epochs(raw, events, mag, grad, eeg, stim, eog,
                                    reject, category, tmin, tmax)
        return epochs        