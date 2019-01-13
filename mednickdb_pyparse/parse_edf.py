import numpy as np
import mne
import datetime
import os


def parse_eeg_file(path):
    """
    extract metadata from file @path and return in a dictionary. Only supports EDF at present.
    TODO extend for all eeg type files that mne can process
    :param path: path of edf to parse
    :return:
    """
    if os.path.splitext(path)[-1].lower() != '.edf':
        NotImplementedError("Only EDFs are supported currently. More files coming.")

    try: #edf
        edf_file = mne.io.read_raw_edf(path, stim_channel=None, verbose=False)
    except RuntimeError: #edf+
        edf_file = mne.io.read_raw_edf(path, preload=True, stim_channel=None, verbose=False)

    # TODO edf++

    eeg_data = {}
    eeg_data['meas_date'] = datetime.datetime.fromtimestamp(edf_file.info["meas_date"])
    eeg_data['nchan'] = edf_file.info["nchan"]
    eeg_data['sfreq'] = edf_file.info["sfreq"]
    eeg_data['subject_info'] = edf_file.info["subject_info"]
    eeg_data['ch_names'] = edf_file.ch_names

    return {"eeg_"+key: value for key, value in eeg_data.items()}
