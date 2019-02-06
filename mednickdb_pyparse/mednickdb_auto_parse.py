import os
from inspect import signature
import time
import warnings
import logging
from typing import Union, List, Dict, Tuple
from parse_scorefile import parse_scorefile
from utils import get_stagemap, get_stagemap_by_studyid
from parse_edf import parse_eeg_file
from parse_tabular import parse_tabular_file
from mednickdb_pyapi import MednickAPI


debug = True


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("errors.log"),
        logging.StreamHandler()
    ])

uploads_path = './uploads/' if os.environ['HOME'] is None else '/data/mednick_server/file_uploads/'

if debug:
    print('Upload path', uploads_path)


def automated_parsing(file_specifiers=None, get_files_from_server_storage=False, **kwargs: dict) -> Union[list, None]:
    """
    Parses the file at fileinfo['filepath']. Data and meta data are extracted according to the rules specified by
    file_info['fileformat']. Return file is dict (if sleep or score file) or list of dict objects (tabular data).
    Other parameters entered (subjectid, etc) will be passed through to the dict return object. If any
    of the data keys are the same as these extra parameters, they will be overwritten.

    This function is called by default on any file upload and will run if fileformat matches any of
    [sleep_scoring, tabular, eeg, sleep_eeg]. sleep_eeg will parse sleep features, etc. TODO.

    :param: file_specifiers: file_specifiers dict, with at least filepath, fileformat, studyid of the file to parse (as downloaded from database).
    :param kwargs: some of all of the individual keys and values of the file info object (i.e. **file_info).
    minimum set is filepath, fileformat, studyid. Useful when parsing without the need for a server (i.e. just extracting data from files)
    :param: get_files_from_server_storage: If files paths should be reletive to server file storage location, or where this file is run from.
    :return: data object to upload to the database, may addtionally return files to post to database also
    """
    if file_specifiers is None:
        file_specifiers = kwargs

    elif kwargs is not None:
        file_specifiers.update(kwargs)

    file_path = file_specifiers['filepath']
    if get_files_from_server_storage:
        file_path = file_path.replace('uploads/', '')
        file_path = uploads_path + file_path

    try:
        # choose correct file type
        if file_specifiers['fileformat'] == "eeg" or file_specifiers['fileformat'] == "sleep_eeg":
            # call sleep parse function
            obj_ret = parse_eeg_file(file_path)
        elif file_specifiers['fileformat'] == 'sleep_scoring':
            # call scoring file parse function
            try:
                stage_map = get_stagemap(studyid=file_specifiers['studyid'], versionid=file_specifiers['versionid'])
            except FileNotFoundError:
                try:
                    stage_map = get_stagemap_by_studyid(file_specifiers['filepath'], file_specifiers['studyid'])
                except FileNotFoundError:
                    warnings.warn(file_specifiers['filepath']+' - Stagemap was not found. Skipping parse')
                    return None

            obj_ret = parse_scorefile(file_path, stage_map)
        elif file_specifiers['fileformat'] == 'tabular' or file_specifiers['fileformat'] == 'stage_map':
            # call tabulardata file parse function
            obj_ret = parse_tabular_file(file_path)
        #elif Add more fileformats here :)
        else:
            warnings.warn('- filetype is unknown, skipping')
            return None
    except AssertionError as e:
        warnings.warn('Problems parsing file. Error was:\n')
        print(e)
        return None

    if type(obj_ret) == list:
        obj_out = []
        for obj in obj_ret:
            base_temp = file_specifiers.copy()
            base_temp.update(obj)
            obj_out.append(base_temp)
    else:
        obj_out = file_specifiers
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

            med_api = MednickAPI(server_address='http://saclab.ss.uci.edu:8000', username='mednickdb.microservices@gmail.com', password=os.environ['MEDNICKDB_DEFAULT_PW']) #TODO pull from ENV
            upload_kwargs = [k for k, v in signature(med_api.upload_data).parameters.items()]
            file_infos = med_api.get_unparsed_files(previous_versions=False)
        except ConnectionError:
            time.sleep(5)
            continue # retry connection

        if len(file_infos) > 0: # There are files to parse
            print('Found', len(file_infos), 'unparsed files, beginning parse:')

        for file_info in file_infos:
            if file_info['filename'] in problem_files:
                continue
            try:
                print('\r Working on '+file_info['filename'])
                file_specifiers = {k: v for k, v in file_info.items() if k in upload_kwargs}
                data_out = automated_parsing(file_specifiers=file_specifiers,
                                             fileformat=file_info['fileformat'],
                                             filepath=file_info['filepath'],
                                             get_files_from_server_storage=True)
                if data_out is not None:
                    for idx, data in enumerate(data_out):
                        del data['filepath']
                        del data['fileformat']  # we don't want to have dead refs, and fid will fill this role
                        data_keys = list(data.keys())
                        data_specifiers = {k: v for k, v in file_info.items() if k in upload_kwargs}
                        data_specifiers.update({k:data.pop(k) for k in data_keys if k in upload_kwargs})
                        med_api.upload_data(data=data, fid=file_info['_id'], **data_specifiers)
                        if debug:
                            print('\r   Uploaded data row',idx+1,'of',len(data_out),'for',file_info['filename'])
                med_api.update_parsed_status(fid=file_info['_id'], status=True)

            except Exception as e:  # some kind of parsing error on a specific file
                if debug:
                    raise e
                else:
                    problem_files.append(file_info['filename'])
                    logging.exception('Problem file: ' + file_info['filename'])

        print('\rCompleted parse. Sleeping for', parse_rate, 'seconds. Logger has '+str(len(problem_files))+' problem files')
        time.sleep(parse_rate)


