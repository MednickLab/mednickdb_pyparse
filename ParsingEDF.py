import numpy
import mne
import json
import sys
import time



def EdfParse(path=None):
    try:
        EDF_file = mne.io.read_raw_edf(path)
    except RuntimeError:
        EDF_file = mne.io.read_raw_edf(path, preload=True)  # FIXME: Preload is only nessary for edf+, so try catch this

    edfDictionary = {}
    # edfDictionary['bads'] = EDF_file.info["bads"]

    # edfDictionary['highpass'] = EDF_file.info["highpass"]
    # edfDictionary['lowpass'] = EDF_file.info["lowpass"]
    # Changed from epoch to date
    timeConvert = time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(EDF_file.info["meas_date"]))
    edfDictionary['meas_date'] = timeConvert
    edfDictionary['nchan'] = EDF_file.info["nchan"]
    edfDictionary['sfreq'] = EDF_file.info["sfreq"]
    edfDictionary['subject_info'] = EDF_file.info["subject_info"]
    edfDictionary['ch_names'] = EDF_file.ch_names

    edfDictionary_with_appended_key = {}
    for key in edfDictionary:
        edfDictionary_with_appended_key["edf_" + key] = edfDictionary[key]

    return edfDictionary_with_appended_key
