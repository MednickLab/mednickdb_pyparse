import pandas as pd

# Automatic mapping from tabular column names to keys that the database knows how to deal with
spell_map = {'subid':'subjectid',
             'subject':'subjectid',
             'sub':'subjectid',
             'sid':'subjectid',
             'subjectnum':'subjectid',
             'subjnum':'subjectid',
             'subj':'subjectid',
             'visit':'visitid',
             'vis':'visitid',
             'session':'sessionid',
             'taskname':'filetype',
             'task':'filetype',
             'sess':'sessionid'}


# parsing panda objects returns jason object
def parse_tabular_file(file):
    """
    Read in txt, csv, xls, tsv tabular file, and strip out each row as a peice of data (formated as dictionary)
    Cols are keys, and will be converted to lowercase. Special chars are not allowed, but are not currently checked TODO
    To push this information to the database, rows should contain the appropriate hierarchical specifiers, e.g. a row for subjectid, etc
    :param file: tabular filepath to parse
    :return: a dict or a list of dicts for each row of the tabular file.
    """
    if 'csv' in file:
        df = pd.read_csv(file)
    if 'txt' in file or 'tsv' in file:
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
