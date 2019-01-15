""" This module provides tools for popping up simple messageboxes
"""

import logging
from meggie.ui.general import messageBoxes

def exc_messagebox(parent, exc, exec_=False):
    """ Pops up a messagebox for exceptions
    """

    try:
        if isinstance(exc, str):
            error_message = exc
        else:
            error_message = str(exc)
            if not error_message:
                error_message = ('(empty message of type ' + 
                                 str(exc.__repr__()) + ')')
    except Exception as e:
        error_message = ''

    # print traceback to console
    logging.getLogger('ui_logger').exception(error_message)

    # create messagebox for user
    message = '\n\n'.join([
        'There has been an error with following message: ',
        error_message,
        'More information can be found from console below.',
    ])

    parent.messagebox = messageBoxes.shortMessageBox(message)
    if exec_:
        parent.messagebox.exec_()
    else:
        parent.messagebox.show()

def messagebox(parent, msg, title='Info', exec_=False):
    """ Pops up a messagebox
    """
    parent.messagebox = messageBoxes.shortMessageBox(msg, title=title)
    if exec_:
        parent.messagebox.exec_()
    else:
        parent.messagebox.show()
