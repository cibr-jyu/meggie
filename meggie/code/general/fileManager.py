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
Created on Mar 13, 2013

@author: Jaakko Leppakangas
Contains the File-class for file operations.
"""
import mne

from PyQt4.QtCore import QObject

import os
import pickle

class FileManager(QObject):
    """
    A class for file operations.
    
    public functions:
    
    open_raw(self, fname)
    save_epoch_item(self, fpath, item, overwirte = False)
    """
    
    
    def __init__(self):
        QObject.__init__(self) 
        
    def open_raw(self, fname):
        """
        Opens a raw file.
        Keyword arguments:
        fname         -- A file to open
        Raises an exception if the file cannot be opened.
        """
        if os.path.isfile(fname):# and fname.endswith('fif'):
            return mne.fiff.Raw(fname, preload=True)
            #self.raw = mne.fiff.Raw(str(fname))
        else:
            raise Exception('Could not open file.')
        
    def save_epoch_item(self, fpath, item, overwrite = False):
        """Save epochs and the parameter values used to create them.
        
        The epochs are saved to fpath.fif. the parameter values are saved
        to fpath.param. Epochs are read from the QListWidgetItem's data
        slot 32, parameter values are in a dict at data slot 33.
        
        Keyword arguments:
        
        fpath     = The full path and base name of the files
        item      = A QListWidgetItem containing epochs
                    and their parameter values.
        overwrite = A boolean telling whether existing files should be
                    replaced. False by default. 
        """
        if os.path.exists(fpath + '.fif') and overwrite is False:
            return
        
        #First save the epochs
        epochs = item.data(32).toPyObject()
        epochs.save(fpath + '.fif')
        
        #Then save the parameters using pickle.
        parameters = item.data(33).toPyObject()
        parameterFileName = str(fpath + '.param')
        
        parameterFile = open(parameterFileName, 'wb')
        
        # Protocol 2 used because of file object being pickled
        pickle.dump(parameters, parameterFile, 2)
        
        parameterFile.close() 