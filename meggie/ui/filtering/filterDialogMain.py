# coding: latin1
'''
Created on Aug 20, 2013

@author: kpaliran
'''
import mne
from PyQt4 import QtCore,QtGui

from meggie.ui.filtering.filterDialogUi import Ui_DialogFilter
from meggie.ui.general import messageBoxes

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general.measurementInfo import MeasurementInfo

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

    def on_pushButtonPreview_clicked(self, checked=None):
        """
        Draws the preview.
        """
        if checked is None: return

        paramDict = self.get_filter_parameters()
        if paramDict.get('isEmpty') == True:
                message = 'Please select filter(s) to preview'
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
                return

        self.drawPreview()

    def drawPreview(self):
        """
        Shows the data (mne.raw.plot()) filtered with the given filters, but
        does not actually modify it. Also asks whether the previewed file
        should be saved over the working file, and saves if the user answers
        yes.
        """
        raw = self.caller.experiment.active_subject.working_file
        paramDict = self.get_filter_parameters()
        dataToFilter = raw._data
        info = raw.info

        samplerate = raw.info['sfreq']

        # Check if the filter frequency values are sane or not.
        if (self._validateFilterFreq(paramDict, samplerate) == False):
            return

        filteredData = None
        filteredData = self.caller.filter(dataToFilter, info, paramDict, 
                                          do_meanwhile=self.parent.update_ui)
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

            previewRaw.save(fname, overwrite=True)
            raw = mne.io.Raw(fname, preload=True)
            self.caller.update_experiment_working_file(fname, raw)

            self.parent._initialize_ui()

    def get_filter_parameters(self):
        """
        Gets the filtering parameters from the UI fields and performs
        rudimentary sanity checks on them.
        """
        dictionary = {}
        dictionary['isEmpty'] = True
        length = str(self.ui.doubleSpinBoxLength.value()) + 's'
        dictionary['length'] = length
        dictionary['trans_bw'] = self.ui.doubleSpinBoxTransBandwidth.value()
        dictionary['lowpass'] = self.ui.checkBoxLowpass.isChecked()
        if dictionary['lowpass']:
            dictionary['isEmpty'] = False
            dictionary['low_cutoff_freq'] = self.ui.\
                                       doubleSpinBoxLowpassCutoff.value()

        dictionary['highpass'] = self.ui.checkBoxHighpass.isChecked()
        if dictionary['highpass']:
            dictionary['isEmpty'] = False
            dictionary['high_cutoff_freq'] = self.ui.\
                                        doubleSpinBoxHighpassCutoff.value()

        dictionary['bandstop1'] = self.ui.checkBoxBandstop.isChecked()
        if dictionary['bandstop1']:
            dictionary['isEmpty'] = False
            dictionary['bandstop1_freq'] = self.ui.\
                                            doubleSpinBoxBandstopFreq.value()

        dictionary['bandstop2'] = self.ui.checkBoxBandstop2.isChecked()
        if dictionary['bandstop2']:
            dictionary['isEmpty'] = False

            dictionary['bandstop2_freq'] = self.ui.\
                                            doubleSpinBoxBandstopFreq2.value()

        dictionary['bandstop_bw'] = self.ui.doubleSpinBoxBandstopWidth.value()
        dictionary['bandstop_transbw'] = self.ui.doubleSpinBoxNotchTransBw.\
                                                                        value()
        length = str(self.ui.doubleSpinBoxBandStopLength.value()) + 's'
        dictionary['bandstop_length'] = length
        if dictionary.get('isEmpty') == True:
                message = 'Please select filter(s) to apply'
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
                return

        return dictionary

    def accept(self):
        """
        Get the parameters dictionary and relay it to caller.filter to
        actually do the filtering.
        """
        paramDict = self.get_filter_parameters()   
        raw = self.caller.experiment.active_subject.working_file
        info = raw.info

        # Check if the filter frequency values are sane or not.
        if (self._validateFilterFreq(paramDict, info['sfreq']) == False):
            return

        result = None
        result = self.caller.filter(raw, info, paramDict, 
                                    do_meanwhile=self.parent.update_ui)

        if result is not None:
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
        self.messageBox = messageBoxes.shortMessageBox(message)
        self.messageBox.show()
        return

    def _showLengthError(self, filterSource):
        """
        Show the error for wrong type of filter length string.

        Keyword arguments:

        filterSource     -- which filter UI box is the source of error.
        """
        message = 'Check filter length for ' + filterSource + \
        '. It should end with \'s\' or \'ms\''
        self.messageBox = messageBoxes.shortMessageBox(message)
        self.messageBox.show()
