import numpy
import mne
import json
import sys
import datetime
import time


def EdfParse(path):
    """extract metadata from file @path and return in a dictionary"""
    try:
        EDF_file = mne.io.read_raw_edf(path, stim_channel=None, verbose=False)
    except RuntimeError:
        EDF_file = mne.io.read_raw_edf(path, preload=True, stim_channel=None, verbose=False)

    edfDictionary = {}
    edfDictionary['meas_date'] = datetime.datetime.fromtimestamp(EDF_file.info["meas_date"])
    edfDictionary['nchan'] = EDF_file.info["nchan"]
    edfDictionary['sfreq'] = EDF_file.info["sfreq"]
    edfDictionary['subject_info'] = EDF_file.info["subject_info"]
    edfDictionary['ch_names'] = EDF_file.ch_names

    return {"edf_"+key:value for key, value in edfDictionary.items()}
