""" Creates mock Experiments and Subjects for testing purposes
"""

import tempfile


class Experiment:
    """
    """
    def __init__(self):
        self.subjects = {}


class Subject:
    """
    """
    def __init__(self, name):
        self.spectrums_directory = tempfile.mkdtemp()
        self.spectrums = {}

        self.subject_name = name

    def add_spectrum(self, spectrum):
        self.spectrums[spectrum.name] = spectrum


def get_experiment():
    """ Returns experiment with subjects """

    experiment = Experiment()

    subject_1 = Subject('test_subject_1')
    experiment.subjects['test_subject_1'] = subject_1

    subject_2 = Subject('test_subject_2')
    experiment.subjects['test_subject_2'] = subject_2

    experiment.active_subject = subject_1

    return experiment
