""" This module provides tools to finding paths """

def homepath():
    """ Tries to find correct path for file from user's home folder """
    from os.path import expanduser
    home = expanduser("~")

    if not home:
        return '.'

    return home
