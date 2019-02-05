from scipy.io import loadmat
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os
from mednickdb_pyapi import MednickAPI

module_path = os.path.dirname(os.path.abspath(__file__))

def hume_matfile_loader(matfile_path):
    """
    Loads a hume matlab .mat file which contains a struct, and writes fields and values to a dictionary
    :param matfile_path: path of matlab file to load
    :return: dict of matlab information
    """
    mat_struct = loadmat(matfile_path)

    # build a list of keys and values for each entry in the structure
    vals = mat_struct['stageData'][0, 0] 
    keys = mat_struct['stageData'][0, 0].dtype.descr

    # Assemble the keys and values into variables with the same name as that used in MATLAB
    mat_dict = {}
    for i in range(len(keys)):
        key = keys[i][0]
        if len(vals[key].shape) > 1 and vals[key].shape[0] > vals[key].shape[1]:
            vals[key] = vals[key].T
        if len(vals[key][0]) > 1:
            val = np.squeeze(vals[key][0])
        else:
            val = np.squeeze(vals[key][0][0])  # squeeze is used to covert matlat (1,n) arrays into numpy (1,) arrays.
        mat_dict[key] = val

    return mat_dict


def mat_datenum_to_py_datetime(mat_datenum):
    """
    Converts a matlab "datenum" type to a python datetime type
    :param mat_datenum: matlab datenum to conver
    :return: converted datetime
    """
    return datetime.fromordinal(int(mat_datenum)) + timedelta(days=mat_datenum % 1) - timedelta(days=366)


def get_stagemap(studyid, versionid):
    """
    Gets the map from for converting a scorefile's stages to the standard format used by the db. File is grabed from servers data staore.
    :param studyid: the studyid of the file.
    :return: the stagemap,a dict which converts one stage format to another
    :raises: FileNotFoundError if file was not found on the server
    """

    med_api = MednickAPI(server_address='http://saclab.ss.uci.edu:8000', username='mednickdb.microservices@gmail.com',
                         password=os.environ['MEDNICKDB_DEFAULT_PW'])
    stage_maps = med_api.get_data(studyid=studyid, versionid=versionid, filetype='stage_map')

    if stage_maps is None or len(stage_maps) == 0:
        raise FileNotFoundError('stagemap not found on database')

    stage_map = stage_maps[0]
    stage_map = {k.replace('stage_map.', ''): v for k, v in stage_map.items()}

    return stage_map

def get_stagemap_by_studyid(file, studyid):
    """
    Gets the map from for converting a scorefile's stages to the standard format used by the db. File is grabbed from stagemaps/ dir.
    :param studyid: the studyid of the file.
    :param file: The scorefile to parse
    :return: the stagemap,a dict which converts one stage format to another
    :raises: FileNotFoundError if file was not found on the server
    """
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

    print(module_path)
    stagemap = pd.read_excel(module_path+'/stagemaps/' + stagemap_type + '_stagemap.xlsx',
                             converters={'mapsfrom': str, 'mapsto': str})
    stage_map = {k: v for k, v in zip(stagemap['mapsfrom'], stagemap['mapsto'])}
    return stage_map