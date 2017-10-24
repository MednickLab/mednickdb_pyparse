import mne
import sys
import pandas as pd
import numpy
import ParsingScoring as ps
import ParsingEDF as pe

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Title: read_edf_annotations, resample_30s
#Author: Stanislas Chambon
#Date: 8/28/2017
# Availability: https://github.com/mne-tools/mne-python/issues/4489
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def read_edf_annotations(fname, annotation_format="edf/edf+"):
    """read_edf_annotations

    Parameters:
    -----------
    fname : str
        Path to file.

    Returns:
    --------
    annot : DataFrame
        The annotations
    """
    with open(fname, 'r', encoding='utf-8',
              errors='ignore') as annotions_file:
        tal_str = annotions_file.read()

    if "edf" in annotation_format:
        if annotation_format == "edf/edf+":
            exp = '(?P<onset>[+\-]\d+(?:\.\d*)?)' + \
                  '(?:\x15(?P<duration>\d+(?:\.\d*)?))?' + \
                  '(\x14(?P<description>[^\x00]*))?' + '(?:\x14\x00)'

        elif annotation_format == "edf++":
            exp = '(?P<onset>[+\-]\d+.\d+)' + \
                  '(?:(?:\x15(?P<duration>\d+.\d+)))' + \
                  '(?:\x14\x00|\x14(?P<description>.*?)\x14\x00)'

        annot = [m.groupdict() for m in re.finditer(exp, tal_str)]
        good_annot = pd.DataFrame(annot)
        good_annot = good_annot.query('description != ""').copy()
        good_annot.loc[:, 'duration'] = good_annot['duration'].astype(float)
        good_annot.loc[:, 'onset'] = good_annot['onset'].astype(float)
    else:
        raise ValueError('Not supported')

    return good_annot


def resample_30s(annot):
    annot = annot.set_index('onset')
    annot.index = pd.to_timedelta(annot.index, unit='s')
    annot = annot.resample('30s').ffill()
    annot = annot.reset_index()
    annot['duration'] = 30.
    return annot

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#File Types are:
#- sleep (edf without scoring)
#- scoringfile (what you have been dealing with, they could be xlsx, .mat, edfs, etc) 
#- tabulardata (this is demographics and the like)
#- sleep diaries (this you can ignore for now, and we can discuss soon)
#- actigraphy (same as above)

def sleep_parsing ( file ):
    jsonobj = pe.EdfParse(file)
    return jsonobj



def scoringfile_parsing ( file ) :
    jsondict = ps.MakeJsonObj(file)                  
    return jsondict

#How is location of stagemap folder passed in?    
def stagemapping (jsondict):
    # Here we find the correct stage map and do mapping
    if 'studyid' in jsondict.keys:
        study = jsondict['studyid']
        #need to figure out how to know hwere stage map located
        stagemapfiles = ps.getAllFilesInTree(_LOCATIONofSTAGEMAP_)
        found = False
        smlocation = ''
        while !found or study == '':
            for i in Range(stagemapfiles):
                if (study + '_') in stagemapfiles[i]:
                    found = True
                    smlocation = stagemapfiles[i]
            if found == False:
                study = study[:-1]
        if smlocation == '':
            print ('Unable to find stagemapfiles for study')
        else:
            stagemap = ps.MakeJsonObj(smlocation)
            jsondict = ps.sleepStageMap(jsondict, stagemap)
    return jsondict
    
def tabulardata_parsing ( file ):
    # works if only one page for tabular data
    jsondict = ps.MakeJsonObj(file)    
    return dict

#def sleepdiaries_parsing ( file ):
#CSV files
#def actigraphy_parsing (file):
    #go line by line until find "- Statistics -"
    #Create it as datatable
    #- remove any lines starting with a blank
    #- remove any lines that are "summary"
    #- remove any lines that are "excluded"
    # GO until you find line start with '-----'

    #go line by line down until find '- Epoch-by-Epoch Data -' go down to line 187 which contains keys
    #map key to the other actigraphy mapping files
    #create datatable until EOF

#main function takes in a path to file
#return as json string
#if __name__ == '__main__': 
def main(filetype, filepath, subject, visit= None, session = None, task = None) :
    filepath = ''
    if len(sys.argv) > 1:
        filepath = sys.argv[1]  # FIXME using file and files as variable names is confusing, be more specific
    else:
        filepath = input("Enter absolute path to the head Directory containing the scorings folders: ")
    
    jsonobj = []
    
    #choose correct file type
    if 'scorefiles' not in filepath and '.edf' in filepath:
        #call sleep parse function
        jsonobj = sleep_parsing(filepath)
    elif 'scorefiles' in filepath:
        #call scoring file parse function
        jsonobj = scoringfile_parsing(filepath)
    elif 'xlsx' in filepath: 
        #call tabulardata file parse function
        jsonobj = tabulardata_parsing(filepath)
#    elif sleepdiaries = filepath:
      #call sleepdiaries parse function
#    elif actigraphy = filepath:
      #call actigraphy parse function
    
    if type(jsonobj) is dict:
        jsonobj['subject'] = subject
        if visit != None:
            jsondict['visit'] = visit
        if session != None:
            jsondict['session'] = session
        if task != None:
            jsondict['task'] = task
        jsondict = stagemapping(jsondict)
    #Is there stages to map for these files (none scorefiles) ??? (I dont think so)
    elif type (jsonobj) is list:
        for index in range(jsonobj):
            jsonobj[index]['subject'] = subject
            if visit != None:
                jsondict[index]['visit'] = visit
            if session != None:
                jsondict[index]['session'] = session
            if task != None:
                jsondict[index]['task'] = task
    
    jsonlist = json.dumps(jsonobj)      
   
    print (jsonobj)      #delete this line.
    return jsonlist