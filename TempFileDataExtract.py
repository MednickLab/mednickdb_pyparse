import xlrd
import requests
import json
import os

#enter path to dir containing the parsing files
exec("/PythonInternship/ParsingEDF.py")
 
#directory to find all files in
testdir = "C:\\source\\mednick\\mednick\\temp"

#function to find all files in dirPath
#returns a list of strings containing the path to the files
def getAllFilesInTree(dirPath):
    _files = []
    for folder, subfolders, files in os.walk(dirPath):
        print(files)
        for _file in files:
            filePath = os.path.join(os.path.abspath(folder), _file)
            _files.append(filePath)
    print(_files)
    return _files


def main():
    print("in main")
    filesInTemp = getAllFilesInTree(testdir)
    #cycle through the files and if you find one that is a __ run script
    print(filesInTemp)
    for _files in filesInTemp:
        if True:# _files.endswith(".edf"):
           #run our python script
           # Parse.main(_files);  
           EdfParse("~\\PythonInternship\\Copy of PAI_2019.edf")
   
    EdfParse("~/PythonInternship/Copy of PAI_2019.edf")
    print("exit main")   #delete this line

if __name__ == "__main__":
   main()
