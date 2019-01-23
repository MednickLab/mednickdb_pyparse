from scipy.io import loadmat
from datetime import datetime, timedelta
import numpy as np


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