# python_parsing
A python model for extracting and calculating relevent data and metadata from sleep files (scorefiles, edfs) and task data files (.mat, .csv). 

While these parsing functions can be used stand alone, as an imported python package. There main use is for automatically parsing uploaded files on the mednickdb. 

Interfaces with  mednickdb via [mednickdb_pyapi](https://github.com/MednickLab/mednickdb_pyapi).

### Parse Score Files
parse_scorefiles.py handles parsing of scorefile in various formats (grass xlsx, txt, edf, edf+, edf++, xml, hume .mat) into scoring information (as a formated dict). 

To use:
```parse_scoring_file(file, studyid)``` 
Takes a scorefile, extracts the stage every 30 seconds and coresponding ofset (since the start of the recording). The start time of a record as a datetime is also returned. Epochs that are not 30 seconds will be resampled to this epoch length (no control for alaising is done).

#Requirements:
[mednickdb_pysleep](https://github.com/MednickLab/mednickdb_pysleep)
    
   
    
              
