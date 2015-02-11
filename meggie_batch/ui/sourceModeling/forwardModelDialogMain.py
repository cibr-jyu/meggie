'''
Created on 30.6.2014

@author: Kari Aliranta
'''


from PyQt4 import QtGui

from forwardModelDialogUi import Ui_forwardModelDialog
import messageBoxes
import string

import fileManager
import re

class ForwardModelDialog(QtGui.QDialog):
    """
    Class containing the logic for forwardModelDialog. It collects parameter
    values for creating forward models and passes them to ***
    
    TODO passes to something that coordinates the MVC structure related
    to views related to forward modeling and saving new forward models to disk.
    
    TODO Removing forward models from disk and view coordination is handled by
    ***
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_forwardModelDialog()
        self.ui.setupUi(self)
        self.populateSurfaceNamesCombobox()
    
    
    def populateSurfaceNamesCombobox(self):
        """
        Use file manager to find all files under the surf-directory
        and populate the self.ui.comboBoxSurfaceName with them. Set white as
        default, like mne_setup_source_space suggests.
        """
        activeSubject = self.parent.experiment._active_subject
        surfaceNames = fileManager.read_surface_names_into_list(activeSubject)
        self.ui.comboBoxSurfaceName.addItems(surfaceNames)
        
        whiteIndex = self.ui.comboBoxSurfaceName.findText('white')
        self.ui.comboBoxSurfaceName.setCurrentIndex(whiteIndex)
        
    
    def on_comboBoxSurfaceDecimMethod_currentIndexChanged(self):
        """
        To disable and enable input fields for spacing and ico as needed.
        """
        if self.ui.comboBoxSurfaceDecimMethod.currentText() == \
        'traditional (default)':
            self.ui.spinBoxSurfaceDecimValue.setEnabled(False)
            self.ui.labelIcoValue.setEnabled(False)
            self.ui.labelSpacing.setEnabled(True)
            self.ui.spinBoxSpacing.setEnabled(True)
        else:
            self.ui.spinBoxSurfaceDecimValue.setEnabled(True)
            self.ui.labelIcoValue.setEnabled(True)
            self.ui.labelSpacing.setEnabled(False)
            self.ui.spinBoxSpacing.setEnabled(False)
            
    
    def collectParametersIntoDictionary(self):
        """
        Collects the parameters from the ui fields of the dialog and returns
        them in a dictionary of dictionaries, one dictionary for each phase
        of forward model creation. 
        """
        setupSourceSpaceDict = {}
        waterShedDict = {}
        setupFmodelDict =  {}
         
        setupSourceSpaceDict['spacing'] = str(self.ui.spinBoxSpacing.value())
        setupSourceSpaceDict['surfaceDecimMethod'] = self.ui.comboBoxSurfaceDecimMethod.currentText()
        setupSourceSpaceDict['surfaceDecimValue'] = str(self.ui.spinBoxSurfaceDecimValue.value())
        setupSourceSpaceDict['surfaceName'] = self.ui.comboBoxSurfaceName.currentText()
        
        if self.ui.buttonGroupCorticalPatchStats.checkedButton() == \
        self.ui.radioButtonPatchStatYes:
            setupSourceSpaceDict['computeCorticalStats'] = True
        else: setupSourceSpaceDict['computeCorticalStats'] = False
            
        if self.ui.buttonGroupAtlas.checkedButton() == \
        self.ui.radioButtonAtlasYes:
            waterShedDict['useAtlas'] = True
        else: waterShedDict['useAtlas'] = False                    
        
        setupFmodelDict['triangFilesIco'] = str(self.ui.spinBoxTriangFilesIco.value())
        setupFmodelDict['compartModel'] = self.ui.comboBoxCompartmentModel.currentText()
        
        if self.ui.buttonGroupNosol.checkedButton == \
        self.ui.radioButtonNoSolYes:
            setupFmodelDict['nosol'] = True
        else: setupFmodelDict['nosol'] = False
        
        setupFmodelDict['innerShift'] = str(self.ui.spinBoxInnerShift.value())
        setupFmodelDict['outerShift'] = str(self.ui.spinBoxOuterShift.value())
        setupFmodelDict['skullShift'] = str(self.ui.spinBoxSkullShift.value())
        setupFmodelDict['brainc'] = str(self.ui.doubleSpinBoxBrainConductivity.value())
        setupFmodelDict['skullc'] = str(self.ui.doubleSpinBoxSkullConductivity.value())
        setupFmodelDict['scalpc'] = str(self.ui.doubleSpinBoxScalpConductivity.value())
        
        fmname = self.ui.lineEditFModelName.text()
        finalDict = {'fmname': fmname, 'sspaceArgs': setupSourceSpaceDict,
                     'wsshedArgs': waterShedDict, 
                     'sfmodelArgs': setupFmodelDict}
        return finalDict
        
        
    def accept(self):
        """
        Gets the arguments from the gui and passes them to caller for forward
        model creation. 
        """
        
        fmdict = self.collectParametersIntoDictionary()
        fmname = fmdict['fmname']
        
        activeSubject = self.parent._experiment._active_subject
        if fileManager.check_fModel_name(fmname, activeSubject):
            message = 'That forward model name is already in use. Please ' + \
            'select another.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return
        
        # A bit of checking for stupidities in naming to avoid conflicts
        # with directories created by MNE scripts.
        if string.lower(fmdict['fmname']) == ('mri' or 'bem' or 'surf'):
            message = "'mri', 'bem' and 'surf' are not acceptable fmodel names" + \
                      " (they get mixed up with directory names created by MNE)."
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return
        
        # Forward model should have a name.
        if (fmdict['fmname']) == '':
            message = "Please give a name to your forward model."
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return
        
        # Name should only use alphanumeric and underscores.
        if not re.match('^[\w+$]' ,fmdict['fmname']): 
            message = 'Please only use alphabets, numbers and underscores in ' + \
            'forward model name'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return
        
        # To help the user with the weird ico parameter.
        if (fmdict['sspaceArgs']['surfaceDecimMethod']) != 'traditional (default)' and \
        fmdict['sspaceArgs']['surfaceDecimValue'] == '0':
            message = 'You need to use a nonzero ico parameter if you ' + \
            'to use a nontraditional cortical surface decimation method.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.exec_()
            return
        
        # FIXME: use try-except here
        if self.parent.caller.create_forward_model(fmdict) == False:
            return
        
        self.close()