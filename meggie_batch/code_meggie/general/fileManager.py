# coding: latin1
from pickle import UnpicklingError

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

A module for various file operations needed by Meggie.
"""
 
import mne

import os
import pickle
import shutil
import glob

# For copy_tree. Because shutil.copytree has restrictions regarding the
# destination directory (ie. it must not exist beforehand).
from distutils import dir_util

from xlrd import open_workbook
from xlwt import Workbook, XFStyle
import csv


import messageBoxes
from statistic import Statistic
    
    
def copy(original, target):
    """Copy the file at original to target.
    
    return True if no exceptions were raised, otherwise return
    the exception 
    """
    try:
        shutil.copyfile(original, target)
    
    except IOError as e:
        return e
    
    return True


def copy_recon_files(aSubject, sourceDirectory):
        """
        Copies mri and surf files from the given directory to under the active
        subject's reconFiles directory (after creating the said directory, 
        if need be).
        
        Keyword arguments:
        
        aSubject            -- currently active subject
        sourceDirectory     -- directory including the mri and surf file 
        
        Returns True if copying was successful, else returns False.
        
        """
        
        mriDir = os.path.join(sourceDirectory, 'mri')
        surfDir = os.path.join(sourceDirectory, 'surf')
        
        if not (os.path.isdir(mriDir) and os.path.isdir(surfDir)):
            message = "Reconstructed image directory should have both 'surf' " + \
             "and 'mri' directories in it."
            messageBox = messageBoxes.shortMessageBox(message)
            messageBox.exec_()   
            return False          
        
        activeSubject = aSubject
        
        reconDir = activeSubject._reconFiles_directory
        
        # Empty the destination directory first by removing it, then make it
        # again.
        if os.path.isdir(reconDir):
            dir_util.remove_tree(reconDir)
        
        activeSubject.create_reconFiles_directory()
        
        dst = activeSubject._reconFiles_directory
        
        try:
            print '\n Meggie: Copying recon files... \n'
            dir_util.copy_tree(sourceDirectory, dst)
            print '\n Meggie: Recon files copying complete! \n'
            return True
        except IOError:
            message = 'Could not copy files. Either the disk is full ' + \
            ' , you have no rights to read the directory or something weird' + \
            ' happened.'
            messageBox = messageBoxes.shortMessageBox(message)
            messageBox.exec_()   
            return False
    
    
def move_trans_file(subject, fModelName):
    """
    Copy the translated coordinated file from the subject root directory
    to the desired forward model directory. Should only be needed after creating
    a new forward model for the subject, and requires the directory to exist
    beforehand.
    
    Keyword arguments:
    
    subject       -- the subject whose coordinate file and forward model
                     are in question.
    fModelName    -- name of the forward model.
    
    """
    original = os.path.join(subject._subject_path, 'reconFiles-trans.fif')
    targetDirectory = os.path.join(subject._forwardModels_directory,
                               fModelName, 'reconFiles')
    
    try:
        shutil.copy(original, targetDirectory)
        os.remove(original)
    except IOError as e:
        return e
    
    return True
    
    
def remove_sourceAnalysis_files(aSubject):
    """
    Recursively removes contents of the source analysis directory.
    Used when copying new recon files invalidates the rest of the source
    analysis chain. 
    
    Keyword arguments:
    
    aSubject    -- currently active subject in the experiment 
    """
    
    # shutil.rmtree(directory, ignore_errors, onerror)
    

def create_fModel_directory(fmname, subject):
    """
    Create a directory for the final forward model (under the directory of the
    subject) and:
    
    - copy the whole bem directory to it. 
    - make symbolic links to subjects mri- and surf-directories to avoid 
    copying them around.
    - copy parameter files used to create the forward model to the directory.
    
    Keyword arguments:
    
    fmname        -- desired name for the forward model.
    subject       -- The subject (as an object) whose model while are to be
                     copied (probably always the active subject of the current
                     experiment).
    """
    
    fromCopyDirData = os.path.join(subject._reconFiles_directory, 'bem')
    fromCopyDirParams = subject._reconFiles_directory
    
    
    # If this is the first forward model, the forwardModels directory doesn't
    # exist yet.
    if not os.path.isdir(subject._forwardModels_directory):
        subject.create_forwardModels_directory()
    
    # Existence actually checked already by check_fModel_name via
    # forwardModelDialog. fmDirFinal is needed because mne.gui.coregistration
    # requires the directory name to be the same as the subject name.
    fmDir = os.path.join(subject._forwardModels_directory, fmname)
    fmDirFinal = os.path.join(fmDir, 'reconFiles')
    if not os.path.isdir(fmDir):
        os.mkdir(fmDir)
        os.mkdir(fmDirFinal)
    
    # Need to have and actual directory named bem for mne.gui.coregistration.
    # Symlinks below for same reason.
    toCopyDirData = os.path.join(fmDirFinal, 'bem')
    if not os.path.isdir(toCopyDirData):
        os.mkdir(toCopyDirData)
    
    try:
        dir_util.copy_tree(fromCopyDirData, toCopyDirData, preserve_symlinks=1)
        # Copy parameter files.
        pattern = os.path.join(fromCopyDirParams,'*.param')
    
        for f in glob.glob(pattern):
            shutil.copy(f, fmDirFinal)
        return True
    except Exception as e:
        os.rmdir(fmDir)
        message = 'There was a problem with copying forward model files. ' + \
                  'Please copy the following to your bug report: ' + str(e)
        messageBox = messageBoxes.shortMessageBox(message)
        messageBox.exec_()
        return False
    
    
    
    
    

def check_fModel_name(fmname, subject):
    """
    Checks whether a forward model name is already in use. If yes, return True,
    else return False.
    
    Keyword arguments:
    fmname         -- proposed forward model name
    subject        -- (the usually active) subject
    
    """
    proposedDir = os.path.join(subject._forwardModels_directory, fmname)
    if os.path.isdir(proposedDir):
        return True
    
    return False


def write_forward_model_parameters(fmname, subject, sspaceArgs=None, 
                                   wshedArgs = None, setupFModelArgs= None):
    """
    Writes the parameters used to create the forward model to the directory
    corresponding to.
    """
    
    targetDir = subject._reconFiles_directory
    
    sspaceArgsFile = os.path.join(targetDir, fmname, 
                                      'setupSourceSpace.param')
    wshedArgsFile = os.path.join(targetDir, fmname, 
                                     'wshed.param')
    setupFModelArgsFile = os.path.join(targetDir, fmname,
                                           'setupFModel.param')
       
    try:
        if sspaceArgs != None:
            pickleObjectToFile(sspaceArgs, sspaceArgsFile)
        
        if wshedArgs != None:
            pickleObjectToFile(wshedArgs, wshedArgsFile)
        
        if setupFModelArgs != None:
            pickleObjectToFile(setupFModelArgs, setupFModelArgsFile)
    except IOError:
        message = 'There was a problem with saving forward model parameters. ' + \
                  'You should not continue using the program before the ' + \
                  'problem is fixed.'
        messageBox = messageBoxes.shortMessageBox(message)
        messageBox.exec_()
           

def link_triang_files(subject):
    """
    Create symlinks to bem directory, linking them to surface triangulation
    files in watershed directory, as needed mne_setup_forward_model and
    mne.gui.coregistration.
    """
    
    bemDir = os.path.join(subject._reconFiles_directory, 'bem/')
    
    watershedDir = os.path.join(bemDir, 'watershed/')
    
    # Symlinks may already exist, no problem.
    try:
        os.symlink(os.path.join(watershedDir, 'reconFiles_brain_surface'), 
               os.path.join(bemDir, 'brain.surf'))
        os.symlink(os.path.join(watershedDir, 'reconFiles_inner_skull_surface'), 
               os.path.join(bemDir, 'inner_skull.surf'))
        os.symlink(os.path.join(watershedDir, 'reconFiles_outer_skull_surface'), 
               os.path.join(bemDir, 'outer_skull.surf'))
        os.symlink(os.path.join(watershedDir, 'reconFiles_outer_skin_surface'), 
               os.path.join(bemDir, 'outer_skin.surf'))
    except:
        pass
    

def create_key_csv_evoked(evoked):
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
    
    
def delete_file_at(folder, files):
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
        message = 'Could not delete selected files.'
        messageBox = messageBoxes.shortMessageBox(message)
        messageBox._exec()
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
    
    
def load_epochs(fname):
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
            message = 'Reading from selected folder is not allowed.'
            messageBox = messageBoxes.shortMessageBox(message)
            messageBox._exec()
            return epochs
    
    try:
        parameters = unpickle(os.path.join(folder, name + '.param'))
        
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
    
    
def load_evoked(folder, file):
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
                    message = 'WARNING: There are more than 8 evoked' + \
                    ' sets in the evoked.fif file. This does not' + \
                    ' necessarily support all the functionality in' + \
                    ' Meggie. The evoked.fif files with more than 8' + \
                    ' datasets could not be loaded.'
                    messageBox = messageBoxes.shortMessageBox(message)
                    messageBox._exec()
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
            message = 'File is not an evoked.fif file.'
            messageBox = messageBoxes.shortMessageBox(message)
            messageBox._exec()
            return None, None
    
    return evokeds, category
    
        
def open_raw(fname, pre_load=True):
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
    
    
def pickleObjectToFile(picklable, fpath):
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
    
    
def unpickle(fpath):
    """Unpickle an object from a file at fpath.
    
    Keyword arguments:
    
    fpath -- the path to the pickled file.
    
    Return the unpickled object. If there is an exception, raise it to
    allow the calling method to decide a what to do.
    """
    try:
        unpickledObject = pickle.load(open(fpath, 'rb'))
    except Exception:
        raise
    
    return unpickledObject
    
    
def save_epoch(fpath, epoch, overwrite=False):
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
    pickleObjectToFile(parameters, parameterFileName)


def read_surface_names_into_list(subject):
    """
    Reads the surface files from under the subject's surf directory and
    returns their names as list. Meant to be used by populating surface combo-
    box in forwardModelDialog (which in turn allows the user to select the 
    surface to be used by mne_setup_source_space).
    
    No exception checking, the existence of surface files is assumed to be
    checked by the calling method.
    
    Keyword arguments:
    subject     -- subjects whose surface files need listing (almost always the
                   active subject at the current experiment, but doesn't have to
                   be).

    Returns a list of surface names.
    """
    
    surfDir = os.path.join(subject._reconFiles_directory, 'surf/')
    surfNameList = []
    
    # Filenames from surf directory to list
    for (dirpath, dirnames, filenames) in os.walk(surfDir):
        surfNameList.extend(filenames)
        break
    
    # Remove 'lh.' and 'rh.' prefixes from surf filenames, ignore reg files.
    finalSurfNameList = []
    for surfName in surfNameList:
        if surfName[-4:] == '.reg':
            continue
        finalSurfNameList.append(surfName[3:])
    
    # To set and back to remove duplicates.
    return list(set(finalSurfNameList))


def write_events(events, subject):
        """
        Saves the events into an Excel file (.xls). 
        Keyword arguments:
        events           -- Events to be saved
        subject          -- subject (as object) whose events are in question 
                            (usually active subject)
        """
        wbs = Workbook()
        ws = wbs.add_sheet('Events')
        styleNumber = XFStyle()
        styleNumber.num_format_str = 'general'
        sizex = events.shape[0]
        sizey = events.shape[1]
                
        path_to_save = subject._subject_path
        
        # Saves events to csv file for easier modification with text editors.
        csv_file = open(os.path.join(path_to_save, 'events.csv'), 'w')
        csv_file_writer = csv.writer(csv_file)
        csv_file_writer.writerows(events)
        csv_file.close()

        for i in range(sizex):
            for j in range(sizey):
                ws.write(i, j, events[i][j], styleNumber)
        wbs.save(os.path.join(path_to_save, 'events.xls'))
        #TODO: muuta filename kayttajan maarittelyn mukaiseksi


def read_events(filename):
    """
    Reads the events from a chosen excel file.
    Keyword arguments:
    filename      -- File to read from.
    """
    wbr = open_workbook(filename)
    sheet = wbr.sheet_by_index(0)
    return sheet
    
    
    
