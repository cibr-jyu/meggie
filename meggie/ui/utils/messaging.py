""" This module provides tools for popping up simple messageboxes
"""

import traceback
from meggie.ui.general import messageBoxes

def exc_messagebox(parent, exc):
    """ Pops up a messagebox for exceptions
    """
    # print traceback to console
    traceback.print_exc()

    try:
        error_message = str(exc.args[0])
    except:
        error_message = str(exc)

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
