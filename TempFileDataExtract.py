#TODO: This can be deleted

import xlrd
import requests
import json
import os
import ParsingEDF
import ParsingPandas
 
#directory to find all files in
testdir = "C:\\source\\mednickdb\\temp"

#server http://127.0.0.1:8001/files/temp
serverdir = "http://127.0.0.1:8001/files/temp"

#function to find all files in dirPath
#returns a list of strings containing the path to the files
def getAllFilesInTree(dirPath):
    _files = []
    for folder, subfolders, files in os.walk(dirPath):
        #print(files)
        for _file in files:
            filePath = os.path.join(os.path.abspath(folder), _file)
            _files.append(filePath)
    #print(_files)
    return _files
	
def getAllTempFileRecords():
    response = requests.get("http://127.0.0.1:8001/files/temp/")
    records = response.json()
    #print(records)
    _files = [i["path"] for i in records]
    return _files


def main():
    
	filesInTemp = getAllFilesInTree(testdir)
	filesInServerTemp = getAllTempFileRecords()
    #cycle through the files and if you find one that is a __ run script
#	print(filesInServerTemp)
#	print(filesInTemp)
	
	#goes through files in our temp folder and parse 
	for _files in filesInTemp:
	   if  _files.endswith(".edf"):
	      ParsingEDF.main(_files) #run our python script
	   elif _files.endswith(".xls") or _files.endswith(".xlsx") or _files.endswith(".csv"):
	      ParsingPandas.main(_files)
#		  		
#	#goes through files in server temp folder and parse
#	print("before For loop")
#	print(filesInServerTemp)
#	for _files in filesInServerTemp:
#	   print("IN For Loop")
#	   if  _files.endswith(".edf"):
#	      ParsingEDF.main(_files) #run our python script
#	   elif _files.endswith(".xlsx"):
#	      temp = _files.split("\\")
#	      ParsingXLSX.main(serverdir + temp[-1])  
           
    
	#use for testing if call to ParsingEDF works
    #ParsingEDF.main("C:\\Users\\User\\Desktop\\Copy of PAI_2019.edf")
	print("exit main")   #delete this line

#if __name__ == "__main__":
main()
	
