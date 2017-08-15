# python_parsing

### ParsingScoring.py
  #### Requirements:
    - Libaries Needed: sys,pandas, json, os, mne
    - must download ParsingPandas.py due to the fact that ParsingScoring imports it
    - File structure must be as followed:
        Head: Folder containing all other directory for different studies and nothing else
              * Directory names must be name of the study
        One Before Leaf: must contain demographics file (.xls or .xlsx) and folder "scoringfiles" which contain the data for scoring files
        Leaf: must contain only scoring files and no other folders or files saved as .txt or .edf files
              * EDF+ format is needed with hypnogram in anotation of the EDF+
  #### Function:
    1) goes through all files of the path to a folder an its subfolders given to main(must give absolute path to folder)
    2) links the demographics data to appropriate scoring files and creates uniform Json objects
    3) stores each subject as a different Json file in newly created or exisiting directory "jsonObject" as 
    "[subjectid]_studyid[studyid]_visit[visitid].json" or if the person has multiple sessions then the Json file will be
    "[subjectid]_studyid[studyid]_visit[visitid]_session[sessionid].json"
    
              
