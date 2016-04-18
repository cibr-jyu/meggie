import traceback
from meggie.ui.general import messageBoxes

def exc_messagebox(parent, e):
    # print traceback to console
    traceback.print_exc()

    # create messagebox for user
    message = '\n\n'.join([
        'There has been an error with following message: ',
        str(e.args[0]),
        'More information can be found from console below.',
    ])

    parent.messagebox = messageBoxes.shortMessageBox(message)
    parent.messagebox.show()

def messagebox(parent, msg, title='Info'):
    parent.messagebox = messageBoxes.shortMessageBox(msg, title=title)
    parent.messagebox.show()
