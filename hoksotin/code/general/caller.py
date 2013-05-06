# coding: latin1
"""
Created on Apr 11, 2013

@author: Jaakko Leppäkangas
"""
import subprocess
import os
import glob

from xlwt import *
from xlrd import open_workbook,cellname

import mne
from mne.time_frequency import induced_power
from mne.layouts import read_layout
from mne.viz import plot_topo_power, plot_topo_phase_lock


import numpy as np
import pylab as pl
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

class Caller(object):
    """
    Class for calling third party software
    """
    def __init__(self, parent):
        
       
        self.parent = parent
    
    def call_mne_browse_raw(self, filename):
        """
        Opens mne_browse_raw with the given file as a parameter
        Keyword arguments:
        filename      -- file to open mne_browse_raw with
        """
        #os.environ['MNE_ROOT'] = '/usr/local/bin/MNE-2.7.0-3106-Linux-x86_64' #TODO Remove
        try:
            proc = subprocess.Popen('$MNE_ROOT/bin/mne_browse_raw --cd ' +
                                    filename.rsplit('/', 1)[0] + ' --raw ' +
                                    filename,
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        except:
            pass #TODO error handling
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()
        print "the program return code was %d" % retval
        
    def call_maxfilter(self, dic, custom):
        """
        Performs maxfiltering with the given parameters.
        Keyword arguments:
        dic           -- Dictionary of parameters
        custom        -- Additional parameters as a string
        """
        #if '$NEUROMAG_ROOT' == '':
        if os.environ.get('NEUROMAG_ROOT') is None:
            os.environ['NEUROMAG_ROOT'] = '/neuro'
        bs = '$NEUROMAG_ROOT/bin/util/maxfilter '
        for i in range(len(dic)):
            bs += dic.keys()[i] + ' ' + str(dic.values()[i]) + ' '
        # Add user defined parameters from the "custom" tab
        bs += custom
        print bs
        proc = subprocess.Popen(bs, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()      
        
        print "the program return code was %d" % retval
        
        outputfile = dic.get('-o')
        self.update_experiment_working_file(outputfile)
        
        """ 
        # Write parameter file
        self.experiment. \
        save_parameter_file('maxfilter', \
                            raw, , dic)
        """
        
    def call_ecg_ssp(self, dic):
        """
        Creates ECG projections using ssp for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        """
        raw_in = dic.get('i')
        tmin = dic.get('tmin')
        tmax = dic.get('tmax')
        event_id = dic.get('event-id')
        ecg_low_freq = dic.get('ecg-l-freq')
        ecg_high_freq = dic.get('ecg-h-freq')
        grad = dic.get('n-grad')
        mag = dic.get('n-mag')
        eeg = dic.get('n-eeg')
        filter_low = dic.get('l-freq')
        filter_high = dic.get('h-freq')
        
        rej_grad = dic.get('rej-grad')
        rej_mag = dic.get('rej-mag')
        rej_eeg = dic.get('rej-eeg')
        rej_eog = dic.get('rej-eog')
        
        reject = dict(grad=1e-13 * float(rej_grad),
                  mag=1e-15 * float(rej_mag),
                  eeg=1e-6 * float(rej_eeg),
                  eog=1e-6 * float(rej_eog))
        qrs_threshold = dic.get('qrs')
        flat = None
        bads = [] #TODO: Check how the whole bads-thing is supposed to work.
        
        start = dic.get('tstart')
        taps = dic.get('filtersize')
        njobs = dic.get('n-jobs')
        eeg_proj = dic.get('avg-ref')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        preload = True #TODO File
        ch_name = dic.get('ch_name')
        
        if raw_in.info.get('filename').endswith('_raw.fif') or \
        raw_in.info.get('filename').endswith('-raw.fif'):
            prefix = raw_in.info.get('filename')[:-8]
        else:
            prefix = raw_in.info.get('filename')[:-4]
        
        ecg_event_fname = prefix + '_ecg-eve.fif'
        
        if comp_ssp:
            ecg_proj_fname = prefix + '_ecg_avg_proj.fif'
        else:
            ecg_proj_fname = prefix + '_ecg_proj.fif'
        
        #raw = mne.fiff.Raw(raw_in, preload=preload)
        
        projs, events = mne.preprocessing.compute_proj_ecg(raw_in, None,
                            tmin, tmax, grad, mag, eeg,
                            filter_low, filter_high, comp_ssp, taps,
                            njobs, ch_name, reject, flat,
                            bads, eeg_proj, excl_ssp, event_id,
                            ecg_low_freq, ecg_high_freq, start, qrs_threshold)
        #raw_in.close()
        
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)
        
        print "Writing ECG projections in %s" % ecg_proj_fname
        mne.write_proj(ecg_proj_fname, projs)
        
        print "Writing ECG events in %s" % ecg_event_fname
        mne.write_events(ecg_event_fname, events)
        
        # Write parameter file
        self.parent.experiment.\
        save_parameter_file('mne.preprocessing.compute_proj_ecg',
                            raw_in.info.get('filename'), ecg_proj_fname, dic)
        
    def call_eog_ssp(self, dic):
        """
        Creates EOG projections using ssp for given data.
        Keyword arguments:
        dic           -- dictionary of parameters including the MEG-data.
        """
        #os.environ['MNE_ROOT'] = '/usr/local/bin/MNE-2.7.0-3106-Linux-x86_64' #TODO Remove
        
        # TODO not the actual path to the needed script (the needed script
        # is an extra script in mne-python)
        # TODO use SSP-projections from a a different file?
        raw_in = dic.get('i')
        tmin = dic.get('tmin')
        tmax = dic.get('tmax')
        event_id = dic.get('event-id')
        eog_low_freq = dic.get('eog-l-freq')
        eog_high_freq = dic.get('eog-h-freq')
        grad = dic.get('n-grad')
        mag = dic.get('n-mag')
        eeg = dic.get('n-eeg')
        filter_low = dic.get('l-freq')
        filter_high = dic.get('h-freq')
        
        rej_grad = dic.get('rej-grad')
        rej_mag = dic.get('rej-mag')
        rej_eeg = dic.get('rej-eeg')
        rej_eog = dic.get('rej-eog')
        
        flat = None
        bads = dic.get('bads') #TODO: Check how the whole bads-thing is supposed to work.
        if bads is None:
            bads = []
        start = dic.get('tstart')
        taps = dic.get('filtersize')
        njobs = dic.get('n-jobs')
        eeg_proj = dic.get('avg-ref')
        excl_ssp = dic.get('no-proj')
        comp_ssp = dic.get('average')
        preload = True #TODO File
        reject = dict(grad=1e-13 * float(rej_grad), mag=1e-15 * float(rej_mag),
                      eeg=1e-6 * float(rej_eeg), eog=1e-6 * float(rej_eog))
        
        if (raw_in.info.get('filename').endswith('_raw.fif') 
        or raw_in.info.get('filename').endswith('-raw.fif')):
            prefix = raw_in.info.get('filename')[:-8]
        else:
            prefix = raw_in.info.get('filename')[:-4]
            
        eog_event_fname = prefix + '_eog-eve.fif'
        
        if comp_ssp:
            eog_proj_fname = prefix + '_eog_avg_proj.fif'
        else:
            eog_proj_fname = prefix + '_eog_proj.fif'
            
        #raw = mne.fiff.Raw(raw_in, preload=preload)
        
        projs, events = mne.preprocessing.compute_proj_eog(raw_in, None,
                            tmin, tmax, grad, mag, eeg,
                            filter_low, filter_high, comp_ssp, taps,
                            njobs, reject, flat, bads,
                            eeg_proj, excl_ssp, event_id,
                            eog_low_freq, eog_high_freq, start)
            
        #raw.close()
        
        #TODO Reading a file
        if isinstance(preload, basestring) and os.path.exists(preload):
            os.remove(preload)
        
        print "Writing EOG projections in %s" % eog_proj_fname
        mne.write_proj(eog_proj_fname, projs)
        
        print "Writing EOG events in %s" % eog_event_fname
        mne.write_events(eog_event_fname, events)
        
        # Write parameter file
        self.parent.experiment.save_parameter_file
        ('mne.preprocessing.compute_proj_eog', raw_in.info.get('filename'),
          eog_proj_fname, dic)
        
        #self.experiment.update_state(EOGcomputed, True)
        
    def apply_ecg(self, raw, directory):
        """
        Applies ECG projections for MEG-data.
        
        Keyword arguments:
        raw           -- Data to apply to
        directory     -- Directory of the projection file
        """
        
        """
        If there already is a file with eog projections applied on it, apply
        ecg projections on this file instead of current.
        """
        if len(filter(os.path.isfile, 
                      glob.glob(directory + '*-eog_applied.fif'))) > 0:
            fname = glob.glob(directory + '*-eog_applied.fif')[0]
        else:
            fname = raw.info.get('filename')
        proj_file = filter(os.path.isfile,
                           glob.glob(directory + '*_ecg_proj.fif'))
        #Checks if there is exactly one projection file
        if len(proj_file) == 1:
            proj = mne.read_proj(proj_file[0])
            raw.add_proj(proj)
            appliedfilename = fname[:-4] + '-ecg_applied.fif'
            raw.save(appliedfilename)
            raw = mne.fiff.Raw(appliedfilename, preload=True)
            
        self.update_experiment_working_file(appliedfilename)
        
    def apply_eog(self, raw, directory):
        """
        Applies EOG projections for MEG-data.
        
        Keyword arguments:
        raw           -- Data to apply to
        directory     -- Directory of the projection file
        """
        if len(filter(os.path.isfile, 
                      glob.glob(directory + '*-ecg_applied.fif'))) > 0:
            fname = glob.glob(directory + '*-ecg_applied.fif')[0]
        else:
            fname = raw.info.get('filename')
        proj_file = filter(os.path.isfile,
                           glob.glob(directory + '*_eog_proj.fif'))
        #Checks if there is exactly one projection file
        if len(proj_file) == 1:
            proj = mne.read_proj(proj_file[0])
            raw.add_proj(proj)
            appliedfilename = fname[:-4] + '-eog_applied.fif'
            raw.save(appliedfilename)
            raw = mne.fiff.Raw(appliedfilename, preload=True)
        self.update_experiment_working_file(appliedfilename)
    
    def TFR(self, raw, epochs, ch_index, minfreq, maxfreq):
        evoked = epochs.average()
        data = epochs.get_data()
        times = 1e3 * epochs.times #s to ms
        evoked_data = evoked.data * 1e13 #TODO: check whether mag or grad (units fT / cm or...)
        
        data = data[:, ch_index:(ch_index+1), :]
        evoked_data = evoked_data[ch_index:(ch_index+1), :]
        
        #Find intervals for given frequency band
        frequencies = np.arange(minfreq, maxfreq, int((maxfreq-minfreq) / 7))
        
        n_cycles = frequencies / float(len(frequencies) - 1)
        #n_cycles = frequencies / float(15)
        Fs = raw.info['sfreq']
        decim = 3
        power, phase_lock = induced_power(data, Fs=Fs,
                                          frequencies=frequencies,
                                          n_cycles=n_cycles, n_jobs=1,
                                          use_fft=False, decim=decim,
                                          zero_mean=True)
        
        # baseline corrections with ratio
        power /= np.mean(power[:, :, times[::decim] < 0], axis=2)[:, :, None]
        pl.clf()
        pl.subplots_adjust(0.1, 0.08, 0.96, 0.94, 0.2, 0.63)
        pl.subplot(3, 1, 1)
        pl.plot(times, evoked_data.T)
        pl.title('Evoked response (%s)' % evoked.ch_names[ch_index])
        pl.xlabel('time (ms)')
        pl.ylabel('Magnetic Field (fT/cm)')
        pl.xlim(times[0], times[-1])
        pl.ylim(-150, 300)
        
        pl.subplot(3, 1, 2)
        pl.imshow(20 * np.log10(power[0]), extent=[times[0], times[-1],
                                                   frequencies[0],
                                                   frequencies[-1]],
                  aspect='auto', origin='lower')
        pl.xlabel('Time (s)')
        pl.ylabel('Frequency (Hz)')
        pl.title('Induced power (%s)' % evoked.ch_names[ch_index])
        pl.colorbar()
        
        pl.subplot(3, 1, 3)
        pl.imshow(phase_lock[0], extent=[times[0], times[-1],
                                         frequencies[0], frequencies[-1]],
                  aspect='auto', origin='lower')
        pl.xlabel('Time (s)')
        pl.ylabel('Frequency (Hz)')
        pl.title('Phase-lock (%s)' % evoked.ch_names[ch_index])
        pl.colorbar()
        pl.show()
        
        
    def TFR_topology(self, raw, epochs, reptype, minfreq, maxfreq, decim, mode,  
                     blstart, blend):
        evoked = epochs.average()
        data = epochs.get_data()
        times = 1e3 * epochs.times #s to ms
        #evoked_data = evoked.data * 1e13 #TODO: check whether mag or grad (units fT / cm or...)
        
        #data = data[:, ch_index:(ch_index+1), :]
        #evoked_data = evoked_data[ch_index:(ch_index+1), :]
        
        #Find intervals for given frequency band
        frequencies = np.arange(minfreq, maxfreq, int((maxfreq-minfreq) / 7))
        
        n_cycles = frequencies / float(len(frequencies) - 1)
        #n_cycles = frequencies / float(15)
        Fs = raw.info['sfreq']
        decim = 3
        power, phase_lock = induced_power(data, Fs=Fs,
                                          frequencies=frequencies,
                                          n_cycles=n_cycles, n_jobs=3,
                                          use_fft=False, decim=decim,
                                          zero_mean=True)
        
        layout = read_layout('Vectorview-all')
        baseline = (blstart, blend)  # set the baseline for induced power
        #mode = 'ratio'  # set mode for baseline rescaling
        
        if ( reptype == 'induced' ):
            title='TFR topology: ' + 'Induced power'
            fig = plot_topo_power(epochs, power, frequencies, layout,
                            baseline=baseline, mode=mode, decim=decim, 
                            vmin=0., vmax=14, title=title)
            canvas = FigureCanvasAgg(fig)
            
            pl.show()
            #pl.clf()
            
        else: 
            title = 'TFR topology: ' + 'Phase locking'
            plot_topo_phase_lock(epochs, phase_lock, frequencies, layout,
                     baseline=baseline, mode=mode, decim=decim, title=title)
            pl.show()
        
        
    def update_experiment_working_file(self, fname):
        """
        Changes the current working file for the experiment the caller relates
        to.
        """
        self.parent.experiment.working_file = fname        

    def write_events(self, events):
        """
        Saves the events in an excel file (.xls).
        
        Keyword arguments:
        events           -- Events to save
        """
        wbs = Workbook()
        ws = wbs.add_sheet('Events')
        styleNumber = XFStyle()
        styleNumber.num_format_str = 'general'
        sizex = events.shape[0]
        sizey = events.shape[1]
                
        for i in range(sizex):
            for j in range(sizey):
                ws.write(i, j, events[i][j], styleNumber)
        
        path_to_save = self.parent.experiment.subject_directory
        wbs.save(path_to_save + '/events.xls') #TODO: muuta filename kayttajan maarittelyn mukaiseksi

    def read_events(self, file):
        """
        Reads the events from a chosen excel file.
        """
        #path_to_read = self.parent.experiment.subject_directory
        #wbr = open_workbook(path_to_read + 'events.xls')
        wbr = open_workbook(file)
        sheet = wbr.sheet_by_index(0)
        return sheet
        """
        for row_index in range(sheet.nrows):
            for col_index in range(sheet.ncols):
                #print cellname(row_index,col_index),'-',
                #print sheet.cell(row_index,col_index).value
                item = QtGui.QListWidgetItem(self.parent.ui.lineEditName.text()
                                             + ' ' + str(sheet.cell(row_index,col_index).value)
                                             + ', ' + str(sheet.cell(row_index,col_index+2).value))
                item.setData(32, row_index)
                item.setData(33, self.parent.ui.lineEditName.text())
                self.parent.ui.listWidgetEvents.addItem(item)
            self.parent.ui.listWidgetEvents.setCurrentItem(item)
        """
