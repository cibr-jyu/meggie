# coding: latin1

# Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies, 
# either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 13, 2013

@author: Jaakko Leppakangas, Atte Rautio, Kari Aliranta
Contains the File-class for file operations.

A module for various file operations needed by Meggie.

public functions:

copy(self, original, target)
create_csv_epochs(self, epochs)
delete_file_at(self, folder, name)
load_epochs(self, fname)
open_raw(self, fname)
pickleObjectToFile(self, picklable, path)
save_epoch(self, fpath, epoch, overwirte = False)
unpickle(self, fpath)
setEnvVariables()
"""
 
import mne

import os
import pickle
import csv
import shutil
import ConfigParser

import messageBox

from epochs import Epochs
from statistic import Statistic

    
def copy(self, original, target):
    """Copy the file at original to target.
    
    return True if no exceptions were raised, otherwise return
    the exception 
    """
    try:
        shutil.copyfile(original, target)
    
    # What type of error is expected here? This raises 'NameError:
    # Global name Error is not defined'.
    # except Error as e:
    #    return e
    
    except IOError as e:
        return e
    
    return True
    
def create_key_csv_evoked(self, evoked):
    """Create a list used for creating a csv file of key values in evoked.
    
    The file contains the
    epoch,  channel, min, min_time, max, max_time,
    half_max, half_max_time-, half_max_time+ and integral in that order.
    
    Keyword arguments:
    
    evoked -- An instance of evoked data.
    
    return a list of rows to write.
    """
    # TODO adjust into saving key values of averaged data.
    stat = Statistic()
    data = evoked.data
    rows = []
    # Create the first row with headings for the fields
    rows.append(['channel', 'min', 'min_time', 'max', 'max_time',
                 'half_max', 'half_max_time-', 'half_max_time+', 'integral'])
    
    # create the actual rows
    for i in range(len(data)):
        
        for j in range(len(data[i])):
            
            row = []
            
            row.append(evoked.ch_names[j])
            
            min, min_time = stat.find_minimum(data[i][j])
            row.append(min)
            row.append(evoked.times[min_time])
            
            max, max_time = stat.find_maximum(data[i][j])
            row.append(max)
            row.append(evoked.times[max_time])
            
            half_max, half_max_time_b, half_max_time_a = \
            stat.find_half_maximum(data[i][j])
            
            row.append(half_max)
            # If half_max_times are -1, the half_max value is not reached
            # inside the epoch window.
            if half_max_time_b == -1:
                row.append(None)
            else:
                row.append(evoked.times[half_max_time_b])
                
            if half_max_time_a == -1:
                row.append(None)
            else:
                row.append(evoked.times[half_max_time_a])
                
            integral = stat.integrate(data[i], half_max_time_b,
                                      half_max_time_a)
            
            row.append(integral)
            
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
        # TODO: using os.path.join assumes strings being used
        # when files consist QStrings
        # os.remove(os.path.join(folder, files))
        os.remove(folder + '/' + files)
    except OSError:
        self.messageBox = messageBox.AppForm()
        self.messageBox.labelException.\
        setText('Could not delete selected files.')
        self.messageBox.show()
    except TypeError:
        # If files is a list object instead of string.
        for file in files:
            try:
                # TODO: using os.path.join assumes strings being used
                # when files consist QStrings
                # os.remove(os.path.join(folder, file))
                os.remove(folder + '/' + file)
            except OSError as e:
                return False
    return True
    
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
    try:
        epochs = mne.read_epochs(os.path.join(folder, name))
    except Exception:
        try:
            epochs = mne.read_epochs(os.path.join(folder, name + '.fif'))
        except IOError:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.\
            setText('Reading from selected folder is not allowed.')
            self.messageBox.show()
            return epochs
    
    try:
        parameters = self.unpickle(os.path.join(folder, name + '.param'))
        
    except IOError:
        parameters = None
        return epochs, parameters
    # The events need to be converted back to QListWidgetItems.
    event_list = []
    event_dict = parameters['events']
    for key in event_dict:
        for event in event_dict[key]:
            event_tuple = (event, key)
            event_list.append(event_tuple)
    
    parameters['events'] = event_list
    return epochs, parameters
    
def load_evoked(self, folder, file):
    """Load evokeds to the list when mainWindow is initialized
    
    Keyword arguments:
    folder  -- the folder for loading evoked
    file -- the name of the fif-file containing evokeds.
    
    """
    split = os.path.split(file)
    name = os.path.splitext(split[1])[0]
    if name == '': return
    category = dict()
    evokeds = []
    i = 0
    # Couldn't find a way to check how many evoked datasets are in the
    # .fif file. So, after the setno gets list index out of range we get
    # an exception. This makes it hard to check if the data type is right,
    # since both 'index out of bound' and 'no evoked data found' raise
    # ValueError.
    try:
            while mne.fiff.Evoked(os.path.join(folder, file), setno=i) is not None:
                evoked = mne.fiff.Evoked(os.path.join(folder, file), setno=i)
                event_name = evoked.comment  # .split('_', 1)
                if i < 5:
                    category[event_name] = i + 1
                    i += 1
                    evokeds.append(evoked)
                    continue
                if i == 5:
                    category[event_name] = 8
                    i += 1
                    evokeds.append(evoked)
                    continue
                if i == 6:
                    category[event_name] = 16
                    i += 1
                    evokeds.append(evoked)
                    continue
                if i == 7:    
                    category[event_name] = 32
                    i += 1
                    evokeds.append(evoked)
                    continue
                
                # Current event ids have only 1, 2, 3, 4, 5, 8, 16 and 32.
                # This makes sure that Meggie won't stop working if more
                # than 8 evoked sets exist.
                if i >= 8:
                    warning = 'WARNING: There are more than 8 evoked' + \
                    ' sets in the evoked.fif file. This does not' + \
                    ' necessarily support all the functionality in' + \
                    ' Meggie. The evoked.fif files with more than 8' + \
                    ' datasets could not be loaded.'
                    self.messageBox = messageBox.AppForm()
                    self.messageBox.labelException.setText(warning)
                    self.messageBox.show()
                    return
                    """
                    # When visualizing evoked datasets the color set
                    # should be fixed for more than 8 datasets.
                    category[event_name] = i + 100
                    i += 1
                    evokeds.append(evoked)
                    continue
                    """
    except ValueError:
        try:
            if mne.fiff.Evoked(os.path.join(folder, file), setno=0) is not None:
        # if isinstance(mne.fiff.Evoked(folder + file, setno=0), mne.fiff.Evoked()):
                return evokeds, category
        except ValueError:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('File is not an evoked.fif file.')
            self.messageBox.show()
            return None, None
    
    return evokeds, category
        
def open_raw(self, fname, pre_load=True):
    """
    Opens a raw file.
    Keyword arguments:
    fname         -- A file to open
    pre_load      -- A boolean telling, whether to read the entire data
                     in the file.
    Raises an exception if the file cannot be opened.
    """
    # if os.path.isfile(fname):# and fname.endswith('fif'):
    try:
        return mne.io.Raw(fname, preload=pre_load)
        # self.raw = mne.io.RawFIFF(str(fname))
    except IOError:
        raise IOError('File does not exist or is not a raw-file')
    
    except OSError:
        raise OSError('You do not have permission to read the file.')
    
    except ValueError:
        raise ValueError('File is not a raw-file')
    
def pickleObjectToFile(self, picklable, fpath):
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
    
    
def unpickle(self, fpath):
    """Unpickle an object from a file at fpath.
    
    Keyword arguments:
    
    fpath -- the path to the pickled file.
    
    Return the unpickled object or None if unpickling failed.
    Raise an IOError if unpickling fails.
    """
    return pickle.load(open(fpath, 'rb'))
    
    
def save_epoch(self, fpath, epoch, overwrite=False):
    """Save epochs and the parameter values used to create them.
    
    The epochs are saved to fpath.fif. the parameter values are saved
    to fpath.param.
    
    Keyword arguments:
    
    fpath     -- The full path and base name of the files without suffix
    epoch     -- Epochs object
    overwrite -- A boolean telling whether existing files should be
                replaced. False by default. 
    """
    if os.path.exists(fpath + '.fif') and overwrite is False:
        return
    # First save the epochs
    raw = epoch._raw
    raw.save(fpath + '.fif')
    # Then save the parameters using pickle.
    parameters = epoch._params
    if parameters is None: return
    # toPyObject turns the dict keys into QStrings so convert them back to
    # strings.
    # parameters = dict((str(k), v) for k, v in parameters.iteritems())
    
    event_dict = {}
    event_list = parameters['events']
    for item in event_list:
        key = str(item[1])
        event = item[0]
        # Create an empty list for the new key
        if key not in event_dict:
            event_dict[key] = []
        event_dict[key].append(event)
    parameters['events'] = event_dict
    parameterFileName = str(fpath + '.param')
    self.pickle(parameters, parameterFileName)


def setEnvVariables():
    """
    Set various shell environment variables needed by MNE-C scripts.
    """
    if os.path.isfile('settings.cfg'):
        configp = ConfigParser.RawConfigParser()
        configp.read('settings.cfg')
        
        if configp.has_option('MNERoot', 'MNERootDir'):
            MNERootPath = configp.get('MNERoot', 'MNERootDir')
            os.environ['MNE_ROOT'] = MNERootPath


def readCSVFileToDictList(self, keynames, fpath, ndoculines):
    # TODO this is simple use of csv.DictReader, remove method
    """
    
    Read a CSV file to a list of dictionaries, one line at a time.
    Each line will be a separate dictionary in the returned list, 
    with keys taken from the keynames list, and values from the CSV file. 
    
    Keyword arguments:
    
    keynames -- list of key names meant to correspond with the CSV values.
                If and empty list, keys will simply be assigned names of
                integers, starting from 1.  
    
                Please note:   
    
                if the keynames list is not empty, the method requires that 
                the CVS file have exactly the len(keynames) number of values
                on each line, resulting in all dictionaries having explitly 
                named keys.
                
    fpath -- full path to CSV file.
    
    doculines -- number of non-CSV documentation lines at the beginning
                 of the file. Are skipped by default.
    
    Return list of dictionaries, None if was reading dictionaries was't
    successful
    
    Raise exception if all CVS lines don't conform to length of keynames.
    Raise IOError if the CVS file can't be read.
  
   
     
    try:
        with open(fpath, 'rb') as file to readfile:
            csvreaderFile=csv.DictReader(readfile)
            
            # Possibly skip the first lines, as they don't include actual
            # CSVdata.
            for i in range(ndoculines):
                next(csvreaderFile)
            
            # Read the rest of the file into a dictionary as
            # key-value pairs.
            
            return CSVdict           
                   
    except IOError:
        # In no dictionary is returned, the dialog just falls back to
        # default initial values.
        return None  
    
    

    # return list
      """

# def writeCSVFileFromDictList(self, keynames, fpath):
    
    
    
