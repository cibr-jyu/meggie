""" Contains a class for logic of action dialog.
"""
import os
import json
import logging
import re

from pprint import pformat

from PyQt5 import QtWidgets

from meggie.mainwindow.dynamic import find_all_action_specs
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox

from meggie.mainwindow.dialogs.actionDialogUi import Ui_ActionDialog


class ActionDialog(QtWidgets.QDialog):
    """ Contains logic for action dialog.
    """

    def __init__(self, parent, experiment):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.ui = Ui_ActionDialog()
        self.ui.setupUi(self)

        # clear the tree widget
        self.ui.treeWidgetActions.clear()

        # read the actions log
        try:
            path = os.path.join(experiment.path, 'actions.log')
            with open(path, 'r') as f:
                lines = f.readlines()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        # get action specifications for id -> name conversion
        action_specs = find_all_action_specs()

        # organize actions data by action uid
        actions = {}
        for line in lines:
            content = json.loads(line)
            if not content['uid'] in actions:
                actions[content['uid']] = []
            actions[content['uid']].append(content)

        # combine data of each action uid to single dict
        # and organize by subject uid
        subject_tree = {}
        for action_uid, action_rows in actions.items():
            action_tree = {}
            name = None
            for row in action_rows:
                if row['type'] == 'ACTION_START':
                    id_ = row['id']
                    desc = row.get('desc')

                if row['type'] == 'SUBJECT_START':
                    if not row['subject_uid'] in action_tree:
                        action_tree[row['subject_uid']] = {}

                    action_tree[row['subject_uid']]['params'] = row['params']

                if row['type'] == 'SUBJECT_END':
                    if not row['subject_uid'] in action_tree:
                        action_tree[row['subject_uid']] = {}
                    action_tree[row['subject_uid']]['finished'] = True
                    action_tree[row['subject_uid']]['timestamp'] = row['timestamp']

            for subject_uid, branch in action_tree.items():
                if branch.get('finished'):
                    branch['id'] = id_
                    branch['desc'] = desc
                    if subject_uid not in subject_tree:
                        subject_tree[subject_uid] = []
                    subject_tree[subject_uid].append(branch)

        # for each subject of the experiment (subjects that have been removed
        # or replaced will not be showed) see if there are entries of finished
        # actions and add them to the tree widget.
        for subject_name, subject in sorted(experiment.subjects.items()):
            if subject.uid not in subject_tree:
                continue

            # Add root node for subject
            subject_item = QtWidgets.QTreeWidgetItem(self.ui.treeWidgetActions)
            subject_item.setText(0, subject_name)

            subject_actions = subject_tree[subject.uid]
            for action_data in subject_actions:

                # create node for each action
                action_item = QtWidgets.QTreeWidgetItem(subject_item)
                
                # if name can be found from the core or installed plugins,
                # use it, otherwise print just the id.
                name = action_data['id']
                if action_data['id'] in action_specs:
                    if action_specs[action_data['id']][2].get('name'):
                        name = action_specs[action_data['id']][2].get('name')

                if action_data['desc']:
                    name += " ({0})".format(action_data['desc'])

                action_item.setText(0, name)

                # Add params item to the action
                params_item = QtWidgets.QTreeWidgetItem(action_item)
                params_item.setText(0, 'Params')
  
                # And fill it with params that are present in the data
                for param_name, param_value in action_data['params'].items():
                    msg = "{0}: {1}".format(param_name, json.dumps(param_value))
                    param_item = QtWidgets.QTreeWidgetItem(params_item)
                    param_item.setText(0, msg)

                # Get date and utc time from the data
                template = re.compile(r'([0-9]*-[0-9]*-[0-9]*)T([0-9]*:[0-9]*:[0-9]*)\..*')
                elems = template.match(action_data['timestamp'])
                msg = "{0}: {1} {2} UTC".format("Timestamp", elems[1], elems[2])
       
                # and add a item
                timestamp_item = QtWidgets.QTreeWidgetItem(action_item)
                timestamp_item.setText(0, msg)

    def on_treeWidgetActions_itemDoubleClicked(self, item):
        if item.childCount() == 0:
            # try creating a pretty formatted details dialog
            try:
                match = re.compile("([a-zA-Z0-9_]*): (.*)").match(item.text(0))
                if not match:
                    return

                key = match.group(1)
                val = match.group(2)
                try:
                    obj = json.loads(val)
                except Exception as exc:
                    obj = val
                message = pformat(obj)
                messagebox(self, message)
            except Exception as exc:
                logging.getLogger('ui_logger').exception("")
                return

