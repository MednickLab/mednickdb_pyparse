import pandas as pd
import mne
import re
import math
import xml.etree.ElementTree as ET
import numpy as np
import scipy.interpolate
from scipy.io import loadmat
from mednickdb_pysleep import sleep_architecture
import datetime
from utils import matfile_loader, mat_datenum_to_py_datetime


# Parse score file of various formats.
# Formats will be automatically detected. Code originally written by Seehoon and Jesse.
# Improved by Ben Yetton.

subidspellings = ["Subject", "subject", "SubjectID", "subjectid", "subjectID", "subid", "subID", "SUBID", "SubID",
                  "Subject ID", "subject id", "ID", "SF_SubID"]
starttimespellings = ["starttime", "startime", "start time", "Start Time", "PSG Start Time", "Start"]

# characters that we will strip
STRIP = "' ', ',', '\'', '(', '[', '{', ')', '}', ']'"

epoch_len = 30


def parse_scorefile_to_dict(file, studyid):
    stage_map_dict = get_stagemap(file, studyid)
    dict_data = extract_score_data(file, stage_map_dict)

    # Do stagemap
    dict_data['epochstage'] = [stage_map_dict[str(x)] if str(x) in stage_map_dict else -1 for x in dict_data['epochstage']]
    if all(np.array(dict_data['epochstage']) == -1):
        raise ValueError('All stages are unknown, this is probably an error, maybe the stagemap was not found. Make sure the study name is correct.')

    if isinstance(dict_data['epochoffset'][0], float):
        dict_data['epochoffset'] = [round(x, 2) for x in dict_data['epochoffset']]

    minutes_in_stage, perc_in_stage, total_mins = sleep_architecture.sleep_stage_architecture(dict_data['epochstage'])
    for stage, mins in minutes_in_stage.items():
        dict_data['mins_in_'+str(stage)] = mins
    dict_data['sleep_efficiency'] = sleep_architecture.sleep_efficiency(minutes_in_stage, total_mins, wake_stage=0)
    dict_data['total_sleep_time'] = sleep_architecture.total_sleep_time(minutes_in_stage, wake_stage=0)
    return dict_data


def get_stagemap(file, studyid):
    if file.endswith('.mat'):
        stagemap_type = 'hume'
    elif 'MednickLab' in studyid or 'Cellini' in studyid:
        stagemap_type = 'grass'
    elif studyid in ['K01', 'SF', 'NP', 'LSD', 'PSTIM', 'SF2014']:
        stagemap_type = 'grass'
    elif file.endswith('.xml'):
        stagemap_type = 'xml'
    else:
        stagemap_type = studyid

    stagemap = pd.read_excel('stagemaps/' + stagemap_type + '_stagemap.xlsx',
                             converters={'mapsfrom': str, 'mapsto': int})
    stage_map_dict = {k: v for k, v in zip(stagemap['mapsfrom'], stagemap['mapsto'])}
    return stage_map_dict


def extract_score_data(file, stagemap):
    if file.endswith("xls") or file.endswith("xlsx") or file.endswith(".csv"):
        xl = pd.ExcelFile(file)
        if 'GraphData' in xl.sheet_names:  # Then we have a mednick type scorefile
            return parse_grass_scorefile(file)

    # these are the scoring files (txt)
    elif file.endswith(".txt"):
        file_data = open(file, 'r')
        return select_and_run_parser_function(file_data)  # This determines which type of txt file is present

    # EDF+ files which contain scoring data
    elif file.endswith(".edf"):
        return parse_edf_scorefile(file, stagemap)

    elif file.endswith('.xml'):  # Some score file were xml...
        return xml_parse(file, stagemap)

    elif file.endswith('.mat'):
        return mat_parse(file)

    raise ValueError('ScoreFile not able to be parsed.')


def mat_parse(file):
    hume_dict = matfile_loader(file)
    dict_obj = {"epochstage": hume_dict['stages'],
                "epochoffset": hume_dict['stageTime']*hume_dict['win']*2,
                "starttime": mat_datenum_to_py_datetime(hume_dict['lightsOFF'])} #TODO deal with hume timing issues

    return dict_obj


# CODE FROM MNE TO READ KEMP FILES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def read_edf_annotations(fname, annotation_format="edf/edf+"):
    """read_edf_annotations

    Parameters:
    -----------
    fname : str
        Path to file.

    Returns:
    --------
    annot : DataFrame
        The annotations
    """
    with open(fname, 'r', encoding='utf-8',
              errors='ignore') as annotions_file:
        tal_str = annotions_file.read()

    if "edf" in annotation_format:
        if annotation_format == "edf/edf+":
            exp = '(?P<onset>[+\-]\d+(?:\.\d*)?)' + \
                  '(?:\x15(?P<duration>\d+(?:\.\d*)?))?' + \
                  '(\x14(?P<description>[^\x00]*))?' + '(?:\x14\x00)'

        elif annotation_format == "edf++":
            exp = '(?P<onset>[+\-]\d+.\d+)' + \
                  '(?:(?:\x15(?P<duration>\d+.\d+)))' + \
                  '(?:\x14\x00|\x14(?P<description>.*?)\x14\x00)'

        annot = [m.groupdict() for m in re.finditer(exp, tal_str)]
        good_annot = pd.DataFrame(annot)
        good_annot = good_annot.query('description != ""').copy()
        good_annot.loc[:, 'duration'] = good_annot['duration'].astype(float)
        good_annot.loc[:, 'onset'] = good_annot['onset'].astype(float)
    else:
        raise ValueError('Not supported')

    return good_annot


def resample_to_new_epoch_len(annot, stage_map_dict, new_epoch_len=30):
    """Some scorefiles have 20 second epochs, this will resample to some other length (30 generally)."""
    annot.reset_index(inplace=True)
    # This is coupled with stagemaps because we need some way of removing the non stage entries of the annotations
    stage_map_back_dict = {v: k for k, v in stage_map_dict.items()}
    stage_entries = [True if i in stage_map_dict else False for i in annot['description'].values]
    annot_stage_only = annot.loc[stage_entries, :]
    annot_stage_only.loc[:, 'description'] = annot_stage_only.loc[:, 'description'].map(stage_map_dict)

    sub_second_offset = annot_stage_only['onset'].values[0] - int(annot_stage_only['onset'].values[0])
    onset = list(annot_stage_only['onset'].astype(int))
    window_onsets = np.array((range(onset[0], onset[-1], new_epoch_len))) + sub_second_offset
    hypno = scipy.interpolate.interp1d(annot_stage_only['onset'], annot_stage_only['description'], kind='zero')
    window_stages = [stage_map_back_dict[stage] for stage in hypno(window_onsets)]
    durations = [new_epoch_len for i in window_stages]
    return pd.DataFrame({'onset': list(window_onsets), 'description': window_stages, 'duration': durations})


def parse_edf_scorefile(path, stage_map_dict):
    """Load edf file @path and extract relevant meta data including epoch stages. Depends on MNE."""

    dictObj = {"epochstage": [], "epochoffset": []}

    try: #type1
        EDF_file = mne.io.read_raw_edf(path, stim_channel='auto', preload=True, verbose=False)
        raw_annot = mne.io.find_edf_events(EDF_file)
        annot = pd.DataFrame(raw_annot, columns=['onset', 'duration', 'description'])
        dictObj['starttime'] = datetime.datetime.fromtimestamp(EDF_file.info['meas_date'])
    except TypeError: #type2
        # need to do try and except because edf++ uses different reading style
            annot = read_edf_annotations(path)
    except ValueError: #type3
        annot = read_edf_annotations(path, annotation_format="edf++")

    annot = resample_to_new_epoch_len(annot, stage_map_dict, epoch_len)
    dictObj['epochstage'] = list(annot['description'].values)
    dictObj['epochoffset'] = list(annot['onset'].values)

    return dictObj


def xml_repeater(node):
    temp = {}
    for child in node:
        J = (xml_repeater(child))
        if len(J) != 0:
            for key in J.keys():
                if key in temp.keys():
                    temp[key].append(J[key])
                else:  # if J[key] != None:
                    temp[key] = []
                    temp[key].append(J[key])
        dict = {child.tag: child.text}
        if (child.text != '\n'):
            for key in dict.keys():
                if key in temp.keys():
                    temp[key].append(dict[key])
                else:  # if dict[key] != None:
                    temp[key] = []
                    temp[key].append(dict[key])
    return temp


def xml_parse(file, stage_map_dict):
    tree = ET.parse(file)
    root = tree.getroot()
    dict_xml = xml_repeater(root)
    temp_dict = {'description': [], 'onset': [], 'duration': []}

    for key in dict_xml.keys():
        needToStrip = str(dict_xml[key]).split(',')
        for i in range(len(needToStrip)):
            needToStrip[i] = needToStrip[i].lstrip(STRIP).rstrip(STRIP)
        dict_xml[key] = needToStrip

    # Need to change this maybe	right now only includes the important stuff
    # Need to fix the time
    # get dictionary with sleepevent, start time, and duration
    # need to expand so it will see every 30 sec and have it in epoch time
    for i in range(len(dict_xml['EventType'])):
        if "Stages" in dict_xml['EventType'][i]:
            temp_dict['description'].append(dict_xml['EventConcept'][i].split('|')[0])
            temp_dict['duration'].append(float(dict_xml['Duration'][i]))
            temp_dict['onset'].append(float(dict_xml['Start'][i]))
    annot = pd.DataFrame(temp_dict)
    annot_resampled = resample_to_new_epoch_len(annot, stage_map_dict, epoch_len)

    return_dict = {}
    return_dict['epochstage'] = list(annot_resampled['description'].values)
    return_dict['epochoffset'] = list(annot_resampled['onset'].values)
    return_dict['starttime'] = datetime.datetime.strptime(dict_xml['ClockTime'][0].split(' ')[-1], '%H.%M.%S')

    return return_dict


def select_and_run_parser_function(file):
    """Returns an integer determing which parse method to use
       if found == 0 file contain only s and 0s
       if found == 1 file contain latency and type(sleep stage mode)
       if found == 2 file contain sleep stage , and time"""

    parsers = {0: parse_basic_type_scorefile,
               1: parse_lat_type_scorefile,
               2: parse_full_type_scorefile}

    key_words = ["latency", "RemLogic"]
    found = 0
    firstline = file.readline()
    file.seek(0)
    for count in range(len(key_words)):
        if firstline.find(key_words[count]) != -1:
            found = count + 1

    try:
        return parsers[found](file)
    except KeyError:
        raise ValueError('txt ScoreFile not able to be parsed.')


def parse_basic_type_scorefile(file):  # No starttime extracted
    dict_obj = {"epochstage": [], "epochoffset": []}
    time = 0
    for line in file:
        temp = line.split(' ')
        temp = temp[0].split('\t')
        temp[0] = temp[0].strip('\n')
        dict_obj["epochstage"].append(temp[0])
        dict_obj["epochoffset"].append(time)
        time = time + epoch_len
    return dict_obj


# Type 1		Example: SpencerLab
# these files give time in seconds in 30 sec interval
# start of sleep time is given in demographic file
def parse_lat_type_scorefile(file):
    dict_obj = {"epochstage": [], "epochoffset": []}
    file.readline()  # done so that we can ignore the first line which just contain variable names
    for line in file:
        temp = line.split('  ')
        if len(temp) == 1:
            temp = line.split('\t')
        temp[-1] = temp[-1].strip('\n')
        dict_obj["epochstage"].append(temp[-1].lstrip(" ").rstrip(" "))
        time = temp[0]
        time = int(time)
        dict_obj["epochoffset"].append(time)
    return dict_obj


# Type 2 Example: CAPStudy, maybe other phsyionet stuff...
def parse_full_type_scorefile(file):
    dict_obj = {"epochstage": [], "epochoffset": []}
    # find line with SleepStage
    # find position of SleepStage and Time
    start_split = False
    get_starttime = True
    sleep_stage_pos = 0
    time_pos = 0
    event_pos = 0
    offset_ticker = 0

    for line in file:
        if start_split and line.strip() != '':
            full_line = line.split('\t')
            if get_starttime:
                starttime = full_line[time_pos]
                get_starttime = False
            if len(full_line) > event_pos and full_line[event_pos].find("MCAP") == -1:
                dict_obj["epochstage"].append(full_line[sleep_stage_pos])
                dict_obj["epochoffset"].append(offset_ticker)
                offset_ticker = epoch_len + offset_ticker

        if line.find("Sleep Stage") != -1:
            start_split = True
            full_line = line.split('\t')
            for i in range(len(full_line)):
                if full_line[i] == "Sleep Stage":
                    sleep_stage_pos = i
                if full_line[i].find("Time") != -1:
                    time_pos = i
                if full_line[i].find("Event") != -1:
                    event_pos = i

        if line.find('Recording Date:') != -1:
            full_line = line.split('\t')
            date = full_line[1]
            print(date)

    dict_obj['startime'] = datetime.datetime.strptime(date + ' ' + starttime, '%d/%m/%Y %H.%M.%S')
    return dict_obj


def parse_grass_scorefile(file):
    dict_dict_out = {"epochoffset": [], 'epochstage': []}

    list_data = pd.read_excel(file, sheetname="list")
    graph_data = pd.read_excel(file, sheetname="GraphData")

    time = None
    date = None
    for i in list_data.iterrows():
        if (i[1][1] == "RecordingStartTime"):
            time = i[1][2]
        if (i[1][1] == "TestDate"):
            date = i[1][2]
        if date is not None and time is not None:
            break

    dict_dict_out['starttime'] = datetime.datetime.strptime(date + ' ' + time, '%m/%d/%y %H:%M:%S')

    epoch = 0
    for i in graph_data.iterrows():
        if not (math.isnan(i[1][1])):
            dict_dict_out['epochstage'].append(int(i[1][1]))
            dict_dict_out['epochoffset'].append(epoch)
            epoch += epoch_len
        else:
            break

    return dict_dict_out
