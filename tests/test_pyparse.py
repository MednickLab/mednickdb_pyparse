import sys, os
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../mednickdb_pyparse')
from mednickdb_pyparse.mednickdb_auto_parse import automated_parsing
import datetime
"""tests for python parsing part of mednickdb"""

def test_multiline_tabular():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/testtabular1.xlsx"),
                                 fileformat="tabular",
                                 filetype="demographics",
                                 studyid="ExampleStudyA")
    s1 = {
        'filepath':os.path.join(os.path.dirname(__file__),"testfiles/testtabular1.xlsx"),
        "studyid": "ExampleStudyA",
        "filetype": "demographics",
        "fileformat": "tabular",
        "subjectid": 1,
        "age": 18,
        "sex": "M",
        "bmi": 22
    }

    s2 = {
        'filepath':os.path.join(os.path.dirname(__file__),"testfiles/testtabular1.xlsx"),
        "studyid": "ExampleStudyA",
        "filetype": "demographics",
        "fileformat": "tabular",
        "subjectid": 2,
        "age": 22,
        "sex": "F",
        "bmi": 23
    }

    s3 = {
        'filepath':os.path.join(os.path.dirname(__file__),"testfiles/testtabular1.xlsx"),
        "studyid": "ExampleStudyA",
        "filetype": "demographics",
        "fileformat": "tabular",
        "subjectid": 3,
        "age": 20,
        "sex": "M",
        "bmi": 19
    }

    correct_return = [s1, s2, s3]
    assert(all([True if dict_out[i] == corr_item else False for i, corr_item in enumerate(correct_return)]))


def test_example_task_data():
    """Task data is structured in some tabular format, and should be indexed by subject, visit, session"""
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/testexampletask1.xlsx"),
                                 fileformat="tabular",
                                 filetype="ExampleTask1",
                                 studyid="ExampleStudyA")

    line1 = {
        'filepath':os.path.join(os.path.dirname(__file__),"testfiles/testexampletask1.xlsx"),
        "studyid": "ExampleStudyA",
        "filetype": "ExampleTask1",
        "fileformat": "tabular",
        "subjectid": 1.0,
        "visitid": 1.0,
        "sessionid": 1.0,
        "accuracy": 0.9,
        "rt": 30.0
    }

    line2 = {
        'filepath': os.path.join(os.path.dirname(__file__),"testfiles/testexampletask1.xlsx"),
        "studyid": "ExampleStudyA",
        "filetype": "ExampleTask1",
        "fileformat": "tabular",
        "subjectid": 1.0,
        "visitid": 2.0,
        "sessionid": 1.0,
        "accuracy": 0.8,
        "rt": 50.0
    }

    line3 = {
        'filepath': os.path.join(os.path.dirname(__file__),"testfiles/testexampletask1.xlsx"),
        "studyid": "ExampleStudyA",
        "filetype": "ExampleTask1",
        "fileformat": "tabular",
        "subjectid": 2.0,
        "visitid": 1.0,
        "sessionid": 1.0,
        "accuracy": 0.5,
        "rt": 20.0
    }

    line4 = {
        'filepath':os.path.join(os.path.dirname(__file__), "testfiles/testexampletask1.xlsx"),
        "studyid": "ExampleStudyA",
        "filetype": "ExampleTask1",
        "fileformat": "tabular",
        "subjectid": 2.0,
        "visitid": 2.0,
        "sessionid": 1.0,
        "accuracy": 0.8,
        "rt": 50.0
    }

    correct_return = [line1, line2, line3, line4]

    assert(all([True if dict_out[i] == corr_item else False for i, corr_item  in enumerate(correct_return)]))


def test_edf_parse():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/edf1.edf"),
                                 fileformat="sleep_eeg",
                                 filetype="sleep_eeg",
                                 subjectid=1,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="ExampleStudyA")[0]

    correct_return = {
        'filepath':os.path.join(os.path.dirname(__file__),"testfiles/edf1.edf"),
        "studyid": "ExampleStudyA",
        "subjectid": 1,
        "visitid": 1,
        "sessionid": 1,
        "filetype": "sleep_eeg",
        "fileformat": "sleep_eeg",
        "eeg_meas_date": datetime.datetime(2002, 12, 31, 16, 25, 37),
        "eeg_nchan": 14,
        "eeg_sfreq": 128.0,
        "eeg_subject_info": None,
        "eeg_ch_names": ["Lefteye", "RightEye", "EMG", "C3A2", "C4A1", "ECG", "SpO2", "Soud", "Flow", "Sum", "ribcage",
                         "abdo", "BodyPos", "Pulse"]
    }

    assert (dict_out == correct_return)


def test_hume1_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/humetype1_scorefile.mat"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="GSF")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/humetype1_scorefile.mat'), 'fileformat': 'sleep_scoring', 'filetype': 'sleep_scoring',
                      'subjectid': 2, 'visitid': 1, 'sessionid': 1, 'studyid': 'GSF',
                      'starttime': datetime.datetime(2016, 1, 1, 0, 1, 42, 841003),
                      'mins_in_waso': 0.0, 'mins_in_stage1': 1.0, 'mins_in_stage2': 2.0,
                      'mins_in_sws': 1.0, 'mins_in_rem': 0, 'sleep_efficiency': 1.0, 'total_sleep_time': 4.0,
                      'sleep_latency': 1.0, 'num_awakenings': 0, 'trans_prob_from_waso': [None, None, None, None, None],
                      'trans_prob_from_stage1': [0.0, 0.0, 1.0, 0.0, 0.0], 'trans_prob_from_stage2': [0.0, 0.0, 0.0, 1.0, 0.0],
                      'trans_prob_from_sws': [0.0, 0.0, 1.0, 0.0, 0.0], 'trans_prob_from_rem': [None, None, None, None, None],}

    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


def test_hume2_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/humetype2_scorefile.mat"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="GSF")[0]

    correct_return = {'filepath': '/data/microservices/mednickdb_pyparse/tests/testfiles/humetype2_scorefile.mat',
                      'fileformat': 'sleep_scoring', 'filetype': 'sleep_scoring', 'versionid': 1, 'subjectid': 2,
                      'visitid': 1, 'sessionid': 1, 'studyid': 'GSF', 'starttime': None, 'epoch_len': 30,
                      'mins_in_waso': 20.5, 'mins_in_stage1': 6.5, 'mins_in_stage2': 308.0, 'mins_in_sws': 98.5,
                      'mins_in_rem': 158.5, 'sleep_efficiency': 0.9653716216216216, 'total_sleep_time': 571.5,
                      'sleep_latency': 16.0, 'num_awakenings': 32,
                      'trans_prob_from_waso': [0.0, 0.15625, 0.46875, 0.03125, 0.34375], 'trans_prob_from_stage1':
                          [0.3333333333333333, 0.0, 0.6666666666666666, 0.0, 0.0], 'trans_prob_from_stage2':
                          [0.3076923076923077, 0.0, 0.0, 0.5192307692307693, 0.17307692307692307],
                      'trans_prob_from_sws': [0.07142857142857142, 0.0, 0.9285714285714286, 0.0, 0.0],
                      'trans_prob_from_rem': [0.6, 0.0, 0.4, 0.0, 0.0], 'average_bout_duration_waso': 0.640625,
                      'average_bout_duration_stage1': 1.0833333333333333, 'average_bout_duration_stage2': 5.811320754716981,
                      'average_bout_duration_sws': 3.517857142857143, 'average_bout_duration_rem': 7.925}
    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


def test_grass_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/grasstype_scorefile.xls"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="ExampleStudyA")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/grasstype_scorefile.xls'), 'fileformat': 'sleep_scoring', 'filetype': 'sleep_scoring',
                      'versionid': 1, 'subjectid': 2, 'visitid': 1, 'sessionid': 1, 'studyid': 'ExampleStudyA',
                      'starttime': datetime.datetime(2013, 2, 18, 12, 58, 59),
                      'epoch_len': 30, 'mins_in_waso': 28.0, 'mins_in_stage1': 10.0, 'mins_in_stage2': 23.0, 'mins_in_sws': 34.0,
                      'mins_in_rem': 16.0, 'sleep_efficiency': 0.7477477477477478, 'total_sleep_time': 83.0, 'sleep_latency': 39.5,
                      'num_awakenings': 14, 'trans_prob_from_waso': [0.0, 0.9285714285714286, 0.0, 0.0, 0.07142857142857142],
                      'trans_prob_from_stage1': [0.3333333333333333, 0.0, 0.5333333333333333, 0.0, 0.13333333333333333],
                      'trans_prob_from_stage2': [0.625, 0.125, 0.0, 0.125, 0.125], 'trans_prob_from_sws': [1.0, 0.0, 0.0, 0.0, 0.0],
                      'trans_prob_from_rem': [1.0, 0.0, 0.0, 0.0, 0.0], 'average_bout_duration_rem': 4.0,
                      'average_bout_duration_stage1': 0.6666666666666666, 'average_bout_duration_stage2': 2.875,
                      'average_bout_duration_sws': 34.0,
                      'average_bout_duration_waso': 2.0}

    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


def test_lat_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/lattype_scorefile.txt"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="SpencerLab")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/lattype_scorefile.txt'), 'fileformat': 'sleep_scoring',
                      'filetype': 'sleep_scoring', 'versionid': 1, 'subjectid': 2, 'visitid': 1,
                      'sessionid': 1, 'studyid': 'SpencerLab',
                      'epoch_len': 30, 'mins_in_waso': 7.0, 'mins_in_stage1': 9.5, 'mins_in_stage2': 33.0,
                      'mins_in_sws': 16.5, 'mins_in_rem': 29.5, 'sleep_efficiency': 0.9267015706806283,
                      'total_sleep_time': 88.5, 'sleep_latency': 5.5, 'num_awakenings': 12,
                      'trans_prob_from_waso': [0.0, 0.75, 0.16666666666666666, 0.0, 0.08333333333333333],
                      'trans_prob_from_stage1': [0.4375, 0.0, 0.5, 0.0, 0.0625],
                      'trans_prob_from_stage2': [0.16666666666666666, 0.25, 0.0, 0.16666666666666666, 0.4166666666666667],
                      'trans_prob_from_sws': [0.5, 0.0, 0.5, 0.0, 0.0],
                      'trans_prob_from_rem': [0.3333333333333333, 0.5, 0.16666666666666666, 0.0, 0.0],
                      'average_bout_duration_waso': 0.5833333333333334,
                      'average_bout_duration_stage1': 0.59375,
                      'average_bout_duration_stage2': 2.75,
                      'average_bout_duration_sws': 8.25,
                      'average_bout_duration_rem': 4.214285714285714}

    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


def test_basic_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/basictype_scorefile.txt"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="DinklemannLab")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/basictype_scorefile.txt'), 'fileformat': 'sleep_scoring',
                      'filetype': 'sleep_scoring', 'versionid': 1, 'subjectid': 2, 'visitid': 1, 'sessionid': 1,
                      'studyid': 'DinklemannLab',
                      'epoch_len': 30, 'mins_in_waso': 18.0, 'mins_in_stage1': 27.5, 'mins_in_stage2': 270.5,
                      'mins_in_sws': 60.5, 'mins_in_rem': 73.0, 'sleep_efficiency': 0.9599555061179088,
                      'total_sleep_time': 431.5, 'sleep_latency': 6.5, 'num_awakenings': 19,
                      'trans_prob_from_waso': [0.0, 1.0, 0.0, 0.0, 0.0], 'trans_prob_from_stage1': [0.34375, 0.0, 0.625, 0.0, 0.03125],
                      'trans_prob_from_stage2': [0.14583333333333334, 0.16666666666666666, 0.0, 0.5416666666666666, 0.14583333333333334],
                      'trans_prob_from_sws': [0.0, 0.0, 1.0, 0.0, 0.0], 'trans_prob_from_rem': [0.125, 0.5, 0.375, 0.0, 0.0],
                      'average_bout_duration_waso': 0.9473684210526315, 'average_bout_duration_stage1': 0.859375,
                      'average_bout_duration_stage2': 5.303921568627451, 'average_bout_duration_sws': 2.326923076923077,
                      'average_bout_duration_rem': 8.11111111111111}

    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


def test_full_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/fulltype_scorefile.txt"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="CAPStudy")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/fulltype_scorefile.txt'), 'fileformat': 'sleep_scoring',
                      'filetype': 'sleep_scoring', 'versionid': 1, 'subjectid': 2, 'visitid': 1,
                      'sessionid': 1, 'studyid': 'CAPStudy', 'startime': datetime.datetime(2010, 1, 28, 22, 18, 17),
                      'epoch_len': 30, 'mins_in_waso': 41.0, 'mins_in_stage1': 45.5, 'mins_in_stage2': 241.0,
                      'mins_in_sws': 83.5, 'mins_in_rem': 89.5, 'sleep_efficiency': 0.9180819180819181,
                      'total_sleep_time': 459.5, 'sleep_latency': 6.5, 'num_awakenings': 20,
                      'trans_prob_from_waso': [0.0, 0.95, 0.05, 0.0, 0.0],
                      'trans_prob_from_stage1': [0.16, 0.0, 0.84, 0.0, 0.0],
                      'trans_prob_from_stage2': [0.3, 0.16666666666666666, 0.0, 0.3333333333333333, 0.2],
                      'trans_prob_from_sws': [0.1, 0.0, 0.9, 0.0, 0.0], 'trans_prob_from_rem': [1.0, 0.0, 0.0, 0.0, 0.0],
                      'average_bout_duration_waso': 2.05, 'average_bout_duration_stage1': 1.82,
                      'average_bout_duration_stage2': 7.303030303030303, 'average_bout_duration_sws': 8.35,
                      'average_bout_duration_rem': 14.916666666666666}
    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


def test_XML_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/xmltype_scorefile.xml"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="NSRR")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/xmltype_scorefile.xml'), 'fileformat': 'sleep_scoring',
                      'filetype': 'sleep_scoring', 'versionid': 1, 'subjectid': 2, 'visitid': 1,
                      'sessionid': 1, 'studyid': 'NSRR', 'starttime': datetime.datetime(1900, 1, 1, 20, 33, 32),
                      'epoch_len': 30, 'mins_in_waso': 28.5, 'mins_in_stage1': 18.5, 'mins_in_stage2': 209.5,
                      'mins_in_sws': 141.0, 'mins_in_rem': 121.0, 'sleep_efficiency': 0.9450337512054002,
                      'total_sleep_time': 490.0, 'sleep_latency': 167.0, 'num_awakenings': 20,
                      'trans_prob_from_waso': [0.0, 0.55, 0.2, 0.05, 0.2],
                      'trans_prob_from_stage1': [0.1875, 0.0, 0.625, 0.0, 0.1875],
                      'trans_prob_from_stage2': [0.3333333333333333, 0.0, 0.0, 0.48148148148148145, 0.18518518518518517],
                      'trans_prob_from_sws': [0.14285714285714285, 0.0, 0.7857142857142857, 0.0, 0.07142857142857142],
                      'trans_prob_from_rem': [0.46153846153846156, 0.3076923076923077, 0.23076923076923078, 0.0, 0.0],
                      'average_bout_duration_waso': 1.425, 'average_bout_duration_stage1': 1.15625,
                      'average_bout_duration_stage2': 7.482142857142857, 'average_bout_duration_sws': 10.071428571428571,
                      'average_bout_duration_rem': 9.307692307692308}

    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


# def test_edf1_scorefile():
#     dict_out = automated_parsing(filepath="testfiles/edftype1_scorefile.edf",
#                                  fileformat='sleep_scoring',
#                                  filetype='sleep_scoring', versionid=1,
#                                  subjectid=2,
#                                  visitid=1,
#                                  sessionid=1,
#                                  studyid="WamsleyLab")[0]
#     correct_return = {
#         "filepath":"testfiles/edftype1_scorefile.edf",
#         "studyid": "WamsleyLab",
#         "subjectid": 2,
#         "visitid": 1,
#         "sessionid": 1,
#         "filetype": "sleep_scoring",
#         "fileformat": "sleep_scoring",
#         "epochstage": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                        0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,
#                        1, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0,
#                        0, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0, 0, 1, 1, 2, 2, 2, 2, 0, 1, 1, 1, 1, 0, 0,
#                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
#                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                        0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,
#                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
#                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 2, 2, 2, 4, 4, 2, 4, 4, 2,
#                        4, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2,
#                        2, 2, 2, 2, 2, 4, 4, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3,
#                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
#                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 2, 3, 3, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4,
#                        4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 0, 0, 1,
#                        1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4,
#                        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
#                        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
#                        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 0,
#                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
#                        0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#                        2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
#                        4, 4, 4, 4, 4, 4, 4, 0, 1, 1, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
#                        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2],
#         "epochoffset": [0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0, 360.0, 390.0,
#                         420.0, 450.0, 480.0, 510.0, 540.0, 570.0, 600.0, 630.0, 660.0, 690.0, 720.0, 750.0, 780.0,
#                         810.0, 840.0, 870.0, 900.0, 930.0, 960.0, 990.0, 1020.0, 1050.0, 1080.0, 1110.0, 1140.0, 1170.0,
#                         1200.0, 1230.0, 1260.0, 1290.0, 1320.0, 1350.0, 1380.0, 1410.0, 1440.0, 1470.0, 1500.0, 1530.0,
#                         1560.0, 1590.0, 1620.0, 1650.0, 1680.0, 1710.0, 1740.0, 1770.0, 1800.0, 1830.0, 1860.0, 1890.0,
#                         1920.0, 1950.0, 1980.0, 2010.0, 2040.0, 2070.0, 2100.0, 2130.0, 2160.0, 2190.0, 2220.0, 2250.0,
#                         2280.0, 2310.0, 2340.0, 2370.0, 2400.0, 2430.0, 2460.0, 2490.0, 2520.0, 2550.0, 2580.0, 2610.0,
#                         2640.0, 2670.0, 2700.0, 2730.0, 2760.0, 2790.0, 2820.0, 2850.0, 2880.0, 2910.0, 2940.0, 2970.0,
#                         3000.0, 3030.0, 3060.0, 3090.0, 3120.0, 3150.0, 3180.0, 3210.0, 3240.0, 3270.0, 3300.0, 3330.0,
#                         3360.0, 3390.0, 3420.0, 3450.0, 3480.0, 3510.0, 3540.0, 3570.0, 3600.0, 3630.0, 3660.0, 3690.0,
#                         3720.0, 3750.0, 3780.0, 3810.0, 3840.0, 3870.0, 3900.0, 3930.0, 3960.0, 3990.0, 4020.0, 4050.0,
#                         4080.0, 4110.0, 4140.0, 4170.0, 4200.0, 4230.0, 4260.0, 4290.0, 4320.0, 4350.0, 4380.0, 4410.0,
#                         4440.0, 4470.0, 4500.0, 4530.0, 4560.0, 4590.0, 4620.0, 4650.0, 4680.0, 4710.0, 4740.0, 4770.0,
#                         4800.0, 4830.0, 4860.0, 4890.0, 4920.0, 4950.0, 4980.0, 5010.0, 5040.0, 5070.0, 5100.0, 5130.0,
#                         5160.0, 5190.0, 5220.0, 5250.0, 5280.0, 5310.0, 5340.0, 5370.0, 5400.0, 5430.0, 5460.0, 5490.0,
#                         5520.0, 5550.0, 5580.0, 5610.0, 5640.0, 5670.0, 5700.0, 5730.0, 5760.0, 5790.0, 5820.0, 5850.0,
#                         5880.0, 5910.0, 5940.0, 5970.0, 6000.0, 6030.0, 6060.0, 6090.0, 6120.0, 6150.0, 6180.0, 6210.0,
#                         6240.0, 6270.0, 6300.0, 6330.0, 6360.0, 6390.0, 6420.0, 6450.0, 6480.0, 6510.0, 6540.0, 6570.0,
#                         6600.0, 6630.0, 6660.0, 6690.0, 6720.0, 6750.0, 6780.0, 6810.0, 6840.0, 6870.0, 6900.0, 6930.0,
#                         6960.0, 6990.0, 7020.0, 7050.0, 7080.0, 7110.0, 7140.0, 7170.0, 7200.0, 7230.0, 7260.0, 7290.0,
#                         7320.0, 7350.0, 7380.0, 7410.0, 7440.0, 7470.0, 7500.0, 7530.0, 7560.0, 7590.0, 7620.0, 7650.0,
#                         7680.0, 7710.0, 7740.0, 7770.0, 7800.0, 7830.0, 7860.0, 7890.0, 7920.0, 7950.0, 7980.0, 8010.0,
#                         8040.0, 8070.0, 8100.0, 8130.0, 8160.0, 8190.0, 8220.0, 8250.0, 8280.0, 8310.0, 8340.0, 8370.0,
#                         8400.0, 8430.0, 8460.0, 8490.0, 8520.0, 8550.0, 8580.0, 8610.0, 8640.0, 8670.0, 8700.0, 8730.0,
#                         8760.0, 8790.0, 8820.0, 8850.0, 8880.0, 8910.0, 8940.0, 8970.0, 9000.0, 9030.0, 9060.0, 9090.0,
#                         9120.0, 9150.0, 9180.0, 9210.0, 9240.0, 9270.0, 9300.0, 9330.0, 9360.0, 9390.0, 9420.0, 9450.0,
#                         9480.0, 9510.0, 9540.0, 9570.0, 9600.0, 9630.0, 9660.0, 9690.0, 9720.0, 9750.0, 9780.0, 9810.0,
#                         9840.0, 9870.0, 9900.0, 9930.0, 9960.0, 9990.0, 10020.0, 10050.0, 10080.0, 10110.0, 10140.0,
#                         10170.0, 10200.0, 10230.0, 10260.0, 10290.0, 10320.0, 10350.0, 10380.0, 10410.0, 10440.0,
#                         10470.0, 10500.0, 10530.0, 10560.0, 10590.0, 10620.0, 10650.0, 10680.0, 10710.0, 10740.0,
#                         10770.0, 10800.0, 10830.0, 10860.0, 10890.0, 10920.0, 10950.0, 10980.0, 11010.0, 11040.0,
#                         11070.0, 11100.0, 11130.0, 11160.0, 11190.0, 11220.0, 11250.0, 11280.0, 11310.0, 11340.0,
#                         11370.0, 11400.0, 11430.0, 11460.0, 11490.0, 11520.0, 11550.0, 11580.0, 11610.0, 11640.0,
#                         11670.0, 11700.0, 11730.0, 11760.0, 11790.0, 11820.0, 11850.0, 11880.0, 11910.0, 11940.0,
#                         11970.0, 12000.0, 12030.0, 12060.0, 12090.0, 12120.0, 12150.0, 12180.0, 12210.0, 12240.0,
#                         12270.0, 12300.0, 12330.0, 12360.0, 12390.0, 12420.0, 12450.0, 12480.0, 12510.0, 12540.0,
#                         12570.0, 12600.0, 12630.0, 12660.0, 12690.0, 12720.0, 12750.0, 12780.0, 12810.0, 12840.0,
#                         12870.0, 12900.0, 12930.0, 12960.0, 12990.0, 13020.0, 13050.0, 13080.0, 13110.0, 13140.0,
#                         13170.0, 13200.0, 13230.0, 13260.0, 13290.0, 13320.0, 13350.0, 13380.0, 13410.0, 13440.0,
#                         13470.0, 13500.0, 13530.0, 13560.0, 13590.0, 13620.0, 13650.0, 13680.0, 13710.0, 13740.0,
#                         13770.0, 13800.0, 13830.0, 13860.0, 13890.0, 13920.0, 13950.0, 13980.0, 14010.0, 14040.0,
#                         14070.0, 14100.0, 14130.0, 14160.0, 14190.0, 14220.0, 14250.0, 14280.0, 14310.0, 14340.0,
#                         14370.0, 14400.0, 14430.0, 14460.0, 14490.0, 14520.0, 14550.0, 14580.0, 14610.0, 14640.0,
#                         14670.0, 14700.0, 14730.0, 14760.0, 14790.0, 14820.0, 14850.0, 14880.0, 14910.0, 14940.0,
#                         14970.0, 15000.0, 15030.0, 15060.0, 15090.0, 15120.0, 15150.0, 15180.0, 15210.0, 15240.0,
#                         15270.0, 15300.0, 15330.0, 15360.0, 15390.0, 15420.0, 15450.0, 15480.0, 15510.0, 15540.0,
#                         15570.0, 15600.0, 15630.0, 15660.0, 15690.0, 15720.0, 15750.0, 15780.0, 15810.0, 15840.0,
#                         15870.0, 15900.0, 15930.0, 15960.0, 15990.0, 16020.0, 16050.0, 16080.0, 16110.0, 16140.0,
#                         16170.0, 16200.0, 16230.0, 16260.0, 16290.0, 16320.0, 16350.0, 16380.0, 16410.0, 16440.0,
#                         16470.0, 16500.0, 16530.0, 16560.0, 16590.0, 16620.0, 16650.0, 16680.0, 16710.0, 16740.0,
#                         16770.0, 16800.0, 16830.0, 16860.0, 16890.0, 16920.0, 16950.0, 16980.0, 17010.0, 17040.0,
#                         17070.0, 17100.0, 17130.0, 17160.0, 17190.0, 17220.0, 17250.0, 17280.0, 17310.0, 17340.0,
#                         17370.0, 17400.0, 17430.0, 17460.0, 17490.0, 17520.0, 17550.0, 17580.0, 17610.0, 17640.0,
#                         17670.0, 17700.0, 17730.0, 17760.0, 17790.0, 17820.0, 17850.0, 17880.0, 17910.0, 17940.0,
#                         17970.0, 18000.0, 18030.0, 18060.0, 18090.0, 18120.0, 18150.0, 18180.0, 18210.0, 18240.0,
#                         18270.0, 18300.0, 18330.0, 18360.0, 18390.0, 18420.0, 18450.0, 18480.0, 18510.0, 18540.0,
#                         18570.0, 18600.0, 18630.0, 18660.0, 18690.0, 18720.0, 18750.0, 18780.0, 18810.0, 18840.0,
#                         18870.0, 18900.0, 18930.0, 18960.0, 18990.0, 19020.0, 19050.0, 19080.0, 19110.0, 19140.0,
#                         19170.0, 19200.0, 19230.0, 19260.0, 19290.0, 19320.0, 19350.0, 19380.0, 19410.0, 19440.0,
#                         19470.0, 19500.0, 19530.0, 19560.0, 19590.0, 19620.0, 19650.0, 19680.0, 19710.0, 19740.0,
#                         19770.0, 19800.0, 19830.0, 19860.0, 19890.0, 19920.0, 19950.0, 19980.0, 20010.0, 20040.0,
#                         20070.0, 20100.0, 20130.0, 20160.0, 20190.0, 20220.0, 20250.0, 20280.0, 20310.0, 20340.0,
#                         20370.0, 20400.0, 20430.0, 20460.0, 20490.0, 20520.0, 20550.0, 20580.0, 20610.0, 20640.0,
#                         20670.0, 20700.0, 20730.0, 20760.0, 20790.0, 20820.0, 20850.0, 20880.0, 20910.0, 20940.0,
#                         20970.0, 21000.0, 21030.0, 21060.0, 21090.0, 21120.0, 21150.0, 21180.0, 21210.0, 21240.0,
#                         21270.0, 21300.0, 21330.0, 21360.0, 21390.0, 21420.0, 21450.0, 21480.0, 21510.0, 21540.0,
#                         21570.0, 21600.0, 21630.0, 21660.0, 21690.0, 21720.0, 21750.0, 21780.0, 21810.0, 21840.0,
#                         21870.0, 21900.0, 21930.0, 21960.0, 21990.0, 22020.0, 22050.0, 22080.0, 22110.0, 22140.0,
#                         22170.0, 22200.0, 22230.0, 22260.0, 22290.0, 22320.0, 22350.0, 22380.0, 22410.0, 22440.0,
#                         22470.0, 22500.0, 22530.0, 22560.0, 22590.0, 22620.0, 22650.0, 22680.0, 22710.0, 22740.0,
#                         22770.0, 22800.0, 22830.0, 22860.0, 22890.0, 22920.0, 22950.0, 22980.0, 23010.0, 23040.0,
#                         23070.0, 23100.0, 23130.0, 23160.0, 23190.0, 23220.0, 23250.0, 23280.0, 23310.0, 23340.0,
#                         23370.0, 23400.0, 23430.0, 23460.0, 23490.0, 23520.0, 23550.0, 23580.0, 23610.0, 23640.0,
#                         23670.0, 23700.0, 23730.0, 23760.0, 23790.0, 23820.0, 23850.0, 23880.0, 23910.0, 23940.0,
#                         23970.0, 24000.0, 24030.0, 24060.0, 24090.0, 24120.0, 24150.0, 24180.0, 24210.0, 24240.0,
#                         24270.0, 24300.0, 24330.0, 24360.0, 24390.0, 24420.0, 24450.0, 24480.0, 24510.0, 24540.0,
#                         24570.0, 24600.0, 24630.0, 24660.0, 24690.0, 24720.0, 24750.0, 24780.0, 24810.0, 24840.0,
#                         24870.0, 24900.0, 24930.0, 24960.0, 24990.0, 25020.0, 25050.0, 25080.0, 25110.0, 25140.0,
#                         25170.0, 25200.0, 25230.0, 25260.0, 25290.0, 25320.0, 25350.0, 25380.0, 25410.0, 25440.0,
#                         25470.0, 25500.0, 25530.0, 25560.0, 25590.0, 25620.0, 25650.0, 25680.0, 25710.0, 25740.0,
#                         25770.0, 25800.0, 25830.0, 25860.0, 25890.0, 25920.0, 25950.0, 25980.0, 26010.0, 26040.0,
#                         26070.0, 26100.0, 26130.0, 26160.0, 26190.0, 26220.0, 26250.0, 26280.0, 26310.0, 26340.0,
#                         26370.0, 26400.0, 26430.0, 26460.0, 26490.0, 26520.0, 26550.0, 26580.0, 26610.0, 26640.0,
#                         26670.0, 26700.0, 26730.0, 26760.0, 26790.0, 26820.0, 26850.0, 26880.0, 26910.0, 26940.0,
#                         26970.0, 27000.0, 27030.0, 27060.0, 27090.0, 27120.0, 27150.0, 27180.0, 27210.0, 27240.0,
#                         27270.0, 27300.0, 27330.0, 27360.0, 27390.0, 27420.0, 27450.0, 27480.0, 27510.0, 27540.0,
#                         27570.0, 27600.0, 27630.0, 27660.0, 27690.0, 27720.0, 27750.0, 27780.0, 27810.0, 27840.0,
#                         27870.0, 27900.0, 27930.0, 27960.0, 27990.0, 28020.0, 28050.0, 28080.0, 28110.0, 28140.0,
#                         28170.0, 28200.0, 28230.0, 28260.0, 28290.0, 28320.0, 28350.0, 28380.0, 28410.0, 28440.0,
#                         28470.0, 28500.0, 28530.0, 28560.0, 28590.0, 28620.0, 28650.0, 28680.0, 28710.0, 28740.0,
#                         28770.0, 28800.0, 28830.0, 28860.0, 28890.0, 28920.0, 28950.0, 28980.0, 29010.0, 29040.0,
#                         29070.0, 29100.0, 29130.0, 29160.0, 29190.0, 29220.0, 29250.0, 29280.0, 29310.0, 29340.0,
#                         29370.0, 29400.0, 29430.0, 29460.0, 29490.0, 29520.0, 29550.0, 29580.0, 29610.0, 29640.0,
#                         29670.0, 29700.0, 29730.0, 29760.0, 29790.0, 29820.0, 29850.0, 29880.0, 29910.0, 29940.0,
#                         29970.0, 30000.0, 30030.0, 30060.0, 30090.0, 30120.0, 30150.0, 30180.0, 30210.0, 30240.0,
#                         30270.0, 30300.0, 30330.0, 30360.0, 30390.0, 30420.0, 30450.0, 30480.0, 30510.0, 30540.0,
#                         30570.0, 30600.0, 30630.0, 30660.0],
#         "starttime": datetime.datetime(2013, 10, 18, 16, 40, 6),
#         "mins_in_waso": 97.0, "mins_in_stage1": 45.0, "mins_in_stage2": 168.0, "mins_in_sws": 89.5, "mins_in_rem": 112.0,
#         "sleep_efficiency": 0.8103616813294232, "total_sleep_time": 414.5
#     }
#
#     assert (dict_out == correct_return)


def test_edf2_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/edftype2_scorefile.edf"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="Kemp")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/edftype2_scorefile.edf'), 'fileformat': 'sleep_scoring', 'filetype': 'sleep_scoring', 'versionid': 1, 'subjectid': 2, 'visitid': 1, 'sessionid': 1, 'studyid': 'Kemp', 'epoch_len': 30, 'mins_in_waso': 34.0, 'mins_in_stage1': 29.0, 'mins_in_stage2': 125.0, 'mins_in_sws': 110.0, 'mins_in_rem': 62.5, 'sleep_efficiency': 0.9056865464632455, 'total_sleep_time': 326.5, 'sleep_latency': 510.5, 'num_awakenings': 10, 'trans_prob_from_waso': [0.0, 0.9, 0.0, 0.1, 0.0], 'trans_prob_from_stage1': [0.21739130434782608, 0.0, 0.6086956521739131, 0.043478260869565216, 0.13043478260869565], 'trans_prob_from_stage2': [0.025, 0.2, 0.0, 0.725, 0.05], 'trans_prob_from_sws': [0.03225806451612903, 0.12903225806451613, 0.8064516129032258, 0.0, 0.03225806451612903], 'trans_prob_from_rem': [0.5, 0.3333333333333333, 0.16666666666666666, 0.0, 0.0], 'average_bout_duration_waso': 3.4, 'average_bout_duration_stage1': 1.2083333333333333, 'average_bout_duration_stage2': 3.125, 'average_bout_duration_sws': 3.5483870967741935, 'average_bout_duration_rem': 10.416666666666666}

    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])


def test_edf3_scorefile():
    dict_out = automated_parsing(filepath=os.path.join(os.path.dirname(__file__),"testfiles/edftype3_scorefile.edf"),
                                 fileformat='sleep_scoring',
                                 filetype='sleep_scoring', versionid=1,
                                 subjectid=2,
                                 visitid=1,
                                 sessionid=1,
                                 studyid="MASS")[0]

    correct_return = {'filepath': os.path.join(os.path.dirname(__file__),'testfiles/edftype3_scorefile.edf'), 'fileformat': 'sleep_scoring', 'filetype': 'sleep_scoring', 'versionid': 1, 'subjectid': 2, 'visitid': 1, 'sessionid': 1, 'studyid': 'MASS', 'epoch_len': 30, 'mins_in_waso': 8.5, 'mins_in_stage1': 15.5, 'mins_in_stage2': 164.0, 'mins_in_sws': 60.0, 'mins_in_rem': 128.5, 'sleep_efficiency': 0.9774236387782205, 'total_sleep_time': 368.0, 'sleep_latency': 46.5, 'num_awakenings': 14, 'trans_prob_from_waso': [0.0, 0.7857142857142857, 0.14285714285714285, 0.0, 0.07142857142857142], 'trans_prob_from_stage1': [0.10526315789473684, 0.0, 0.8421052631578947, 0.0, 0.05263157894736842], 'trans_prob_from_stage2': [0.24390243902439024, 0.07317073170731707, 0.0, 0.5121951219512195, 0.17073170731707318], 'trans_prob_from_sws': [0.0, 0.0, 0.9523809523809523, 0.0, 0.047619047619047616], 'trans_prob_from_rem': [0.2222222222222222, 0.4444444444444444, 0.3333333333333333, 0.0, 0.0], 'average_bout_duration_waso': 0.6071428571428571, 'average_bout_duration_stage1': 0.8157894736842105, 'average_bout_duration_stage2': 4.0, 'average_bout_duration_sws': 2.857142857142857, 'average_bout_duration_rem': 12.85}

    assert all([dict_out[k] == correct_return[k] for k in correct_return.keys()])
