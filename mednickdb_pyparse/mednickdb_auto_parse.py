import mne
import sys
import pandas as pd
import numpy
from .parse_scorefile import parse_scorefile_to_dict
from .parse_edf import parse_edf_file_to_dict
from .parse_tabular import parse_tabular_file_to_dict
import glob
import datetime
from mednickdb_pyapi.mednickdb_pyapi import MednickAPI

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


def automated_parsing(filepath, filetype, fileformat, studyid, subjectid=None, visitid=None, sessionid=None):
    """
    Parses the file at @filepath. Data and meta data are extracted according to the rules specified by
    @fileformat. Return file is dict (if sleep or score file) or list of dict objects (tabular data).
    Other parameters entered (subjectid, etc) will be passed through to the dict return object. If any
    of the data keys are the same as these extra parameters, they will be overwritten.

    This function is called by default on any file upload and will run if fileformat matches any of
    [sleep, edf, tabular, tabulardata, scorefile].

    """

    base_dictobj = {'studyid': studyid,
                    'subjectid': subjectid,
                    'visitid': visitid,
                    'session': sessionid,
                    'filetype': filetype,
                    'fileformat': fileformat}
    base_dictobj = {k: v for k, v in base_dictobj.items() if v is not None}  # Remove None values

    # choose correct file type
    if fileformat == "sleep" or fileformat == 'edf':
        # call sleep parse function
        obj_ret = parse_edf_file_to_dict(filepath)
    elif fileformat == 'scorefile':
        # call scoring file parse function
        obj_ret = parse_scorefile_to_dict(filepath, studyid)
    elif fileformat == 'tabular' or fileformat == 'tabulardata':
        # call tabulardata file parse function
        obj_ret = parse_tabular_file_to_dict(filepath)
    else:
        raise ValueError('filetype is unknown')

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
    med_api = MednickAPI('http://localhost:8001', 'PyAutoParser')
    fids = med_api.get_unparsed_files()
    for fid in fids:
        f_info = med_api.file_info(fid)
        data_out = automated_parsing(**f_info)
        for data in data_out:
            med_api.upload_data(data, fid=fid)

