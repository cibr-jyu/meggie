# coding: utf-8
'''
Created on Aug 20, 2013

@author: kpaliran
'''

import traceback

import mne
from PyQt4 import QtCore,QtGui

from meggie.ui.filtering.filterDialogUi import Ui_DialogFilter
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general.measurementInfo import MeasurementInfo

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox

from copy import deepcopy

class FilterDialog(QtGui.QDialog):
    """
    Class containing the logic for filterDialog. It collects the parameters
    needed for filtering and shows the preview for the filter if required.
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogFilter()
        self.ui.setupUi(self)
        
        self.filterParameterDictionary = None
        self.caller = Caller.Instance()
        self.batching_widget = BatchingWidget(self, self.ui.scrollAreaWidgetContents)

    def on_pushButtonPreview_clicked(self, checked=None):
        """
        Draws the preview.
        """
        if checked is None: return

        paramDict = self.collect_parameter_values()()
        if paramDict.get('isEmpty') == True:
            message = 'Please select filter(s) to preview'
            messagebox(self.parent, message)
            return

        self.drawPreview()

    def drawPreview(self):
        """
        Shows the data (mne.raw.plot()) filtered with the given filters, but
        does not actually modify it. Also asks whether the previewed file
        should be saved over the working file, and saves if the user answers
        yes.
        """
        raw = self.caller.experiment.active_subject.get_working_file()
        paramDict = self.collect_parameter_values()()
        dataToFilter = raw._data
        info = raw.info

        samplerate = raw.info['sfreq']

        # Check if the filter frequency values are sane or not.
        if (self._validateFilterFreq(paramDict, samplerate) == False):
            return

        filteredData = None

        try:
            filteredData = self.caller.filter(dataToFilter, info, paramDict, 
                                              do_meanwhile=self.parent.update_ui)
        except Exception as e:
            exc_messagebox(self.parent, e)

        if filteredData is None:
            return

        previewRaw = deepcopy(raw)
        previewRaw._data = filteredData

        # This should really block, but doesn't.
        previewRaw.plot(block=True)                       

        reply = QtGui.QMessageBox.question(self, 'Apply filters?',
                    'Apply the previewed filters to the working file?',
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.Yes)

        if reply == QtGui.QMessageBox.Yes:
            fname = previewRaw.info.get('filename')
            # This actually saves the file over current working file,
            # because the previewRaw filename is the same as that of raw
            # file it is copied from.

            # Update the data file with new filter values.
            if 'lowpass' in paramDict and paramDict['lowpass'] == True:
                previewRaw.info['lowpass'] = paramDict['low_cutoff_freq']

            if ( 'highpass' in paramDict and paramDict['highpass'] == True ):
                previewRaw.info['highpass'] = paramDict['high_cutoff_freq']

            fileManager.save_raw(self.caller.experiment, previewRaw, fname, overwrite=True)       
            self.caller.experiment.active_subject.set_working_file(previewRaw)

            self.parent._initialize_ui()


    def accept(self):
        """
        Get the parameters dictionary and relay it to caller.filter to
        actually do the filtering.
        """
        subject = self.caller.experiment.active_subject
        parameter_values = self.collect_parameter_values()
        info = subject.get_working_file().info
        
        self.batching_widget.data[subject.subject_name] = parameter_values
        
        if any([
            self._validateFilterFreq(parameter_values, info['sfreq']) == False,
            not self.filter(subject)
        ]):
            self.batching_widget.failed_subjects.append(subject)
        
        self.batching_widget.cleanup()
        self.close()
        self.parent._initialize_ui()
        
    def acceptBatch(self):
        
        recently_active_subject = self.caller.experiment.active_subject.subject_name
        subject_names = []
        for i in range(self.batching_widget.ui.listWidgetSubjects.count()):
            item = self.batching_widget.ui.listWidgetSubjects.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                subject_names.append(item.text())
        
        # In case of batch process:
        # 1. Calculation is first done for the active subject to prevent an
        #    excessive reading of a raw file.
        if recently_active_subject in subject_names:

            params = self.batching_widget.data[recently_active_subject]
            info = self.caller.experiment.active_subject.get_working_file().info
            subject = self.caller.experiment.active_subject
            # Check if the filter frequency values are sane or not.
            
            if any([
                self._validateFilterFreq(params, info['sfreq']) == False,
                not self.filter(subject)
            ]):
                self.batching_widget.failed_subjects.append(subject)
        
        # 2. Calculation is done for the rest of the subjects.
        for name, subject in self.caller.experiment.subjects.items():
            if name in subject_names:
                if name == recently_active_subject:
                    continue
                
                self.caller.activate_subject(name)

                params = self.batching_widget.data[name]
                info = subject.get_working_file().info
                
                if any([
                    self._validateFilterFreq(params, info['sfreq']) == False,
                    not self.filter(subject)
                ]):
                    self.batching_widget.failed_subjects.append(subject)        

                
        self.caller.activate_subject(recently_active_subject)
        
        self.batching_widget.cleanup()
        self.parent._initialize_ui()
        self.close()
    
    def _validateFilterFreq(self, paramDict, samplerate):
        """
        Checks the validity of filter cutoff frequency values.
        """
        if 'lowpass' in paramDict and paramDict['lowpass'] == True:
            if ( paramDict['low_cutoff_freq'] > samplerate/2 ):
                self._show_filter_freq_error(samplerate)

        if ( 'highpass' in paramDict and paramDict['highpass'] == True ):
            if ( paramDict['high_cutoff_freq'] > samplerate/2 ):
                self._show_filter_freq_error(samplerate)

    def _show_filter_freq_error(self, samplerate):
        message = 'Cutoff frequencies should be lower than samplerate/2 ' + \
                    '(' + 'current samplerate is ' + str(samplerate) + ' Hz)'
        messagebox(self.parent, message)
        return

    def _showLengthError(self, filterSource):
        """
        Show the error for wrong type of filter length string.

        Keyword arguments:

        filterSource     -- which filter UI box is the source of error.
        """
        message = 'Check filter length for ' + filterSource + \
        '. It should end with \'s\' or \'ms\''
        messagebox(self.parent, message)
        
    def selection_changed(self, subject_name, params_dict):
        subject = self.caller.experiment.subjects[subject_name]

	if len(params_dict) > 0:
	    dic = params_dict  
	else:
	    dic = self.get_default_values()
	self.ui.doubleSpinBoxLength.setProperty("value", dic.get('length'))
	self.ui.doubleSpinBoxTransBandwidth.setProperty("value", dic.get('trans_bw'))
	
	if dic.get('lowpass'):
	    self.ui.doubleSpinBoxLowpassCutoff.setProperty("value", dic.get('low_cutoff_freq'))
	else:
	    self.ui.doubleSpinBoxLowpassCutoff.setProperty("value", dic.get('low_cutoff_freq_false'))
	self.ui.checkBoxLowpass.setChecked(dic.get('lowpass'))
	
	self.ui.checkBoxHighpass.setChecked(dic.get('highpass'))
	if dic.get('highpass'):
	    self.ui.doubleSpinBoxHighpassCutoff.setProperty("value", dic.get('high_cutoff_freq'))
	else:
	    self.ui.doubleSpinBoxHighpassCutoff.setProperty("value", dic.get('high_cutoff_freq_false'))
	
	self.ui.checkBoxBandstop.setChecked(dic.get('bandstop1'))
	if dic.get('bandstop1'):
	    self.ui.doubleSpinBoxBandstopFreq.setProperty("value", dic.get('bandstop1_freq'))
	else:
	    self.ui.doubleSpinBoxBandstopFreq.setProperty("value", dic.get('bandstop1_freq_false'))
	
	self.ui.checkBoxBandstop2.setChecked(dic.get('bandstop2'))
	if dic.get('bandstop2'):
	    self.ui.doubleSpinBoxBandstopFreq2.setProperty("value", dic.get('bandstop2_freq'))
	else:
	    self.ui.doubleSpinBoxBandstopFreq2.setProperty("value", dic.get('bandstop2_freq_false'))
	
	self.ui.doubleSpinBoxBandstopWidth.setProperty("value", dic.get('bandstop_bw'))
	self.ui.doubleSpinBoxNotchTransBw.setProperty("value", dic.get('bandstop_transbw'))
	self.ui.doubleSpinBoxBandStopLength.setProperty("value", dic.get('bandstop_length'))
	self.update()
    
    def get_default_values(self):
        """Sets default values for dialog."""
        return {
            'length': 10.00,
            'trans_bw': 0.500, 
            'lowpass': True,
            'low_cutoff_freq': 40.000,
            'highpass': True,
            'high_cutoff_freq': 1.000,
            'bandstop1': True,
            'bandstop1_freq': 50.000,
            'bandstop2': False,
            'bandstop2_freq': 100.000,
            'bandstop_bw': 1.000,
            'bandstop_transbw': 0.500,
            'bandstop_length': 10.00
        }

        
    def collect_parameter_values(self):
        """
        Gets the filtering parameters from the UI fields and performs
        rudimentary sanity checks on them.
        """
        dictionary = {}
        dictionary['isEmpty'] = True
        length = str(self.ui.doubleSpinBoxLength.value())# + 's'
        dictionary['length'] = length
        dictionary['trans_bw'] = self.ui.doubleSpinBoxTransBandwidth.value()
        dictionary['lowpass'] = self.ui.checkBoxLowpass.isChecked()
        if dictionary['lowpass']:
            dictionary['isEmpty'] = False
            dictionary['low_cutoff_freq'] = self.ui.\
                                       doubleSpinBoxLowpassCutoff.value()
        else:
            #Only UI needs the value: value set to different key
            dictionary['low_cutoff_freq_false'] = self.ui.doubleSpinBoxLowpassCutoff.value()


        dictionary['highpass'] = self.ui.checkBoxHighpass.isChecked()
        if dictionary['highpass']:
            dictionary['isEmpty'] = False
            dictionary['high_cutoff_freq'] = self.ui.\
                                        doubleSpinBoxHighpassCutoff.value()
        else:
            dictionary['high_cutoff_freq_false'] = self.ui.doubleSpinBoxHighpassCutoff.value()
        dictionary['bandstop1'] = self.ui.checkBoxBandstop.isChecked()
        if dictionary['bandstop1']:
            dictionary['isEmpty'] = False
            dictionary['bandstop1_freq'] = self.ui.\
                                            doubleSpinBoxBandstopFreq.value()
        else:
            dictionary['bandstop1_freq_false'] = self.ui.doubleSpinBoxBandstopFreq.value()


        dictionary['bandstop2'] = self.ui.checkBoxBandstop2.isChecked()
        if dictionary['bandstop2']:
            dictionary['isEmpty'] = False
            dictionary['bandstop2_freq'] = self.ui.\
                                            doubleSpinBoxBandstopFreq2.value()
        else:
            dictionary['bandstop2_freq_false'] = self.ui.doubleSpinBoxBandstopFreq2.value()

        dictionary['bandstop_bw'] = self.ui.doubleSpinBoxBandstopWidth.value()
        dictionary['bandstop_transbw'] = self.ui.doubleSpinBoxNotchTransBw.\
                                                                        value()
        a = self.ui.doubleSpinBoxBandStopLength.value()
        length = str(self.ui.doubleSpinBoxBandStopLength.value())# + 's'
        dictionary['bandstop_length'] = length
        if dictionary.get('isEmpty') == True:
            message = 'Please select filter(s) to apply'
            messagebox(self.parent, message)
            return

        return dictionary
    
    def filter(self, subject):
        """Calls caller class for filtering the given
        subject and passes errors to accept method.

        Keyword arguments:
        subject               -- Subject object
        """
        params = self.batching_widget.data[subject.subject_name]
        #MNE wants the lengths to be human-readable values
        params['length'] = params['length'] + 's'
        params['bandstop_length'] = params['bandstop_length'] + 's'
        
        try:
            result = self.caller.filter(params, subject,
                do_meanwhile=self.parent.update_ui)
            if not result == 0:
                return False
        except Exception as e:
            return False
        return True
