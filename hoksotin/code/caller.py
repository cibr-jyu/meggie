# coding: latin1
"""
Created on Apr 11, 2013

@author: Jaakko Leppäkangas
"""
import subprocess
import os

class Caller(object):
    """
    Class for calling third party software
    """
    def __init__(self):
        pass
    
    def call_mne_browse_raw(self, filename):
        """
        Opens mne_browse_raw with the given file as a parameter
        Keyword arguments:
        filename      -- file to open mne_browse_raw with
        """
        os.environ['MNE_ROOT'] = '/usr/local/bin/MNE-2.7.0-3106-Linux-x86_64'
        subprocess.Popen('$MNE_ROOT', shell=True)
        proc = subprocess.Popen('$MNE_ROOT/bin/mne_browse_raw --raw ' + filename, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()
        print "the program return code was %d" % retval