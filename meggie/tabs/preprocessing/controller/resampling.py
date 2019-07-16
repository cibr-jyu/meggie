import meggie.utilities.fileManager as fileManager


def resample(experiment, raw, fname, rate):
    raw.resample(rate)
    fileManager.save_raw(experiment, raw, fname)
