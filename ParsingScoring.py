import pandas as pd
import mne
import numpy
import datetime
import ParsingPandas
import xlrd
import requests
import json
import os 


def getAllFilesInTree(dirPath):
    _files = []
    for folder, subfolders, files in os.walk(dirPath):
        #print(files)
        for _file in files:
            filePath = os.path.join(os.path.abspath(folder), _file)
            _files.append(filePath)
    #print(_files)
    return _files
	

#parsing panda objects returns jason object
def Parsing(PandaFile):
	FileKeys = PandaFile.keys()
    #cycle through keys to see if we get hits on the five keys we want and keep track of which ones we hit

	output_dict = []
	for sub_data in PandaFile.iterrows():
		#print(json.loads(sub_data[1].to_json()))
		output_dict.append(sub_data[1].to_json())
	#print(output_dict[-1])
	return output_dict

				    	  

def StringTimetoEpoch(time):
	#print(time)
	time = time.replace('.',':')
	temp = time.split(":")
	hours = int(temp[0])
	if temp[-1].find("AM") != -1 and temp[0].find("12"):
		hours = 0
	elif temp[-1].find("PM") != -1:
		hours = hours + 12
	#get rid of AM and PM
	temp[-1] = temp[-1].split(' ')[0]
	
	EpochTime = hours * 60 + int(temp[1]) + int(temp[2])/60
	EpochTime = round(EpochTime,1)

	return EpochTime
	
	
def EpochtoStringTime(time):
	Sec = time % 60
	time = time / 60
	Min = time % 60
	time = time / 60
	TotalTime = str(time) + ':' + str(Min) + ":" + str(Sec)
	
#demographics file contains te data you would need fro the other one
#in the name of the demographics file it tells you which file to access for its data type
#from file path and name of scoring we know the SubjectID 
#each file data base needs different parsing method
#we will neee a  checker to see which parse method is needed
#all demographics files contain same information

 
#returns an integer determiing which parse method to use
#if found == 0 file contain only s and 0s
#if found == 1 file contain latency and type(sleep stage mode)
#if found == 2 file contain sleep stage , and time 
KeyWords = ["latency","RemLogic"]
def ScoringParseChoose(file):
	found = 0 
	firstline = file.readline()
	file.seek(0)
	for count in range(len(KeyWords)):
		if firstline.find(KeyWords[count]) != -1:
			found = count + 1
	return found
	
# Type 0		
def BasicScoreFile(file):
	JasonObj = {}
	JasonObj["epochstage"] = []
	JasonObj["Type"] = "0"
	for line in file:
		temp = line.split(' ')
		temp = temp[0].split('\t')
		temp[0] = temp[0].strip('\n')
		JasonObj["epochstage"].append(temp[0])
	return JasonObj	

# Type 1
def LatTypeScoreFile(file):
	JasonObj = {}
	JasonObj["Type"] = "1"
	JasonObj["epochstage"] = []
	JasonObj["epochstarttime"] = []
	file.readline()						#done so that we can ignore the first line which just contain variable names
	for line in file:
		temp = line.rstrip()
		temp = line.split('  ')
		if len(temp) == 1:
			temp = line.split('\t')		
		temp[-1] = temp[-1].strip('\n')
		JasonObj["epochstage"].append(temp[-1])
		time = temp[0]
		JasonObj["epochstarttime"].append(time)		
	return JasonObj	


# Type 2
def FullScoreFile(file):
	JasonObj = {}
	JasonObj["Type"] = "2"
	JasonObj["epochstage"] = []
	JasonObj["epochstarttime"] = []
#find line with SleepStage
#find position of SleepStage and Time
	StartSplit = False
	
	SleepStagePos = 0
	TimePos = 0
	EventPos = 0
	
	for line in file:
		if StartSplit and line.strip() != '':
			temp = line.split('\t')
			#print(len(temp))
			#print(EventPos)
			#print(file)
			if len(temp) > EventPos and temp[EventPos].find("MCAP") == -1:
				JasonObj["epochstage"].append(temp[SleepStagePos])
				time = StringTimetoEpoch(temp[TimePos])
				JasonObj["epochstarttime"].append(time)
			
		if line.find("Sleep Stage") != -1:
			StartSplit = True
			temp = line.split('\t')
			for i in range(len(temp)):
				if temp[i] == "Sleep Stage":
					SleepStagePos = i
				if temp[i].find("Time") != -1:
					TimePos = i
				if temp[i].find("Event") != -1:
					EventPos = i
	return JasonObj
	
#gets the file reads it using appropriate read method then calls appropriate parse function 
#does fine tuning for jason obj to uniform include subjectID and studyID	
def MakeJsonObj(file):
	#demographic Files
	if file.endswith("xls") or file.endswith("xlsx") or file.endswith(".csv"):
		#do the parsing
		JsonList = ParsingPandas.main(file)
		for i in range(len(JsonList)):
			JsonList[i] = json.loads(JsonList[i])
		#add studyID from name of file
		temp = file.split('.')
		temp = temp[0].split('\\')
		temp = temp[-1].split('ics_')
		temp = temp[-1]
		#visit = 1
		if '_P' in temp: 
			temp = temp.split('_')
			#visit = temp[-1]
			temp = temp[0]
			dict = {}
		returningList = []
		for i in range(len(JsonList)):
			if "subjectID" not in JsonList[i]:
				if "subid" in JsonList[i]:
					JsonList[i]["subjectID"] = JsonList[i]["subid"]
					JsonList[i].pop("subid",None)
				elif "Subject" in JsonList[i]:
					JsonList[i]["subjectID"] = JsonList[i]["Subject"]
					JsonList[i].pop("Subject",None)
				else:
					JsonList[i]["subjectID"] = 'N/A'
				if isinstance(JsonList[i]["subjectID"],str):
					JsonList[i]["subjectID"] = JsonList[i]["subjectID"].lower()
			JsonList[i]["studyID"] = temp
			#JsonList[i]["visitID"] = visit
		
		return JsonList

	#these are the scoring files
	elif file.endswith(".txt"):
		JSON = {}
		temp = open(file, 'r')
		ScoreFileType = ScoringParseChoose(temp)
		if ScoreFileType == 0:
			JSON = BasicScoreFile(temp)
		elif ScoreFileType == 1:
			JSON = LatTypeScoreFile(temp)
		elif ScoreFileType == 2:
			JSON = FullScoreFile(temp)
		else:
			print("other")

		#add studyID and subectID to JSON for scoring
		holder = file.split('.')
		holder = holder[0].split('\\')
		if not "subjectID" in JSON.keys():
			JSON["subjectID"] = holder[-1]
		JSON["studyID"] = holder[-3]
		if isinstance(JSON["subjectID"],str):
			JSON["subjectID"].strip(' ')
			JSON["subjectID"] = JSON["subjectID"].lower()
		return JSON
	
	#EDF files
	elif file.endswith(".edf"):
		EDF_file = mne.io.read_raw_edf(file, preload=True)
	
	return 1

#Demo is a list of dictionary from demographic files
#Score is  list of dictionar from all score files
def CombineJson(Demo, Score):
	ReturnJsonList = []
	for i in range(len(Demo)):
		Found = False
		for j in range(len(Score)):
			#print(Demo[i]["studyID"] + ' ' + Score[j]["studyID"])
			if Demo[i]["studyID"] == Score[j]["studyID"]:
				#print(str(Demo[i]["subjectID"]) + ' ' + str(Score[j]["subjectID"]))
				if  str(Demo[i]["subjectID"]) == str(Score[j]["subjectID"]):
					#print("MATCH 2")
					temp = {**Demo[i],**Score[j]}
					
					#type 0 files have epoch timestamps we add it now
					if temp["Type"] == '0':
							temp["epochstarttime"] = []
							#print(temp.keys())
							if "startime" in temp.keys():
								temp["epochstarttime"].append(StringTimetoEpoch(temp["startime"]))
							elif "starttime" in temp.keys():
								temp["epochstarttime"].append(StringTimetoEpoch(temp["starttime"]))
							for samples in range(len(temp["epochstage"]) - 1):
								epochTime = temp["epochstarttime"][samples] + .5
								if epochTime > 1439.5:
									epochTime = 0
								temp["epochstarttime"].append(epochTime)
					ReturnJsonList.append(temp)
					Found = True
				#else:
					#print(str(Demo[i]["subjectID"]) + ' ' + str(Score[j]["subjectID"]))
			
				
		if Found == False:
			print("no match found for: " + str(Demo[i]["studyID"]) + ", " + str(Demo[i]["subjectID"]))
	return ReturnJsonList
		
#Main
#main chooses which parsing function is called
def main(file):    
	#filesInTemp = getAllFilesInTree(testdir)
	filelist = getAllFilesInTree(file)

#cycle through the files and if you find one that is a __ run script
#	print(filesInServerTemp)
#	print(filesInTemp)
	
	#now we have a list of Json Objs made from all files in folder
	#fist will contain all json obj from the score files
	#second will contain all json objs from demographic files
	JsonObjList = []
	JsonObjListDemo = []
	#print (file)
	for files in filelist:
		JsonObj = MakeJsonObj(files)
		if isinstance(JsonObj, int):
			print(files + " is not comprehendable")
		elif isinstance(JsonObj,dict):
			JsonObjList.append(JsonObj)
		elif isinstance(JsonObj,list):
			#print(JsonObj)
			for i in JsonObj:
				JsonObjListDemo.append(i)
	#call function to combine the lists into one json obj
	FinishedJson = CombineJson(JsonObjListDemo, JsonObjList)
	print(FinishedJson[0])
		
main("C:/source/mednickdb/temp/DinklemannLab")#CAPStudy/")#SpencerLab/")#
