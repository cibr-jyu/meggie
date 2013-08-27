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

@author: Jaakko Leppakangas, Atte Rautio
Contains the File-class for file operations.
"""
import mne

from PyQt4.QtCore import QObject
from PyQt4 import QtGui

import os
import pickle
import csv
import shutil

from statistic import Statistic

class FileManager(QObject):
    
    """
    A class for file operations.
    
    public functions:
    
    copy(self, original, target)
    create_csv_epochs(self, epochs)
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
        
    def copy(self, original, target):
        """Copy the file at original to target.
        
        return True if no exceptions were raised, otherwise return
        the exception 
        """
        try:
            shutil.copyfile(original, target)
        
        except Error as e:
            return e
        
        except IOError as e:
            return e
        
        return True
        
    def create_csv_epochs(self, epochs):
        """Create a list used for creating a csv file based on epochs.
        
        The file contains the
        epoch,  channel, min, min_time, max, max_time,
        half_max, half_max_time- and half_max_time+ in that order.
        
        Keyword arguments:
        
        epochs -- An instance of epochs.
        
        return a list of rows to write.
        """
        stat = Statistic()
        data = epochs.get_data()
        rows = []
        #Create the first row with headings for the fields
        rows.append(['epoch','channel','min','min_time','max','max_time',
                     'half_max','half_max_time-','half_max_time+'])
        
        #create the actual rows
        for i in range(len(data)):
            
            for j in range(len(data[i])):
                
                row = []
                row.append(i)
                
                row.append(epochs.ch_names[j])
                
                min, min_time = stat.find_minimum(data[i][j])
                row.append(min)
                row.append(epochs.times[min_time])
                
                max, max_time = stat.find_maximum(data[i][j])
                row.append(max)
                row.append(epochs.times[max_time])
                
                half_max, half_max_time_b, half_max_time_a =\
                stat.find_half_maximum(data[i][j])
                
                row.append(half_max)
                #If half_max_times are -1, the half_max value is not reached
                #inside the epoch window.
                if half_max_time_b == -1:
                    row.append(None)
                else:
                    row.append(epochs.times[half_max_time_b])
                    
                if half_max_time_a == -1:
                    row.append(None)
                else:
                    row.append(epochs.times[half_max_time_a])
                
                rows.append(row)
                
        return rows    
        
    def delete_file_at(self, folder, files):
        """Delete files from a folder.
        
        Keyword arguments:
        
        folder -- The location of the deleted files
        files  -- The files to be deleted. Can be a single file or a list of
                  files in the same folder.
                  
        Return True if operation was succesful, otherwise return False.
        """
        
        try:
            os.remove(folder + files)
            
        except OSError as e:
            for file in files:
                try:
                    os.remove(folder + file)
        
                except OSError as e:
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
        item = QtGui.QListWidgetItem(name)
        try:
            epochs = mne.read_epochs(folder + name)
            item.setData(32, epochs)
            
        except Exception:
            try:
                epochs = mne.read_epochs(folder + name + '.fif')
                item.setData(32, epochs)
            
            except Exception as e:
                print str(e)
                return
        
        try:
            parameters = self.unpickle(folder + name + '.param')
            
        except IOError:
            return item
        #The events need to be converted back to QListWidgetItems.
        event_list = []
        event_dict = parameters['events']
        for key in event_dict:
            for event in event_dict[key]:
                event_tuple = (event, key)
                event_list.append(event_tuple)
        
        parameters['events'] = event_list
        #Create and return the QListWidgetItem

        item.setData(33, parameters)
        
        return item
    
    def load_epochs(self, fname):
        """Load epochs from a folder.
        
        Keyword arguments:
        fname -- the name of the fif-file containing epochs.
        
        return epochs in a QListWidgetItem 
        """
        split = os.path.split(fname)
        folder = split[0] + '/'
        name = os.path.splitext(split[1])[0]
        if name == '': return
        else:
            item = self.load_epoch_item(folder, name)
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
        if parameters is None: return
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
        
        csv_rows = self.create_csv_epochs(epochs)
        
        #Create a csv file of the epochs
        with open(fpath + '.csv', 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
            row_number = 1
            for row in csv_rows:
                if row_number % 1000 == 0:
                    print ('Csv file: Writing row ' + str(row_number) +
                           ' of ' + str(len(csv_rows))) 
                csv_writer.writerow(row)
                row_number += 1
        
    def unpickle(self, fpath):
        """Unpickle an object from a file at fpath.
        
        Keyword arguments:
        
        fpath -- the path to the pickled file.
        
        Return the unpickled object or None if unpickling failed.
        Raise an IOError if unpickling fails.
        """
        return pickle.load( open(fpath, 'rb') )