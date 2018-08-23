import pandas as pd

spell_map = {'subid':'subjectid',
             'subject':'subjectid',
             'sub':'subjectid',
             'sid':'subjectid',
             'subjectnum':'subjectid',
             'subjnum':'subjectid',
             'subj':'subjectid',
             'visit':'visitid',
             'session':'sessionid',
             'version':'versionid',
             'taskname':'taskid',
             'task':'taskid',
             'sess':'session'}


# parsing panda objects returns jason object
def parse_tabular_file_to_dict(file):
    if 'csv' in file:
        df = pd.read_csv(file)
    if 'txt' in file:
        df = pd.read_csv(file, delimiter='\t')
    if 'xls' in file or 'xlsx' in file:
        df = pd.read_excel(file)
    output_list = []
    for idx, row_data in df.iterrows():
        assert all([isinstance(i, str) for i in row_data.index]), "Column names are not all strings"
        # print(json.loads(sub_data[1].to_json()))
        row_data.index = [spell_map[i.lower()] if i in spell_map else i.lower() for i in row_data.index]
        output_list.append(row_data.to_dict())

    return output_list


# Main
# main chooses which parsing function is called
def main(file):
    List_of_JSON = []
    temp = []
    if file.endswith("xls") or file.endswith("xlsx"):
        temp = pd.read_excel(file)
    elif file.endswith("csv"):
        temp = pd.read_csv(file)
    List_of_JSON = parse_tabular_file_to_dict(temp)
    return List_of_JSON
    # main("C:/source/mednickdb/temp/Encoding_Sub1_Visit1.csv")
