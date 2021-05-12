"""Defines an abstract class to derive from when creating datatypes."""


class Datatype:
    """Abstract class that shows the methods that can be expected to 
    be present in the actual datatypes.

    Parameters
    ----------
    name : str
        Name of the data object, used in the UI lists and in the .exp file.
    directory : str
        Absolute path to the folder where the data is expected to be stored.
    params : dict
        Contains additional information about the data object.
    content : dict or instance, optional
        Stores the actual numerical data.
        If not provided, it is assumed that the content is already stored 
        in the file system.
    """
    def __init__(self, name, directory, params, content=None):
        pass
 
    def save_content(self):
        """Saves the data object contents to the file system."""
        raise NotImplementedError('')

    def delete_content(self):
        """Deletes the data object contents from the file system."""
        raise NotImplementedError('')

    @property
    def content(self):
        """Returns the actual stored contents. Is expected to load
        it from the file system if not loaded already."""
        raise NotImplementedError('')

    @property
    def data(self):
        """In contrast to returning contents, that can be for example mne.Epochs,
        return actual numpy arrays """
        raise NotImplementedError('')

    @property
    def info(self):
        """Returns info, usually needed for sensor locations."""
        raise NotImplementedError('')

    @property
    def params(self):
        """Returns related information about the data object,
        stored in the experiment file."""
        raise NotImplementedError('')

    @property
    def times(self):
        """If time-based object, should return the times."""
        raise NotImplementedError('')

    @property
    def freqs(self):
        """If freqs-based object, should return the freqs."""
        raise NotImplementedError('')

    @property
    def ch_names(self):
        """If contains channels, should return the ch_names."""
        raise NotImplementedError('')
