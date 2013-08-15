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
from PyQt4 import QtGui

import os
import pickle

class FileManager(QObject):
    
    """
    A class for file operations.
    
    public functions:
    
    delete_file_at(self, folder, name)
    load_epoch_item(self, folder, name)
    open_raw(self, fname)
    pickle(self, picklable, path)
    save_epoch_item(self, fpath, item, overwirte = False)
    unpickle(self, fpath)
    """ 
    
    def __init__(self):
        """Constructor"""
        QObject.__init__(self)
        
    def delete_file_at(self, folder, files):
        """Delete files from a folder.
        
        Keyword arguments:
        
        folder -- The location of the deleted files
        files  -- The files to be deleted. Can be a single file or a list of
                  files in the same folder.
                  
        Return True if operation was succesful, otherwise return False.
        """
        
        try:
            for file in files:
                try:
                    os.remove(folder + file)
        
                except OSError as e:
                    print str(e)
                    return False
        
        except TypeError:
            try:
                os.remove(folder + file)
        
            except OSError as e:
                print str(e)
                return False
        
        return True
        
    def load_epoch_item(self, folder, name):
        """Load epochs and the parameters used to create them from a file.
        
        Search the specified folder for 'name.fif' and 'name.param' -files and
        construct a QListWidget item from them. Epochs are stored in the item's
        data slot 32, parameter values are stored in data slot 33.
        
        Keyword arguments:
        
        folder -- The folder containing the required files.
        name   -- Both the base name of the files and the name of the created
                  QListWidget item.
                 
        Return a QListWidgetItem containing the epochs and their parameters.
        """
        try:
            epochs = mne.read_epochs(folder + name + '.fif')
            
        except Exception as e:
            print 'Could not load epochs' + str(e)
            return
        
        parameters = self.unpickle(folder + name + '.param')
        #The events need to be converted back to QListWidgetItems.
        event_list = []
        event_dict = parameters['events']
        for key in event_dict:
            for event in event_dict[key]:
                event_tuple = (event, key)
                event_list.append(event_tuple)
        
        parameters['events'] = event_list
        #Create and return the QListWidgetItem
        item = QtGui.QListWidgetItem(name)
        item.setData(32, epochs)
        item.setData(33, parameters)
        
        return item
    
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
        
    def pickle(self, picklable, fpath):
        """pickle a picklable object to a file indicated by fpath
        
        Keyword arguments:
        
        picklable -- A picklable object.
        fpath     -- Path to the pickled file
        """
        try:
            pickleFile = open(fpath, 'wb')
            
        except IOError as e:
            return str(e)
        
        # Protocol 2 used because of file object being pickled
        pickle.dump(picklable, pickleFile, 2)
        
        pickleFile.close()
        
    def save_epoch_item(self, fpath, item, overwrite = False):
        """Save epochs and the parameter values used to create them.
        
        The epochs are saved to fpath.fif. the parameter values are saved
        to fpath.param. Epochs are read from the QListWidgetItem's data
        slot 32, parameter values are in a dict at data slot 33.
        
        Keyword arguments:
        
        fpath     -- The full path and base name of the files
        item      -- A QListWidgetItem containing epochs
                    and their parameter values.
        overwrite -- A boolean telling whether existing files should be
                    replaced. False by default. 
        """
        if os.path.exists(fpath + '.fif') and overwrite is False:
            return
        
        #First save the epochs
        epochs = item.data(32).toPyObject()
        epochs.save(fpath + '.fif')
        
        #Then save the parameters using pickle.
        parameters = item.data(33).toPyObject()
        #toPyObject turns the dict keys into QStrings so convert them back to
        #strings.
        parameters_str = dict((str(k), v) for k, v in parameters.iteritems())
        
        event_dict = {}
        event_list = parameters_str['events']
        for item in event_list:
            key = str(item[1])
            event = item[0]
            #Create an empty list for the new key
            if key not in event_dict:
                event_dict[key] = []
            
            event_dict[key].append(event)
        
        parameters_str['events'] = event_dict
        
        parameterFileName = str(fpath + '.param')
        
        self.pickle(parameters_str, parameterFileName)
        
    def unpickle(self, fpath):
        """Unpickle an object from a file at fpath.
        
        Keyword arguments:
        
        fpath -- the path to the pickled file.
        
        Return the unpickled object or None if unpickling failed.
        """
        try:
            return pickle.load( open(fpath, 'rb') )
        
        except IOError:
            return None