""" This module provides tools to finding paths """

def filepath(filename):
    """ Tries to find correct path for file with pkg_resources """
    try:
        import pkg_resources
        return pkg_resources.resource_filename('meggie', filename)
    except ImportError:
        return filename

def home_filepath(filename):
    """ Tries to find correct path for file from user's home folder """
    from os.path import expanduser
    home = expanduser("~")
    if home:
        return home + '/' + filename
    else:
        return filename
