""" This module provides tools for popping up simple messageboxes
"""

import logging
from meggie.ui.general import messageBoxes

def exc_messagebox(parent, exc):
    """ Pops up a messagebox for exceptions
    """
    try:
        error_message = str(exc.args[0])
        if not error_message:
            error_message = exc.__repr__()
    except:
        error_message = str(exc)

    # print traceback to console
    logging.getLogger('ui_logger').exception(error_message)

    # create messagebox for user
    message = '\n\n'.join([
        'There has been an error with following message: ',
        error_message,
        'More information can be found from console below.',
    ])

    parent.messagebox = messageBoxes.shortMessageBox(message)
    parent.messagebox.show()

def messagebox(parent, msg, title='Info'):
    """ Pops up a messagebox
    """
    parent.messagebox = messageBoxes.shortMessageBox(msg, title=title)
    parent.messagebox.show()
