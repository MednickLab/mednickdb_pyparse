import mne
import sys
import pandas as pd
import numpy
import ParsingScoring as ps
import ParsingEDF as pe
import json
#global variable
SLEEPMAP = ""

#File Types are:
#- sleep (edf without scoring)
#- scoringfile (what you have been dealing with, they could be xlsx, .mat, edfs, etc) 
#- tabulardata (this is demographics and the like)
#- sleep diaries (this you can ignore for now, and we can discuss soon)
#- actigraphy (same as above)

def sleep_parsing ( file ):
    try:
        jsonobj = pe.EdfParse(file)
    except:
        return  None, 1, "Failed to open edf file" 
    addedKey = []
    for key in jsonobj.keys():
        addedKey["edf_"+key] = jsonobj[key]
    return addedKey, 0, ''



def scoringfile_parsing ( file ) :
    try:
        print(file)
        jsondict = ps.MakeJsonObj(file) 
    except:
        return  None, 1, "Failed to parse scorefile"
    #line for change stages to stagemap stages
    #jsondict = stagemapping(jsondict)
    return jsondict, 0, ''

#How is location of stagemap folder passed in?    
def stagemapping (jsondict):
    # Here we find the correct stage map and do mapping
    if 'studyid' in jsondict.keys:
        study = jsondict['studyid']
        #need to figure out how to know hwere stage map located
        stagemapfiles = ps.getAllFilesInTree(SLEEPMAP)
        found = False
        smlocation = ''
        while (not found) or (study == ''):
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
    try:
        jsondict = ps.MakeJsonObj(file)
    except:
        return  None, 1, "Failed to parse tabular file"
    return jsondict, 0, ''

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
def automated_parsing (filepath, filetype, subject = None, visit= None, session = None, task = None) :
    #Delete when running program, Here just for testing
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #if len(sys.argv) > 1:
    #    filepath = sys.argv[1]  # FIXME using file and files as variable names is confusing, be more specific
    #else:
    #    filepath = input("Enter absolute path to the head Directory containing the scorings folders: ")
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
        
    error = 0
    msg = ""
    jsonobj = []
    
    #choose correct file type
    if filetype == "sleep":
        #call sleep parse function
        jsonobj, error , msg = sleep_parsing(filepath)
    elif filetype =='scorefiles':
        #call scoring file parse function
        jsonobj, error , msg = scoringfile_parsing(filepath)
    elif filetype == 'tabular': 
        #call tabulardata file parse function
        jsonobj, error , msg = tabulardata_parsing(filepath)
#    elif sleepdiaries = filepath:
      #call sleepdiaries parse function
#    elif actigraphy = filepath:
      #call actigraphy parse function
    
    #check if error occured
    if error == 1:
        return jsonobj, error , msg
    
    
    if type(jsonobj) is dict:
        jsonobj['subject'] = subject
        if visit != None:
            jsonobj['visit'] = visit
        if session != None:
            jsonobj['session'] = session
        if task != None:
            jsonobj['task'] = task
        #jsonobj = stagemapping(jsonobj)
    #Is there stages to map for these files (none scorefiles) ??? (I dont think so)
    elif type (jsonobj) is list:
        for index in range(jsonobj):
            jsonobj[index]['subject'] = subject
            if visit != None:
                jsonobj[index]['visit'] = visit
            if session != None:
                jsonobj[index]['session'] = session
            if task != None:
                jsonobj[index]['task'] = task
    
    jsonlist = ''
    if type (jsonobj) is list:
        jsonlist = []
        for index in range(len(jsonobj)):
            jsonlist.append(json.dumps(jsonobj[index]))
    elif type (jsonobj) is dict:
        jsonlist = json.dumps(jsonobj)
    else :
        return jsonobj, error, msg
    print (jsonobj)      #delete this line.
    return jsonlist, error, msg

#for testing
object, error, message = automated_parsing("E:/BensGoogleDrive/SleepArchData/StudiesToParse/WamsleyLab/WamsleyLab_R21/scorefiles/subjectid01.edf", 'scorefiles')
print (message)