import numpy
import mne
import json
import sys
import datetime
import time
import os


def parse_edf_file_to_dict(path):
    """extract metadata from file @path and return in a dictionary"""
    assert os.path.splitext(path)[-1].lower() == '.edf', "Only EDFs are supported"

    try:
        edf_file = mne.io.read_raw_edf(path, stim_channel=None, verbose=False)
    except RuntimeError:
        edf_file = mne.io.read_raw_edf(path, preload=True, stim_channel=None, verbose=False)

    edf_dictionary = {}
    edf_dictionary['meas_date'] = datetime.datetime.fromtimestamp(edf_file.info["meas_date"])
    edf_dictionary['nchan'] = edf_file.info["nchan"]
    edf_dictionary['sfreq'] = edf_file.info["sfreq"]
    edf_dictionary['subject_info'] = edf_file.info["subject_info"]
    edf_dictionary['ch_names'] = edf_file.ch_names

    return {"edf_"+key:value for key, value in edf_dictionary.items()}
