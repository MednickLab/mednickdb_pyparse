import sys
sys.path.append("../mednickdb_pyapi/")
import mednickdb_pyapi
import json

dev = True

if __name__ == '__main__':
    #query api
    db = mednickdb_pyapi.MednickAPI('http://saclab.ss.uci.edu:8001')
    files = db.get_incomplete_files()
    for file in files:
        print('downloading', file['fileName'])
        db.download_file(file['_id'])