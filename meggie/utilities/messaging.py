"""Provides functions for popping up different kind of messageboxes."""

import logging
from meggie.utilities.dialogs.shortMessageBoxMain import shortMessageBox
from meggie.utilities.dialogs.shortQuestionBoxMain import shortQuestionBox


def exc_messagebox(parent, exc):
    """Pops up a messagebox for a exception.

    Parameters
    ----------
    parent : QDialog or QMainWindow
        Parent dialog, that is set as a parent.
    exc : instance of Exception
        The exception that is presented.
    """

    try:
        if isinstance(exc, str):
            error_message = exc
        else:
            error_message = str(exc)
            if not error_message:
                error_message = "(empty message of type " + str(exc.__repr__()) + ")"
    except Exception:
        error_message = ""

    # print traceback to console
    logging.getLogger("ui_logger").exception("")

    # create messagebox for user
    message = "\n\n".join(
        [
            "There has been an error with following message: ",
            error_message,
            "More information can be found from console below.",
        ]
    )

    messagebox = shortMessageBox(message, parent)
    messagebox.show()


def messagebox(parent, msg):
    """Pops up a messagebox with a message.

    Parameters
    ----------
    parent : QDialog or QMainWindow
        Parent dialog, that is set as a parent.
    msg : str
        The message that is presented.
    """
    messagebox = shortMessageBox(msg, parent)
    messagebox.show()


def questionbox(parent, question, handler):
    """Pops up a yes/no questionbox.

    Parameters
    ----------
    parent : QDialog or QMainWindow
        Parent dialog, that is set as a parent.
    question : str
        The question that is asked.
    handler : function
        A function that is called with the answer used provided.

    """

    questionbox = shortQuestionBox(question, parent, handler)
    questionbox.exec()
