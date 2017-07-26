import pandas as pd
import json

#parsing panda objects returns jason object
def Parsing(PandaFile):
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
		#print(json.loads(sub_data[1].to_json()))
		output_dict.append(sub_data[1].to_json())
	print(output_dict[-1])
	return output_dict

				    	    

#Main
#main chooses which parsing function is called
def main(file):
	List_of_JSON = []
	temp = []
	if file.endswith("xls") or file.endswith("xlsx"):
		temp = pd.read_excel(file)
	else:
		temp = pd.read_csv(file)
	List_of_JSON = Parsing(temp)
	
#main("C:/source/mednickdb/temp/ERQ.xls")#Encoding_Sub1_Visit1.csv")