import tempfile
import os
import shutil
import numpy as np

from meggie.experiment import Experiment
from meggie.utilities.filemanager import create_timestamped_folder
from meggie.utilities.filemanager import save_csv
from meggie.utilities.filemanager import load_csv


def test_create_timestamped_folder():
    with tempfile.TemporaryDirectory() as dirpath:

        name = 'test_experiment'
        author = ''
        path = os.path.join(dirpath, name)
        experiment = Experiment(name, author, path)

        create_timestamped_folder(experiment)

        contents = os.listdir(os.path.join(experiment.path, 'output'))
        assert(len(contents) > 0)


def test_save_and_load_csv():
    with tempfile.TemporaryDirectory() as dirpath:

        filepath = os.path.join(dirpath, 'data.csv')

        data = np.array([[1,2,3], [4,5,6]])
        column_names = ['A', 'B', 'C']
        row_descs = [('X', 'Kissa'), ('Y', 'Koira')]

        save_csv(filepath, data, column_names, row_descs)

        loaded_column_names, loaded_row_descs, loaded_data = load_csv(filepath)

        assert(loaded_column_names == column_names)
        assert(loaded_row_descs[0] == row_descs[0])
        assert(loaded_row_descs[1] == row_descs[1])
        assert(np.array_equal(loaded_data, data))

