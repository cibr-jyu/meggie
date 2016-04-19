# coding: utf-8
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
import re
import sys
import json

from os.path import isfile, join

from shutil import copyfile

# For copy_tree. Because shutil.copytree has restrictions regarding the
# destination directory (ie. it must not exist beforehand).
from distutils import dir_util

from xlrd import open_workbook
from xlwt import Workbook, XFStyle
import csv

from meggie.code_meggie.general.statistic import Statistic
from meggie.code_meggie.general.wrapper import wrap_mne_call

    
def copy_recon_files(activeSubject, sourceDirectory):
        """
        Copies mri and surf files from the given directory to under the active
        subject's reconFiles directory (after creating the said directory, 
        if need be).
        
        Keyword arguments:
        
        activeSubject            -- currently active subject
        sourceDirectory     -- directory including the mri and surf file 
        
        Returns True if copying was successful, else returns False.
        
        """         
        reconDir = activeSubject.reconFiles_directory
        
        # Empty the destination directory first by removing it, then make it
        # again.
        if os.path.isdir(reconDir):
            dir_util.remove_tree(reconDir)
        
        dst = activeSubject.reconFiles_directory
        
        try:
            print '\n Meggie: Copying recon files... \n'
            dir_util.copy_tree(sourceDirectory, dst)
            print '\n Meggie: Recon files copying complete! \n'
        except IOError: raise
    
    
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
    except IOError: raise
    
    
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
    subject       -- The subject (as an object) whose model files are to be
                     copied (probably always the active subject of the current
                     experiment).
    """
    
    fromCopyDirData = os.path.join(subject._reconFiles_directory, 'bem')
    fromCopyDirParams = subject._reconFiles_directory
    
    
    # Existence actually checked already by check_fModel_name via
    # forwardModelDialog. fmDirFinal is needed because mne.gui.coregistration
    # requires the directory name to be the same as the subject name.
    fmDir = os.path.join(subject._forwardModels_directory, fmname)
    fmDirFinal = os.path.join(fmDir, 'reconFiles')
    if not os.path.isdir(fmDir):
        os.mkdir(fmDir)
        os.mkdir(fmDirFinal)
    
    # Need to have an actual directory named bem for mne.gui.coregistration.
    # Symlinks preserved below for same reason.
    toCopyDirData = os.path.join(fmDirFinal, 'bem')
    if not os.path.isdir(toCopyDirData):
        os.mkdir(toCopyDirData)
    
    try:
        # Can return if previous directory doesn't exist.
        if os.path.isdir(fromCopyDirData):
            dir_util.copy_tree(fromCopyDirData, toCopyDirData,
                               preserve_symlinks=1)
        else: return
        
        # Copy parameter files.
        pattern = os.path.join(fromCopyDirParams,'*.param')
    
        for f in glob.glob(pattern):
            shutil.copy(f, fmDirFinal)
    except Exception:
        shutil.rmtree(fmDir)
        raise
    
    
def remove_fModel_directory(fmname, subject):
    """
    Remove an fModel directory named fmname from the directory of the subject.
    
    Keyword arguments:
    
    fmname        -- name of the forward model to be removed.
    subject       -- The subject (as an object) whose model directory and
                     files under it are to be removed.
    """
    fmDir = os.path.join(subject._forwardModels_directory, fmname)
    
    try:
        shutil.rmtree(fmDir)
    except IOError: raise


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
    corresponding to the said forward model. Saves the previous parameter files
    in the forward model directory root.
    """
    
    fmdir = subject._forwardModels_directory
    targetDir = os.path.join(subject._forwardModels_directory, fmname)
    
    sspaceArgsFile = os.path.join(fmdir, 'setupSourceSpace.param')
    wshedArgsFile = os.path.join(fmdir, 'wshed.param')
    setupFModelArgsFile = os.path.join(fmdir, 'setupFModel.param')
       
    try:
        if sspaceArgs != None:
            pickleObjectToFile(sspaceArgs, sspaceArgsFile)
        
        if wshedArgs != None:
            pickleObjectToFile(wshedArgs, wshedArgsFile)
        
        if setupFModelArgs != None:
            pickleObjectToFile(setupFModelArgs, setupFModelArgsFile)
            
        # Copy from the root to the actual directory
        shutil.copy(sspaceArgsFile, targetDir)
        shutil.copy(wshedArgsFile, targetDir)
        shutil.copy(setupFModelArgsFile, targetDir)     
    except Exception: raise
    
           
def convertFModelParamDictToCmdlineParamTuple(fmdict):
        """
        Converts the parameters input in the dialog into valid command line
        argument strings for various MNE-C-scripts (mne_setup_source_space, 
        mne_watershed_bem, mne_setup_forward_model) used in forward model
        creation.
        
        Keyword arguments:
        
        pdict        -- dictionary of three dictionaries, created by 
                        ForwardModelDialogMain.
        
        Returns a tuple of lists with suitable arguments for commandline tools.
        Looks like this:
        (mne_setup_source_space_argumentList, mne_watershed_bem_argumentList, 
        mne_setup_forward_model_argumentList) 
        """
        
        # Arguments for source space setup
        if fmdict['sspaceArgs']['surfaceDecimMethod'] == 'traditional (default)':
            sDecimIcoArg = []
        else: sDecimIcoArg = ['--ico', fmdict['sspaceArgs']['surfaceDecimValue']]
        
        if fmdict['sspaceArgs']['computeCorticalStats'] == True:
            cpsArg = ['--cps']
        else: cpsArg = []
        
        spacingArg = ['--spacing', fmdict['sspaceArgs']['spacing']]
        surfaceArg = ['--surface', fmdict['sspaceArgs']['surfaceName']]
        
        setupSourceSpaceArgs = spacingArg + surfaceArg + sDecimIcoArg + cpsArg
        
        # Arguments for BEM model meshes
        if fmdict['wsshedArgs']['useAtlas'] == True:
            waterShedArgs = ['--atlas']
        else: waterShedArgs = []
        
        # Arguments for BEM model setup
        surfArg = ['--surf']
        bemIcoArg = ['--ico', fmdict['sfmodelArgs']['triangFilesIco']]
        
        if fmdict['sfmodelArgs']['compartModel'] == 'three layer':
            braincArg = fmdict['sfmodelArgs']['brainc']
            skullcArg = fmdict['sfmodelArgs']['skullc']
            scalpcArg = fmdict['sfmodelArgs']['scalpc']
            homogArg = ['']
        else:
            braincArg = ['']
            skullcArg = ['']
            scalpcArg = ['']
            homogArg = ['--homog']

        if fmdict['sfmodelArgs']['nosol'] == True:
            nosolArg = ['--nosol']
        else: nosolArg = ['']
        
        innerShiftArg = ['--innerShift', fmdict['sfmodelArgs']['innerShift']] 
        outerShiftArg = ['--outerShift', fmdict['sfmodelArgs']['outerShift']] 
        skullShiftArg = ['--outerShift', fmdict['sfmodelArgs']['skullShift']] 
        
        setupFModelArgs = homogArg + surfArg + bemIcoArg + braincArg + \
                          skullcArg + scalpcArg + nosolArg + innerShiftArg + \
                          outerShiftArg + skullShiftArg
        
        return (setupSourceSpaceArgs, waterShedArgs, setupFModelArgs)


def write_forward_solution_parameters(fmdir, fsdict):
    """
    Writes (pickles) the forward solution parameters to a file.
    
    Keyword arguments:
    fmdir    -- directory to which the parameter file should be pickled (should
                be forward models directory).
    fsdict   -- dictionary of parameters to pickle.
    
    """
    fsparamFile = os.path.join(fmdir, 'fSolution.param')
    
    try:
        pickleObjectToFile(fsdict, fsparamFile)
    except Exception: raise    


def remove_files_with_regex(directory, pattern):
    """
    Removes, from the given directory, files with a given regex pattern in
    their names.
    
    Keyword arguments:
    directory    -- directory to search the files for.
    pattern      -- regex pattern to match.
    """
    try:
        for f in os.listdir(directory):
            if re.search(pattern, f):
                os.remove(os.path.join(directory, f))
    except IOError: raise


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
    except Exception:
        pass
    
    
def delete_file_at(folder, files):
    """Delete files from a folder.
    
    Keyword arguments:
    
    folder -- The location of the deleted files
    files  -- The files to be deleted. Can be a single file or a list of
              files in the same folder.
    """
    if isinstance(files, list):
        for f in files:
            os.remove(os.path.join(folder, f))
        return
    os.remove(os.path.join(folder, files))
    
def load_epochs(fname, load_object=False):
    """Load epochs from a folder.
    
    Keyword arguments:
    fname         -- the name of the fif-file containing epochs.
    load_object   -- boolean to indicate whether to load epoch objects to
                     memory.
    
    # TODO: fix this.
    Return a tuple with an Epochs instance and 
    """
    try:
        epochs = mne.read_epochs(fname)
    except IOError:
        raise Exception('Reading epochs failed.')
    return epochs

def load_evoked(fname):
    """Load evokeds to the list when mainWindow is initialized

    Keyword arguments:
    fName -- the name of the fif-file containing evokeds.
    """
    try:
        evokeds = mne.read_evokeds(fname)
    except IOError:
        raise IOError('Reading evokeds failed.')
    return evokeds

def load_powers(subject):
    """
    Loads power files from the subject folder.
    Returns a list of AverageTFR names.
    """
    powers = list()
    path = os.path.join(subject.subject_path, 'TFR')
    if not os.path.exists(path):
        return list()
    files = os.listdir(path)
    for fname in files:
        if fname.endswith('.h5'):
            powers.append(fname)
    return powers

def open_raw(fname, pre_load=True):
    """
    Opens a raw file.
    Keyword arguments:
    fname         -- A file to open
    pre_load      -- A boolean telling, whether to read the entire data
                     in the file.
    Raises an exception if the file cannot be opened.
    """
    try:
        return mne.io.Raw(fname, preload=pre_load, allow_maxshield=True)
    except IOError as e:
        raise IOError('File does not exist or is not a raw-file.' + str(e))
    except OSError as e:
        raise OSError('You do not have permission to read the file.' + str(e))
    except ValueError as e:
        raise ValueError('File is not a raw-file.' + str(e))

def save_raw(experiment, raw, fname, overwrite=True):
    wrap_mne_call(experiment, raw.save, fname, overwrite=True)
    

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
    with open(fpath, 'rb') as f:
        try:
            unpickledObject = pickle.load(f)
        except ImportError:
            from pkg_resources import resource_filename
            sys.path.insert(0, resource_filename('meggie', '/'))
            unpickledObject = pickle.load(f)
            sys.path.pop(0)

    return unpickledObject


def save_epoch(epoch, overwrite=False):
    """Save epochs and the parameter values used to create them.
    
    The epochs are saved to fpath.fif. the parameter values are saved
    to fpath.param.
    
    Keyword arguments:
    
    fpath     -- The full path and base name of the files without suffix
    epoch     -- mne.Epochs object
    params    -- Parameter of the epochs.
    overwrite -- A boolean telling whether existing files should be
                 replaced. False by default. 
    """
    if os.path.exists(epoch.path) and overwrite is False:
        return
    # First save the epochs
    epoch.raw.save(epoch.path)

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

    
def get_layouts():
    """
    Finds the layout files from MNE_ROOT.
    Returns a list of strings of found files. 
    """
    import pkg_resources
    
    files = []
    
    try:
        path_meggie = pkg_resources.resource_filename('meggie', 'data/layouts')

        files.extend([f for f in os.listdir(path_meggie)])
    except:
        pass        
    
    try:    
        path = pkg_resources.resource_filename('mne', 'channels/data/layouts')
        
        files.extend([f for f in os.listdir(path) 
                      if isfile(join(path,f)) and f.endswith('.lout')])
    except:
        pass
    
    return files


def load_tfr(fname):
    """
    Function for loading AverageTFR from a file.
    Returns AverageTFR object.
    """
    return mne.time_frequency.tfr.read_tfrs(fname)[0]

def create_folders(paths):
    for path in paths:
        os.makedirs(path)

def save_subject(subject, path):
    try:
        create_folders([
            subject.subject_path,
            subject.epochs_directory,
            subject.evokeds_directory,
            subject.source_analysis_directory,
            subject.forwardModels_directory,
            subject.reconFiles_directory,
            subject.stc_directory
        ])
    except OSError as e:
        raise OSError("Couldn't create all the necessary folders. "
                      "Do you have the necessary permissions?")
    
    copyfile(path, subject.working_file_path)
    
