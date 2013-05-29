'''
Created on Feb 27, 2013

@author: jaeilepp
'''
# -*- coding: latin-1 -*-
import mne
import pylab as pl
import os
import csv


def saveFile(param, path, fileName):
    """
    Method for saving a dictionary of parameters to a file.
    
    Keyword arguments:
    param    -- a dictionary of parameters 
    path     -- path of the file
    fileName -- name of the file
    """
    path += fileName
    print path
    writer = csv.writer(open(path, 'wb'))
    #f = open(path, 'w')
    for key, value in param.items():
        writer.writerow([key,value])
    
    
def loadFile(path,fileName):
    """Method for loading saved parameters to a dictionary.
    
    Keyword arguments:
    path     -- path of the file
    fileName -- name of the file
    """
    path += fileName
    reader = csv.reader(open(path, 'rb'))
    a = dict(x for x in reader)
    print a
    
    

fname = ('/home/jaeilepp/Downloads/MNE-sample-data/MEG/sample/' +
         'sample_audvis_raw.fif')
raw = mne.fiff.Raw(fname)

picks = mne.fiff.pick_types(raw.info, meg=False, eeg=False, stim=True,
                            eog=False, exclude=[])
#print picks
start, stop = raw.time_as_index([0, 15])
data, times = raw[picks, start:(stop + 1)]

triggers = []
x = data.T[0]
for i in range (0, len(data.T)):
    if data.T[i].any() != 0:
        if set(x) != set(data.T[i]):
            trigger = (times[i], data.T[i])
            triggers.append(trigger)
            x = data.T[i]
mydict = {'key':'value', 'k2':'v2', 'k3':'v4'}
saveFile(mydict, '/home/jaeilepp/', 'triggers.csv')
loadFile('/home/jaeilepp/', 'triggers.csv')

"""filename = 'triggers'
path = os.path.abspath("/home/jaeilepp/%s.log" % filename)
f = open(path, 'w+')
for line in triggers:
    str = "(%s,%s)" % line
    f.write(str)
    f.write("\n")
    #print str
f.close()
pl.plot(times,data.T)
pl.show()
"""
