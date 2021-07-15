"""Contains functions that are used in the dynamic location and creation 
of tabs and datatypes. Can be used both internally and externally.
"""

import os
import json
import pkg_resources
import importlib
import logging

from PyQt5 import QtWidgets

from meggie.utilities.uid import generate_uid
from meggie.utilities.messaging import exc_messagebox


def find_all_plugins():
    """Looks for plugins (installed packages with name meggie_*), that
    can contain tabs or datatypes"""
    plugins = []
    package_keys = [dist.key.replace('-', '_') for dist 
                    in pkg_resources.working_set]
    for key in package_keys:
        try:
            if key.startswith('meggie_'):
                # check that there exists configuration.json
                if not os.path.exists(
                        pkg_resources.resource_filename(key, 'configuration.json')):
                    continue
                plugins.append(key)
        except Exception as exc:
            logging.getLogger('ui_logger').exception('')
    return plugins


def find_all_sources():
    """Returns all packages where to look for tabs / datatypes.
    """
    return ['meggie'] + find_all_plugins()


def find_all_action_specs():
    """Finds all valid tabs from the core and plugins.
    """
    action_specs = {}

    found_keys = []

    sources = find_all_sources()
    for source in sources:
        action_path = pkg_resources.resource_filename(source, 'actions')
        if not os.path.exists(action_path):
            continue
        for package in os.listdir(action_path):
            config_path = os.path.join(action_path, package, 'configuration.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    if config:
                        if config['id'] in found_keys:
                            raise Exception('Action with the same id found ' + 
                                            'in multiple packages')
                        else:
                            found_keys.append(config['id'])
                        action_specs[config['id']] = source, package, config

    # add possibly missing fields
    for source, package, action_spec in action_specs.values():

        if 'id' not in action_spec:
            raise Exception('Every action specification must have id.')

        if 'name' not in action_spec:
            action_spec['name'] = action_spec['id']
        
    return action_specs


def construct_tab(tab_spec, action_specs, parent):
    """Constructs analysis tab dynamically. Returns a QDialog
    that can be used within a QTabDialog of the main window.

    Parameters
    ----------
    tab_spec : dict
        The specification of the tab read to a dict
    action_specs : dict
        Specifications of the actions stored in a dict
    parent : instance of main window
        The main window, is passed to the handlers in the ui.py.

    Returns
    -------
    instance of QDialog
        The constructed tab than can be added to
        main window.
    """

    class DynamicTab(QtWidgets.QDialog):
        """ Class defining a tab.
        
        Parameters
        ----------
        parent : instance of main window
            The main window, is passed to the handlers in actions.
        """
        def __init__(self, parent):
            QtWidgets.QDialog.__init__(self)
            self.parent = parent
            self.tab_spec = tab_spec
            self.action_specs = action_specs

            # first create basic layout
            self.gridLayoutContainer = QtWidgets.QGridLayout(self)

            self.gridLayoutRoot = QtWidgets.QGridLayout()
            self.gridLayoutContainer.addLayout(self.gridLayoutRoot, 0, 0, 1, 1)

            if self.tab_spec['outputs']:
                self.groupBoxOutputs = QtWidgets.QGroupBox(self)
                self.groupBoxOutputs.setTitle('Outputs')
                self.gridLayoutOutputs = QtWidgets.QGridLayout(
                    self.groupBoxOutputs)

            if self.tab_spec['output_actions']:
                self.groupBoxOutputActions = QtWidgets.QGroupBox(self)
                self.groupBoxOutputActions.setTitle('Actions')
                self.gridLayoutOutputActions = QtWidgets.QGridLayout(
                    self.groupBoxOutputActions)

            if self.tab_spec['input_actions']:
                self.groupBoxInputActions = QtWidgets.QGroupBox(self)
                self.groupBoxInputActions.setTitle('Actions')
                self.gridLayoutInputActions = QtWidgets.QGridLayout(
                    self.groupBoxInputActions)

            if self.tab_spec['inputs']:
                self.groupBoxInputs = QtWidgets.QGroupBox(self)
                self.groupBoxInputs.setTitle('Inputs')
                self.gridLayoutInputs = QtWidgets.QGridLayout(
                    self.groupBoxInputs)

            if self.tab_spec['info']:
                self.groupBoxInfo = QtWidgets.QGroupBox(self)
                self.groupBoxInfo.setTitle('Info')
                self.gridLayoutInfo = QtWidgets.QGridLayout(self.groupBoxInfo)

            # add the (empty) input lists
            for idx, input_name in enumerate(self.tab_spec['inputs']):

                title = input_name.capitalize()

                groupBoxInputElement = QtWidgets.QGroupBox(self.groupBoxInputs)
                groupBoxInputElement.setTitle(title)
                gridLayoutInputElement = QtWidgets.QGridLayout(
                    groupBoxInputElement)
                listWidgetInputElement = QtWidgets.QListWidget(
                    groupBoxInputElement)

                listWidgetInputElement.setSelectionMode(
                    QtWidgets.QAbstractItemView.ExtendedSelection)

                gridLayoutInputElement.addWidget(
                    listWidgetInputElement, idx, 0, 1, 1)
                self.gridLayoutInputs.addWidget(groupBoxInputElement)

                setattr(self, 'groupBoxInputElement_' + str(idx + 1),
                        groupBoxInputElement)
                setattr(self, 'gridLayoutInputElement_' + str(idx + 1),
                        gridLayoutInputElement)
                setattr(self, 'listWidgetInputElement_' + str(idx + 1),
                        listWidgetInputElement)

            # add the (empty) output lists
            for idx, output_name in enumerate(self.tab_spec['outputs']):

                title = output_name.capitalize()

                groupBoxOutputElement = QtWidgets.QGroupBox(
                    self.groupBoxOutputs)
                groupBoxOutputElement.setTitle(title)
                gridLayoutOutputElement = QtWidgets.QGridLayout(
                    groupBoxOutputElement)
                listWidgetOutputElement = QtWidgets.QListWidget(
                    groupBoxOutputElement)

                listWidgetOutputElement.setSelectionMode(
                    QtWidgets.QAbstractItemView.ExtendedSelection)

                gridLayoutOutputElement.addWidget(
                    listWidgetOutputElement, idx, 0, 1, 1)
                self.gridLayoutOutputs.addWidget(groupBoxOutputElement)

                setattr(self, 'groupBoxOutputElement_' + str(idx + 1),
                        groupBoxOutputElement)
                setattr(self, 'gridLayoutOutputElement_' + str(idx + 1),
                        gridLayoutOutputElement)
                setattr(self, 'listWidgetOutputElement_' + str(idx + 1),
                        listWidgetOutputElement)

            # add input action buttons
            for idx, action_name in enumerate(self.tab_spec['input_actions']):

                action_spec = self.action_specs[action_name][2]
                title = action_spec['name']
                
                pushButtonInputActionElement = QtWidgets.QPushButton(
                    self.groupBoxInputActions)
                pushButtonInputActionElement.setText(title)
                self.gridLayoutInputActions.addWidget(
                    pushButtonInputActionElement, idx, 0, 1, 1)
                setattr(self, 'pushButtonInputActionElement_' + str(idx + 1),
                        pushButtonInputActionElement)

            if getattr(self, 'gridLayoutInputActions', None):
                spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)
                self.gridLayoutInputActions.addItem(spacer, idx + 1, 0, 1, 1)

            # add action buttons
            for idx, action_name in enumerate(self.tab_spec['output_actions']):

                action_spec = self.action_specs[action_name][2]
                title = action_spec['name']
 
                pushButtonOutputActionElement = QtWidgets.QPushButton(
                    self.groupBoxOutputActions)
                pushButtonOutputActionElement.setText(title)
                self.gridLayoutOutputActions.addWidget(
                    pushButtonOutputActionElement, idx, 0, 1, 1)
                setattr(self, 'pushButtonOutputActionElement_' + str(idx + 1),
                        pushButtonOutputActionElement)

            if getattr(self, 'gridLayoutOutputActions', None):
                spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)
                self.gridLayoutOutputActions.addItem(spacer, idx + 1, 0, 1, 1)

            # add info text boxes
            for idx, info_name in enumerate(self.tab_spec['info']):

                action_spec = self.action_specs[info_name][2]
                title = action_spec['name']

                groupBoxInfoElement = QtWidgets.QGroupBox(self.groupBoxInfo)
                groupBoxInfoElement.setTitle(title)
                gridLayoutInfoElement = QtWidgets.QGridLayout(
                    groupBoxInfoElement)
                plainTextEditInfoElement = QtWidgets.QTextBrowser(
                    groupBoxInfoElement)

                gridLayoutInfoElement.addWidget(
                    plainTextEditInfoElement, idx, 0, 1, 1)
                self.gridLayoutInfo.addWidget(groupBoxInfoElement)

                setattr(self, 'groupBoxInfoElement_' + str(idx + 1),
                        groupBoxInfoElement)
                setattr(self, 'gridLayoutInfoElement_' + str(idx + 1),
                        gridLayoutInfoElement)
                setattr(self, 'plainTextEditInfoElement_' + str(idx + 1),
                        plainTextEditInfoElement)

            # lay out inputs, outputs, actions and info elements
            # in a nice way to a grid
            if self.tab_spec['inputs'] and not self.tab_spec['input_actions']:
                self.gridLayoutRoot.addWidget(self.groupBoxInputs, 0, 0, 2, 1)
            elif self.tab_spec['inputs']:
                self.gridLayoutRoot.addWidget(self.groupBoxInputs, 0, 0, 1, 1)

            if self.tab_spec['outputs'] and not self.tab_spec['output_actions']:
                self.gridLayoutRoot.addWidget(self.groupBoxOutputs, 0, 1, 2, 1)
            elif self.tab_spec['outputs']:
                self.gridLayoutRoot.addWidget(self.groupBoxOutputs, 0, 1, 1, 1)

            if self.tab_spec['input_actions'] and not self.tab_spec['inputs']:
                self.gridLayoutRoot.addWidget(
                    self.groupBoxInputActions, 0, 0, 2, 1)
            elif self.tab_spec['input_actions']:
                self.gridLayoutRoot.addWidget(
                    self.groupBoxInputActions, 1, 0, 1, 1)

            if self.tab_spec['output_actions'] and not self.tab_spec['outputs']:
                self.gridLayoutRoot.addWidget(self.groupBoxOutputActions, 0, 1, 2, 1)
            elif self.tab_spec['output_actions']:
                self.gridLayoutRoot.addWidget(self.groupBoxOutputActions, 1, 1, 1, 1)

            if self.tab_spec['info']:
                self.gridLayoutRoot.addWidget(self.groupBoxInfo, 0, 2, 2, 1)

            # add spacers to bottom and right to keep the window concise
            spacerItemVertical = QtWidgets.QSpacerItem(
                20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayoutContainer.addItem(spacerItemVertical, 1, 0, 1, 1)
            spacerItemHorizontal = QtWidgets.QSpacerItem(
                10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.gridLayoutContainer.addItem(spacerItemHorizontal, 0, 1, 1, 1)

            # add handlers for list selection changed -> info updates
            def connect_to_handler(list_element, info_element, info_name):

                source, package, action_spec = self.action_specs[info_name]
                module = importlib.import_module(
                    '.'.join([source, 'actions', package]))
                entry = action_spec['entry']

                handler = getattr(module, entry)

                def handler_wrapper():
                    experiment = self.parent.experiment
                    if not experiment:
                        return
                    subject = experiment.active_subject
                    if not subject:
                        return

                    data = self._get_data()

                    try:
                        info_content = handler(experiment, data, 
                                               parent, action_spec).run()
                        info_element.setPlainText(info_content)
                    except Exception as exc:
                        exc_messagebox(self, exc)

                list_element.itemSelectionChanged.connect(handler_wrapper)

            for idx, info_name in enumerate(self.tab_spec['info']):
                info_element = getattr(self, 'plainTextEditInfoElement_' +
                                       str(idx + 1))

                for idx, input_name in enumerate(self.tab_spec['inputs']):

                    input_element = getattr(
                        self, 'listWidgetInputElement_' + str(idx + 1))
                    connect_to_handler(input_element, info_element, info_name)

                for idx, output_name in enumerate(self.tab_spec['outputs']):

                    output_element = getattr(
                        self, 'listWidgetOutputElement_' + str(idx + 1))
                    connect_to_handler(output_element, info_element, info_name)

            # add button handlers
            def connect_to_handler(button, name):

                source, package, action_spec = self.action_specs[name]
                module = importlib.import_module(
                    '.'.join([source, 'actions', package]))
                entry = action_spec['entry']

                handler = getattr(module, entry)

                def handler_wrapper(checked):
                    experiment = self.parent.experiment
                    if not experiment:
                        return

                    subject = experiment.active_subject
                    if not subject:
                        return

                    data = self._get_data()

                    try:
                        handler(experiment, data, parent, action_spec).run()
                    except Exception as exc:
                        exc_messagebox(self, exc)

                button.clicked.connect(handler_wrapper)

            for idx, action_name in enumerate(self.tab_spec['input_actions']):
                action_element = getattr(
                    self, 'pushButtonInputActionElement_' + str(idx + 1))
                connect_to_handler(action_element, action_name)

            for idx, action_name in enumerate(self.tab_spec['output_actions']):
                action_element = getattr(
                    self, 'pushButtonOutputActionElement_' + str(idx + 1))
                connect_to_handler(action_element, action_name)
 

        def _get_data(self):
            """Returns data from input and output lists.
            """
            data = {'inputs': {},
                    'outputs': {}}

            inputs = []
            for idx, name in enumerate(self.tab_spec['inputs']):
                ui_element = getattr(
                    self, 'listWidgetInputElement_' + str(idx + 1))
                try:
                    selected_items = [item.text()
                                      for item in ui_element.selectedItems()]
                except BaseException:
                    continue

                data['inputs'][name] = selected_items

            for idx, name in enumerate(self.tab_spec['outputs']):
                ui_element = getattr(
                    self, 'listWidgetOutputElement_' + str(idx + 1))
                try:
                    selected_items = [item.text() for item in
                                      ui_element.selectedItems()]
                except BaseException:
                    continue

                data['outputs'][name] = selected_items

            return data

        def initialize_ui(self):
            """Updates (empties and refills) ui contents when called.
            """
            experiment = self.parent.experiment
            if not experiment:
                return

            subject = experiment.active_subject

            # fill input lists with contents
            for idx, input_name in enumerate(self.tab_spec['inputs']):
                ui_element = getattr(
                    self, 'listWidgetInputElement_' + str(idx + 1))

                ui_element.clear()

                if not subject:
                    continue

                data = getattr(subject, input_name, None)
                if not data:
                    continue

                for key in sorted(list(data.keys())):
                    ui_element.addItem(key)

            # fill output lists with contents
            for idx, output_name in enumerate(
                    self.tab_spec['outputs']):
                ui_element = getattr(
                    self, 'listWidgetOutputElement_' + str(idx + 1))

                ui_element.clear()

                if not subject:
                    continue

                data = getattr(subject, output_name, None)
                if not data:
                    continue

                for key in sorted(list(data.keys())):
                    ui_element.addItem(key)

            # allow to fill info element already here.
            # there are also handlers to update info element
            # on list selection changes
            for idx, info_name in enumerate(self.tab_spec['info']):

                ui_element = getattr(
                    self, 'plainTextEditInfoElement_' + str(idx + 1))

                source, package, action_spec = self.action_specs[info_name]
                module = importlib.import_module(
                    '.'.join([source, 'actions', package]))
                entry = action_spec['entry']
                handler = getattr(module, entry)

                try:
                    info_content = handler(experiment, None, 
                                           self.parent, action_spec).run()
                    ui_element.setPlainText(info_content)
                except Exception as exc:
                    exc_messagebox(self, exc)


        @property
        def name(self):
            """Returns name of the tab."""
            return self.tab_spec['name']

    DynamicTab.__name__ = 'MainWindowTab' + tab_spec['id'].capitalize()

    tab = DynamicTab(parent)

    return tab


def construct_tabs(selected_pipeline, window, prefs):
    """
    """
    active_plugins = prefs.active_plugins

    pipelines = []
    for source in find_all_sources():
        if source not in active_plugins and source != "meggie":
            continue
        config_path = pkg_resources.resource_filename(
            source, 'configuration.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        if 'pipelines' in config:
            pipelines.extend(config['pipelines'])

    # add possibly missing fields
    for pipeline in pipelines:

        if 'id' not in pipeline:
            raise Exception('Every pipeline specification must have id.')

        if 'name' not in pipeline:
            pipeline['name'] = pipeline['id']

        for tab_spec in pipeline['tabs']:

            if 'id' not in tab_spec:
                raise Exception('Every tab specification must have id.')

            if 'name' not in tab_spec:
                tab_spec['name'] = tab_spec['id']

            if 'inputs' not in tab_spec:
                tab_spec['inputs'] = []

            if 'outputs' not in tab_spec:
                tab_spec['outputs'] = []

            if 'input_actions' not in tab_spec:
                tab_spec['input_actions'] = []

            if 'output_actions' not in tab_spec:
                tab_spec['output_actions'] = []

            if 'info' not in tab_spec:
                tab_spec['info'] = []

    found = False
    combined_spec = {}
    for pipeline in pipelines:
        if pipeline['id'] == selected_pipeline:
            combined_spec = pipeline
            found = True
            break
    if not found:
        raise Exception('Could not find pipeline with the selected name')

    # merges specification from others to first
    for pipeline in pipelines:

        # if this is the first, skip
        if pipeline is combined_spec:
            continue

        # if this has different name, skip
        if selected_pipeline != pipeline['id']:
            continue

        for tab_spec in pipeline['tabs']:

            # if completely new tab, just add it to list
            if tab_spec['id'] not in [tab['id'] for tab in combined_spec['tabs']]:
                combined_spec['tabs'].append(tab_spec)
            # otherwise..
            else:
                # find idx of the tab in the first specification
                idx = [tab['id'] for tab in combined_spec['tabs']].index(tab_spec['id'])

                # and add missing inputs
                for input_spec in tab_spec['inputs']:
                    if input_spec not in combined_spec['tabs'][idx]['inputs']:
                        combined_spec['tabs'][idx]['inputs'].append(input_spec)

                # add missing outputs
                for input_spec in tab_spec['outputs']:
                    if input_spec not in combined_spec['tabs'][idx]['outputs']:
                        combined_spec['tabs'][idx]['outputs'].append(input_spec)

                # add missing input actions
                for input_spec in tab_spec['input_actions']:
                    if input_spec not in combined_spec['tabs'][idx]['input_actions']:
                        combined_spec['tabs'][idx]['input_actions'].append(input_spec)

                # add missing output actions
                for input_spec in tab_spec['output_actions']:
                    if input_spec not in combined_spec['tabs'][idx]['output_actions']:
                        combined_spec['tabs'][idx]['output_actions'].append(input_spec)

                # add missing info elements
                for input_spec in tab_spec['info']:
                    if input_spec not in combined_spec['tabs'][idx]['info']:
                        combined_spec['tabs'][idx]['info'].append(input_spec)


    # Read action specs from file system
    action_specs = find_all_action_specs()

    # Do a thorough validation of the pipeline
    # that is check if necessary actions are found and 
    # if the input elements needed are present
    for tab_spec in combined_spec['tabs']:
        for elem in tab_spec['input_actions']:
            if elem not in action_specs.keys():
                raise Exception("Cannot read action " + elem + ".")

            for input_elem in action_specs[elem][2]['inputs']:
                if input_elem not in tab_spec['inputs']:
                    raise Exception('Inconsistent tab and action. ' + str(input_elem) + 
                                    ' not present in the tab but needed by the action.')

        for elem in tab_spec['output_actions']:
            if elem not in action_specs.keys():
                raise Exception("Cannot read action " + elem + ".")

        for elem in tab_spec['info']:
            if elem not in action_specs.keys():
                raise Exception("Cannot read info item " + elem + ".")

    # If everything is fine, construct each of the tabs
    tabs = []
    for tab_spec in combined_spec['tabs']:
        tabs.append(construct_tab(tab_spec, action_specs, window))

    return tabs


def subject_action(inner_function):
    def outer_function(self, subject, params, *args, **kwargs):

        message_dict = {
            'uid': self.uid,
            'type': 'SUBJECT_START',
            'subject_uid': subject.uid,
            'params': params
        }
        logging.getLogger('action_logger').info(message_dict)

        res = inner_function(self, subject, params, *args, **kwargs)

        message_dict = {
            'uid': self.uid,
            'type': 'SUBJECT_END',
            'subject_uid': subject.uid
        }
        logging.getLogger('action_logger').info(message_dict)

        return res
    return outer_function


class Action:
    """
    """
    logged = True

    def __init__(self, experiment, data, window, action_spec):
        """
        """
        self.experiment = experiment
        self.data = data
        self.window = window
        self.action_spec = action_spec

        # generate short temporary uid
        self.uid = generate_uid()

        if self.logged:
            # and log action with it
            message_dict = {
                'uid': self.uid,
                'type': 'ACTION_START',
                'id': action_spec['id']
            }
            logging.getLogger('action_logger').info(message_dict)

    def run(self):
        """ Called when action is initiated
        """
        messagebox("Running action " + self.action_spec['id'])


class InfoAction(Action):
    logged = False

    def run(self):
        """ Called when the info box is filled.
        """
        return "Returned content."

