'''
Created on 15.10.2014

@author: Kari Aliranta
'''

"""
Methods for writing and reading various command parameters to disk and from
disk. Needed in cased where deriving the parameters from files created with
those parameters is impossible, needlessly compilicated or resource-hungry.
"""

import csv
import os
    
    

def save_parameter_file(self, command, inputfilename, outputfilename,
                            operation, dic):
        """
        Saves the command and parameters related to creation of a certain
        output file to a separate parameter file in csv-format.
        
        An example of the structure of the resulting parameter file:
        
        jn_multimodal01_raw_sss.fif
        jn_multimodal01_raw_sss_ecg_proj.fif 
        mne.preprocessing.compute_proj_eog
        tmin,0.2
        tmax,0.5
        .
        .
        .  
        
        Keyword arguments:
        command          -- command (as string) used.
        inputfilename    -- name of the file the command with parameters
                            was executed on
        outputfilename   -- the resulting output file from the command.
        operation        -- operation the command represents. Used for
                            determining the parameter file name.
        dic              -- dictionary including commands.
        """
        paramfilename = os.path.join(self._workspace, self._experiment_name, 
                                     self._active_subject_name, operation + 
                                     '.param')
        
        with open(paramfilename, 'wb') as paramfullname:
            print 'writing param file'
            csvwriter = csv.writer(paramfullname)
            
            csvwriter.writerow([inputfilename])
            csvwriter.writerow([outputfilename])
            csvwriter.writerow([command])
            
            for key, value in dic.items():
                csvwriter.writerow([key, value])
          
                    
def parse_parameter_file(self, operation):
    """
    Reads the parameters from a single file matching the operation
    and returns the parameters as a dictionary.        
    Keyword arguments:
    operation    -- String that designates the operation. See Caller class
                    for operation names.
                    
    """

    # Reading parameter file.
    paramdirectory = os.path.join(self._workspace, self._experiment_name, 
                                  self._active_subject_name) 
    paramfilefullpath = os.path.join(paramdirectory, operation + '.param')

    try:
        with open(paramfilefullpath, 'rb') as paramfile:
            csvreader=csv.reader(paramfile)

            # skip the first three lines, as they don't include actual
            # info about parameters
            for i in range(3):
                next(csvreader)

            # Read the rest of the parameter file into a dictionary as
            # key-value pairs
            paramdict = dict(x for x in csvreader)
            return paramdict           
    except IOError:
        # In no dictionary is returned, the dialog just falls back to
        # default initial values.
        return None  
