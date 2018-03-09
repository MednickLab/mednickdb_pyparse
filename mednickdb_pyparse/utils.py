STRIP = "' ', ',', '\'', '(', '[', '{', ')', '}', ']'"

def extract_file_tags_from_file_name(filePath): #TODO untested and unused
    out_dict = {}
    studyid = 'n/a'
    subjectid = 'n/a'
    visitid = '1'

    if 'scorefiles' in filePath:
        studyid = filePath.split('scorefiles')[0]
        studyid = studyid.split('\\')
        if studyid[-1] == '':
            studyid = studyid[-2]
        else:
            studyid = studyid[-1]
        subjectid = filePath.split('scorefiles')[-1]
        subjectid = subjectid.split('subjectid')[-1]
        subjectid = subjectid.split('.')[0]
        if 'visit' in filePath:
            visitid = subjectid.split('visitid')[-1]
            visitid = visitid.split('.')[0]
            subjectid = subjectid.split('visitid')[0]

    subjectid = str(subjectid).lstrip(STRIP).rstrip(STRIP)
    subjectid = str(subjectid).lstrip('_').rstrip('_')
    visitid = str(visitid).lstrip(STRIP).rstrip(STRIP)
    visitid = str(visitid).lstrip('_').rstrip('_')
    studyid = str(studyid).lstrip(STRIP).rstrip(STRIP)
    out_dict['subjectid'] = subjectid
    out_dict['studyid'] = studyid
    out_dict['visitid'] = visitid
    return out_dict