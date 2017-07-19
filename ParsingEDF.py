import numpy
import mne
import json
import sys
import time

#File name needs to be parsed to not include full Path
EDF_file = mne.io.read_raw_edf(sys.argv[1])

#Splits the fileName into list of strings seperated by /
#[-1] takes the last string in the list which is the file name
NameOfFile = (sys.argv[1].split('/')[-1])

timeConvert = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(EDF_file.info["meas_date"]))

edfDictionary = {}

edfDictionary['bads'] = EDF_file.info["bads"]
edfDictionary['ch_names'] = EDF_file.ch_names
edfDictionary['highpass'] = EDF_file.info["highpass"]
edfDictionary['lowpass'] = EDF_file.info["lowpass"]
#Changed from epoch to date
edfDictionary['meas_date'] = timeConvert
edfDictionary['nchan'] = EDF_file.info["nchan"]
edfDictionary['sfreq'] = EDF_file.info["sfreq"]
edfDictionary['subject_info'] = EDF_file.info["subject_info"]

edfDictionary['file_name'] = NameOfFile 

#The JSON dictionary of meta data of edf file
edfDictionaryToJSON = json.dumps(edfDictionary)
