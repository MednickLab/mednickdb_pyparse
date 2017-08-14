# python_parsing

### ParsingScoring.py
  #### Requirements:
    - must download ParsingPandas.py due to the fact that ParsingScoring imports it
    - File structure must be as followed:
        Head: Folder containing all Folders for different studies and nothing else
              - folder name must be name of the study
        SecondLevel: must contain demographics file and folder "scoringfiles" which contain the ata for scoring files
        ThirdLevel: must contain only scoring files and no other folders or files
  #### Function:
    1) goes through all files of the path to a folder an its subfolders given to main (must give absolute path to folder)
    2) links the demographics data to appropriate scoring files and creates uniform Json objects
    3) stores each subject as a different Json file in newly created or exisiting directory "jsonObject" as "[subjectID]_[studyID].json"
              
