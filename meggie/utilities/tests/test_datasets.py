import tempfile
from meggie.utilities.datasets import get_open_datasets
from meggie.mainwindow.preferences import PreferencesHandler


def test_create_open_datasets():
    tempdir = tempfile.TemporaryDirectory()

    prefs = PreferencesHandler()
    prefs.workspace = tempdir.name

    datasets = get_open_datasets()
    for dataset in datasets.values():
        dataset["constructor"](
            dataset["title"], "", prefs, set_previous_experiment=False
        )

    tempdir.cleanup()
