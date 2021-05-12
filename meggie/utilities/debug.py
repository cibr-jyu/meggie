"""Contains useful functions for developers.
"""

def debug_trace():
    """Helper to allow debugging with pyqt application.
    
    The standard way of using "import pdb; pdb.set_trace()"
    does not work with Qt application as the Qt fills the terminal
    with messages. Using this bypasses it:
    from meggie.utilities.debug import debug_trace; debug_trace()
    When stopped, use "u" to go to parent function.

    After debugging should call PyQt4.QtCore.pyqtRestoreInputHook, though
    often one just quits and restarts.
    """
    from PyQt5.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()

    import pdb
    pdb.set_trace()
