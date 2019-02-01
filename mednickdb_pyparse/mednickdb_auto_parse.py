import os
from inspect import signature
print(os.getcwd())
import sys
'''
from mednickdb_pyparse.parse_scorefile import parse_scorefile
from mednickdb_pyparse.parse_edf import parse_eeg_file
from mednickdb_pyparse.parse_tabular import parse_tabular_file
'''
from parse_scorefile import parse_scorefile
from parse_edf import parse_eeg_file
from parse_tabular import parse_tabular_file

import time
import warnings


sys.path.append('../../mednickdb_pyapi/')
from mednickdb_pyapi.mednickdb_pyapi import MednickAPI
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("errors.log"),
        logging.StreamHandler()
    ])

uploads_path = './uploads/' if os.environ['HOME'] is None else '/data/mednick_server/file_uploads/'
print('Upload path', uploads_path)
"""
# fileformats are:
        Known parse-able fileformats are currently (others will be ignored by parsing microservices):
        - "sleep_scoring" - sleep scoring files. Currently supports edf, mat (hume), xml (NSRR), and various tabular types
        - "tabular" - any tabular-like data, with column headers and cols for specific subjectid, visitid, etc
        - "eeg" - edf's or other eeg like files. Basically anything the python package MNE can open
        TODO:
        - "actigraphy"
        - "sleep_diaries"

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
data_keys = ['_id', 'studyid', 'subjectid', 'versionid', 'visitid', 'sessionid', 'filetype', 'fileformat']


def automated_parsing(file_info=None, get_files_from_server_storage=False, **kwargs: dict) -> list:
    """
    Parses the file at fileinfo['filepath']. Data and meta data are extracted according to the rules specified by
    file_info['fileformat']. Return file is dict (if sleep or score file) or list of dict objects (tabular data).
    Other parameters entered (subjectid, etc) will be passed through to the dict return object. If any
    of the data keys are the same as these extra parameters, they will be overwritten.

    This function is called by default on any file upload and will run if fileformat matches any of
    [sleep_scoring, tabular, eeg, sleep_eeg]. sleep_eeg will parse sleep features, etc. TODO.

    :param: file_info: file_info dict of the file to parse (as downloaded from database).
    :param kwargs: some of all of the individual keys and values of the file info object (i.e. **file_info).
    minimum set is filepath, fileformat, studyid. Useful when parsing without the need for a server (i.e. just extracting data from files)
    :param: get_files_from_server_storage: If files paths should be reletive to server file storage location, or where this file is run from.
    :return: data object to upload to the database, may addtionally return files to post to database also
    """
    if file_info is None:
        file_info = kwargs

    file_path = file_info['filepath']
    if get_files_from_server_storage:
        file_path = file_path.replace('uploads/', '')
        file_path = uploads_path + file_path
    print(file_path)
    try:
        # choose correct file type
        if file_info['fileformat'] == "eeg" or file_info['fileformat'] == "sleep_eeg":
            # call sleep parse function
            obj_ret = parse_eeg_file(file_path)
        elif file_info['fileformat'] == 'sleep_scoring':
            # call scoring file parse function
            obj_ret = parse_scorefile(file_path, file_info['studyid'])
        elif file_info['fileformat'] == 'tabular':
            # call tabulardata file parse function
            obj_ret = parse_tabular_file(file_path)
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
            base_temp = file_info.copy()
            base_temp.update(obj)
            obj_out.append(base_temp)
    else:
        obj_out = file_info
        obj_out.update(obj_ret)
        obj_out = [obj_out]

    return obj_out


if __name__ == '__main__':
    """
    Automatic parsing routine. Will pull from the database every 5 seconds and try to parse whatever is marked as unparsed
    If some error occurs, this is logged but not raised too, so that the regular db can continue as normal.
    TODO: we should probably alert an admin in this case (somehow, automatic email?)
    """
    parse_rate = 5 #seconds per DB query
    problem_files = []
    while True: #Run indefinatly
        try:
            #med_api = MednickAPI('http://saclab.ss.uci.edu:8000', 'PyAutoParser', password='1234')
            med_api = MednickAPI('PyAutoParser', password='1234')
            upload_kwargs = [k for k, v in signature(med_api.upload_data).parameters.items()]
            file_infos = med_api.get_unparsed_files(previous_versions=False)
        except ConnectionError:
            continue # retry connection

        if len(file_infos) > 0:
            print('Found', len(file_infos), 'unparsed files, beginning parse:')

            for file_info in file_infos:
                if file_info['filename'] in problem_files:
                    continue
                try:
                    print('\r Working on '+file_info['filename'])
                    data_out = automated_parsing(file_info=file_info, get_files_from_server_storage=True)
                    if data_out is not None:
                        for data in data_out:
                            del data['filepath']  # we don't want to have dead refs, and fid will fill this role
                            file_specifiers = {k: v for k, v in file_info.items() if k in upload_kwargs}
                            data_keys = list(data.keys())
                            file_specifiers.update({k:data.pop(k) for k in data_keys if k in upload_kwargs})
                            med_api.upload_data(data=data, fid=file_info['_id'], **file_specifiers)
                            print('Uploaded a data row for', file_info['filename'])
                            print(med_api.get_data(**file_specifiers))
                    med_api.update_parsed_status(fid=file_info['_id'], status=True)

                except:  # some kind of parsing error on a specific file
                    problem_files.append(file_info['filename'])
                    logging.exception('Problem file: ' + file_info['filename'])

        print('\rCompleted parse. Sleeping for', parse_rate, 'seconds. Logger has '+str(len(problem_files))+' problem files')
        time.sleep(parse_rate)


