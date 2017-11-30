#TODO: may not be used...

import pandas as pd
import mne
import numpy
import datetime
import json
import matplotlib.pyplot as plt

def hypRead(path = None):
    if path == None:
        #File name needs to be parsed to not include full Path
        EDF_file = mne.io.read_raw_edf(sys.argv[1])
        path = sys.argv[1]
    else:
        EDF_file = mne.io.read_raw_edf(path, stim_channel = 'auto', preload = True)
        #splits the fileName into list of strings seperated by \
        #[-1] takes the last string in the list which is the file name
        NameOfFile = (path.split('\\')[-1])

    jsonObj = {}
    jsonObj["epochstage"] = []
    jsonObj["epochstarttime"] = []
    interval = -30

    for i in range(len(mne.io.get_edf_events(EDF_file))):
        durationOfStage = mne.io.get_edf_events(EDF_file)[i][1]
        while durationOfStage > 0:
            stage = mne.io.get_edf_events(EDF_file)[i][2].split(' ')
            interval+= 30
            jsonObj["epochstage"].append(stage[-1])
            jsonObj["epochstarttime"].append(interval)
            durationOfStage -= 30

    #For missed duration
    lastDuration = mne.io.get_edf_events(EDF_file)[-1][1]
    while lastDuration > 0:
        stage = mne.io.get_edf_events(EDF_file)[-1][2].split(' ')
        interval+= 30
        jsonObj["epochstage"].append(stage[-1])
        jsonObj["epochstarttime"].append(interval)
        lastDuration -= 30


    print(len(jsonObj["epochstage"]))
    print(len(jsonObj["epochstarttime"]))
    print(mne.io.get_edf_events(EDF_file))
    print('split')
    print(jsonObj)

def main (File_to_Parse):
    hypRead(File_to_Parse)

main('/home/jesse/Desktop/MednickLabs/PythonParsing/R21/edfs/15.edf')
