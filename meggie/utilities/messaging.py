import logging

from meggie.utilities.dialogs.shortMessageBoxMain import shortMessageBox
from meggie.utilities.dialogs.shortQuestionBoxMain import shortQuestionBox


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
    logging.getLogger('ui_logger').exception('')

    # create messagebox for user
    message = '\n\n'.join([
        'There has been an error with following message: ',
        error_message,
        'More information can be found from console below.',
    ])

    messagebox = shortMessageBox(message, parent)
    if exec_:
        messagebox.exec_()
    else:
        messagebox.show()


def messagebox(parent, msg, exec_=False):
    """ Pops up a messagebox
    """
    messagebox = shortMessageBox(msg, parent)
    if exec_:
        messagebox.exec_()
    else:
        messagebox.show()


def questionbox(parent, question, handler):
    questionbox = shortQuestionBox(question, parent, handler)
    questionbox.exec_()
