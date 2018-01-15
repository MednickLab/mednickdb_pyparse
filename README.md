# python_parsing

### Parse Score Files
ParsingScoring.py handles parsing of scorefile in various formats (grass xlsx, txt, edf, edf+, edf++, xml, TODO hume .mat) into scoring information (as a formated dict). 

To use:
```parse_scoring_file(file, studyid)``` 
Takes a scorefile, extracts the stage every 30 seconds and coresponding ofset (since the start of the recording). The start time of a record as a datetime is also returned. Epochs that are not 30 seconds will be resampled to this epoch length (no control for alaising is done).

#### Requirements:
    - Libaries Needed: sys,pandas, json, os, mne, parse
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
    
   
    
              
