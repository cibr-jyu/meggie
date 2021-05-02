
class Datatype:
    """ Shows the methods that can be expected to 
    be present in datatypes 
    """
    def __init__(self, name, directory, params, content=None):
        """ 
        """
 
    def save_content(self):
        """ saves the main data object to file system """
        raise NotImplementedError('')

    def delete_content(self):
        """ deletes the main data object from file system """
        raise NotImplementedError('')

    @property
    def content(self):
        """ returns the main data object. is expected to read
        it from the file system if needed """
        raise NotImplementedError('')

    @property
    def data(self):
        """ return numpy array of the data. may or may not be
        different from content """
        raise NotImplementedError('')

    @property
    def info(self):
        """ return mne info object """
        raise NotImplementedError('')

    @property
    def params(self):
        """ returns related information about the item,
        stored in the experiment file """
        raise NotImplementedError('')

    @property
    def times(self):
        """ if time-based object, should return the times """
        raise NotImplementedError('')

    @property
    def freqs(self):
        """ if freqs-based object, should return the freqs """
        raise NotImplementedError('')

    @property
    def ch_names(self):
        """ if contains channels, should return the ch_names """
        raise NotImplementedError('')
