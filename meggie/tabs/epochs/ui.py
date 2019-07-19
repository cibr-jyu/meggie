"""
"""
counter = 0

def epochs_info(experiment, data, parent):
    global counter
    counter += 1
    message = '\n'.join(["Info about the list element on the left", "",
                         "Where to begin",
                         "Where to go",
                         "To the sea", " (" + str(counter) + ")",
                         "And a long line at the bottom."])
    return message


def create(experiment, data, parent):
    pass


def delete(experiment, data, parent):
    pass


def delete_from_all(experiment, data, parent):
    pass


def plot_epochs(experiment, data, parent):
    pass
