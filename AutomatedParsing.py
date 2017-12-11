import mne
import sys
import pandas as pd
import numpy
import ParsingScoring as ps
import ParsingEDF as pe
import json
import glob

# global variable
SLEEPMAP = ""

# File Types are:
# - sleep (edf without scoring)
# - scoringfile (what you have been dealing with, they could be xlsx, .mat, edfs, etc)
# - tabulardata (this is demographics and the like)
# - sleep diaries (this you can ignore for now, and we can discuss soon)
# - actigraphy (same as above)

# How is location of stagemap folder passed in?
def stagemapping(jsondict): #TODO: move stagemapping to parsing_scoreing
    # Here we find the correct stage map and do mapping
    if 'studyid' in jsondict.keys:
        study = jsondict['studyid']
        # need to figure out how to know hwere stage map located
        stagemapfiles = ps.getAllFilesInTree(SLEEPMAP)
        found = False
        smlocation = ''
        while (not found) or (study == ''):
            for i in range(stagemapfiles):
                if (study + '_') in stagemapfiles[i]:
                    found = True
                    smlocation = stagemapfiles[i]
            if found == False:
                study = study[:-1]
        if smlocation == '':
            print('Unable to find stagemapfiles for study')
        else:
            stagemap = ps.MakeJsonObj(smlocation)
            jsondict = ps.sleepStageMap(jsondict, stagemap)
    return jsondict


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

# main function takes in a path to file
# return as json string
# if __name__ == '__main__':
def automated_parsing(filepath, filetype, subject=None, visit=None, session=None, task=None):
    error = False
    msg = ""
    jsonobj = []

    base_josnobj = {'subjectid': subject,
                    'visitid': visit,
                    'session': session,
                    'task': task,
                    'filetype': filetype}
    base_josnobj = dict((k, v) for k, v in base_josnobj.items() if v is not None)  # Remove None values

    # choose correct file type
    if filetype == "sleep":
        # call sleep parse function
        jsonobj = pe.EdfParse(filepath)
    elif filetype == 'scorefile':
        # call scoring file parse function
        jsonobj = ps.MakeJsonObj(filepath)
    elif filetype == 'tabular':
        # call tabulardata file parse function
        jsonobj = ps.MakeJsonObj(filepath)
    #    elif sleepdiaries = filepath:
    # call sleepdiaries parse function
    #    elif actigraphy = filepath:
    # call actigraphy parse function

    # check if error occured
    if error != 1:
        if type(jsonobj) is dict:
            base_josnobj.update(jsonobj)
            json_out = json.dumps(base_josnobj)
        elif type(jsonobj) is list:
            json_out = []
            for jsonobj_el in jsonobj:
                temp_base = base_josnobj
                temp_base.update(jsonobj_el)
                json_out.append(json.dumps(temp_base))

    return json_out, error, msg

# for testing
if __name__ == "__main__":
    folder_path = "/data/mednickdb/mednickdb_autoupload/scorefile/"
    file_paths = glob.iglob(folder_path + '*')
    file_path = "mednickdb_data/MASS/MASS_SS1/edfs/MASS_SS1_subjectid1.edf"
    for file_path in file_paths:
        object, error, message = automated_parsing(file_path, 'scorefile')
        print(object)
