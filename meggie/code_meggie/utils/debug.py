def debug_trace():
    """ Helper to allow debugging with pyqt application.
    After debugging call PyQt4.QtCore.pyqtRestoreInputHook
    """
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()
    
    import pdb; pdb.set_trace()