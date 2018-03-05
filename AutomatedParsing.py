import mne
import sys
import pandas as pd
import numpy
import ParsingScoring as ps
import ParsingEDF as pe
import ParsingPandas as pp
import json
import glob
import datetime


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

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
    @fileformat. Return file is JSON (if sleep or score file) or list of JSON objects (tabular data).
    Other parameters entered (subjectid, etc) will be passed through to the JSON return object. If any
    of the data keys are the same as these extra parameters, they will be overwritten.

    This function is called by default on any file upload and will run if fileformat matches any of
    [sleep, edf, tabular, tabulardata, scorefile].

    """
    jsonobj = []

    base_josnobj = {'studyid': studyid,
                    'subjectid': subjectid,
                    'visitid': visitid,
                    'session': sessionid,
                    'filetype': filetype,
                    'fileformat': fileformat}
    base_josnobj = dict((k, v) for k, v in base_josnobj.items() if v is not None)  # Remove None values

    # choose correct file type
    if fileformat == "sleep" or fileformat == 'edf':
        # call sleep parse function
        jsonobj = pe.EdfParse(filepath)
    elif fileformat == 'scorefile':
        # call scoring file parse function
        jsonobj = ps.parse_scoring_file(filepath, studyid)
    elif fileformat == 'tabular' or fileformat == 'tabulardata':
        # call tabulardata file parse function
        jsonobj = pp.parse_tabular_file_to_dict(filepath)
    else:
        raise ValueError('filetype is unknown')
    #    elif sleepdiaries = filepath:
    # call sleepdiaries parse function
    #    elif actigraphy = filepath:
    # call actigraphy parse function

    if type(jsonobj) is dict:
        base_josnobj.update(jsonobj)
        json_out = json.dumps(base_josnobj, cls=MyEncoder)
    elif type(jsonobj) is list:
        json_out = []
        for jsonobj_el in jsonobj:
            temp_base = base_josnobj
            temp_base.update(jsonobj_el)
            json_out.append(json.dumps(temp_base, cls=MyEncoder))

    return json_out

# for testing
if __name__ == "__main__":
    remote_folder_path = "/data/mednickdb/mednickdb_autoupload/"
    types_of_files_to_test = ['tabular']
    local_folder_path = "C:/Users/bdyet/UCIGoogleDrive/dataForDB/test_files/"
    for data_type in types_of_files_to_test:
        file_paths = glob.iglob(local_folder_path + data_type + '/' + '*')

        for file_path in file_paths:
            object, error, message = automated_parsing(file_path,
                                                       data_type,
                                                       studyid=file_path.split('\\')[-1].split('_')[0])
            print(object)
