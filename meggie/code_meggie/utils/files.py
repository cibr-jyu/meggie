
def filepath(filename):
    """ Tries to find correct path for file with pkg_resources """
    try:
        import pkg_resources
        return pkg_resources.resource_filename('meggie', filename)
    except ImportError:
        return filename
