import mne
import sys
import pandas as pd
import numpy
import os
from parse_scorefile import parse_scorefile_to_dict
from parse_edf import parse_edf_file_to_dict
from parse_tabular import parse_tabular_file_to_dict
import glob
import time
import datetime
import warnings
from mednickdb_pyapi.mednickdb_pyapi import MednickAPI

uploads_path = './uploads/' if os.environ['HOME'] is None else '/data/mednick_server/file_uploads/'

"""
# File Types are:
# - sleep (edf without scoring)
# - scoringfile (what you have been dealing with, they could be xlsx, .mat, edfs, etc)
# - tabulardata (this is demographics and the like)
# - sleep diaries (this you can ignore for now, and we can discuss soon)
# - actigraphy (same as above)

# def sleepdiaries_parsing ( file ):
# CSV files
# def actigraphy_parsing (file):
# go line by line until find "- Statistics -"
# Create it as datatable
# - remove any lines starting with a blank
# - remove any lines that are "summary"
# - remove any lines that are "excluded"
# GO until you find line start with '-----'

# go line by line down until find '- Epoch-by-Epoch Data -' go down to line 187 which contains keys
# map key to the other actigraphy mapping files
# create datatable until EOF
"""
data_keys = ['_id', 'studyid', 'subjectid', 'versionid', 'visitid', 'sessionid', 'filetype', 'fileformat', 'filepath']


def automated_parsing(file_info: dict) -> dict:
    """
    Parses the file at fileinfo['filepath']. Data and meta data are extracted according to the rules specified by
    file_info['fileformat']. Return file is dict (if sleep or score file) or list of dict objects (tabular data).
    Other parameters entered (subjectid, etc) will be passed through to the dict return object. If any
    of the data keys are the same as these extra parameters, they will be overwritten.

    This function is called by default on any file upload and will run if fileformat matches any of
    [sleep, edf, tabular, tabulardata, scorefile].

    """

    base_dictobj = {k: file_info[k] for k in data_keys if k in file_info}

    file_path = base_dictobj['filepath'].replace('./uploads/', uploads_path)
    try:
        # choose correct file type
        if base_dictobj['fileformat'] == "sleep" or base_dictobj['fileformat'] == 'edf':
            # call sleep parse function
            obj_ret = parse_edf_file_to_dict(file_path)
        elif base_dictobj['fileformat'] == 'scorefile':
            # call scoring file parse function
            obj_ret = parse_scorefile_to_dict(file_path, base_dictobj['studyid'])
        elif base_dictobj['fileformat'] == 'tabular' or base_dictobj['fileformat'] == 'tabulardata':
            # call tabulardata file parse function
            obj_ret = parse_tabular_file_to_dict(file_path)
        else:
            warnings.warn('- filetype is unknown, skipping')
            return None
    except AssertionError as e:
        warnings.warn('Problems parsing file. Error was:\n')
        print(e)
        return None

    #    elif sleepdiaries = filepath: TODO
    # call sleepdiaries parse function
    #    elif actigraphy = filepath:
    # call actigraphy parse function

    if type(obj_ret) == list:
        obj_out = []
        for obj in obj_ret:
            base_temp = base_dictobj.copy()
            base_temp.update(obj)
            obj_out.append(base_temp)
    else:
        obj_out = base_dictobj
        obj_out.update(obj_ret)
    return obj_out


if __name__ == '__main__':
    #This script should be automatically called every few minutes
    med_api = MednickAPI('http://saclab.ss.uci.edu:8000', 'PyAutoParser', password='1234')

    while True:
        file_infos = med_api.get_unparsed_files(active=True)
        if len(file_infos) > 0:
            print('Found', len(file_infos), 'unparsed files, beginning parse:')
            for file_info in file_infos:
                if 'fileName' in file_info:
                    print('Found old file')
                    continue
                print('\r Working on'+file_info['filename'], end='')
                data_out = automated_parsing(file_info)
                if data_out is not None:
                    for data in data_out:
                        med_api.upload_data(data, fid=file_info['_id'])
            print('\rCompleted parse. No errors. Sleeping for 30 seconds.')
        time.sleep(30)

