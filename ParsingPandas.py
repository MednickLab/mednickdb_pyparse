import pandas as pd
import json



#excel
def ParsingExcel(path):
	PandaFile = pd.read_excel(path)
	FileKeys = PandaFile.keys()
	#cycle through keys to see if we get hits on the five keys we want and keep track of which ones we hit
	hit = []

	count = PandaFile.shape
	for _key in FileKeys:
		if _key == "SubID":
			hit.append("SubID")   
		elif _key == "Study":
			hit.append("Study")   
		elif _key == "Visit":
			hit.append("Visit")   
		elif _key == "Session":
			hit.append("Session")   
		elif _key == "Task":
			hit.append("Task")	
	output_dict = []
	for sub_data in PandaFile.iterrows():
		print(json.loads(sub_data[1].to_json()))
		output_dict.append(sub_data[1].to_json())
	#print(output_dict[-1])
	return output_dict

	

#CSV parsing returns jason object
def ParsingCSV(path):
	PandaFile = pd.read_csv(path)
	FileKeys = PandaFile.keys()
    #cycle through keys to see if we get hits on the five keys we want and keep track of which ones we hit
	hit = []

	count = PandaFile.shape
	for _key in FileKeys:
		if _key == "SubID":
			hit.append("SubID")   
		elif _key == "Study":
			hit.append("Study")   
		elif _key == "Visit":
			hit.append("Visit")   
		elif _key == "Session":
			hit.append("Session")   
		elif _key == "Task":
			hit.append("Task")	

	output_dict = []
	for sub_data in PandaFile.iterrows():
		tempDict = {}
		for _key in range(len(sub_data[1])):
			tempDict[FileKeys[_key]] = sub_data[1][_key]
		JsonObject = json.dumps(tempDict)
		output_dict.append(JsonObject)
	print(output_dict[-1])
	return output_dict

				    	    

#Main
#main chooses which parsing function is called
def main(file):
	List_of_JSON = []
	temp = []
	if file.endswith("xls") or file.endswith("xlsx"):
		List_of_JSON = ParsingExcel(file)
	else:
		List_of_JSON = ParsingCSV(file)
	
main("C:/source/mednickdb/temp/ERQ.xls")