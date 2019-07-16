import meggie.code_meggie.general.fileManager as fileManager


def resample(experiment, raw, fname, rate):
    raw.resample(rate)
    fileManager.save_raw(experiment, raw, fname)
