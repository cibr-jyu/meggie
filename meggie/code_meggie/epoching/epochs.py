# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppakangas, Janne Pesonen and Atte Rautio>

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
import os

from PyQt4.QtCore import QObject

import mne

from meggie.code_meggie.general.fileManager import load_epochs

class Epochs(QObject):
    
    """
    A class for creating and handling epochs.
    
    Public functions:
    
    create_epochs(raw, events, mag, grad, eeg, stim, eog, reject,
                  category, tmin, tmax)
    """

    def __init__(self, collection_name, subject, params, raw=None):
        """
        Constructor
        """
        QObject.__init__(self)
        self._collection_name = collection_name
        self._raw = raw
        self._params = params
        self._path = os.path.join(subject.epochs_directory, collection_name + '.fif')

    @property
    def raw(self):
        """
        Returns the current working raw object.
        """
        if isinstance(self._raw, mne.Epochs):
            return self._raw
        else:
            raw = self.load_working_file()
            return raw
 
    @raw.setter
    def raw(self, raw):
        """
        Sets the raw data for the epoch collection. 
        Keyword arguments:
        raw    -- the raw .fif of the collection
        """
        self._raw = raw
        
    @property
    def collection_name(self):
        """
        Returns the name of the epoch collection.
        """
        return self._collection_name

    @collection_name.setter
    def collection_name(self, collection_name):
        """
        Sets the name for the epoch collection. 
        Keyword arguments:
        collection_name    -- the name of the collection
        """
        # TODO: Add name checks, see experiment_name setter. At
        # this moment UI probably handles the name check.
        self._collection_name = collection_name
        
    @property
    def params(self):
        """
        Returns the params dictionary of the epoch collection parameters.
        """
        return self._params

    @params.setter
    def params(self, params):
        """
        Sets the parameters for the epoch collection. 
        Keyword arguments:
        params    -- dictionary of the parameters of the collection
        """
        self._params = params

    def load_working_file(self):
        if self._raw is None:
            self._raw = load_epochs(self._path)
        return self._raw

    @property
    def path(self):
        return self._path
                  