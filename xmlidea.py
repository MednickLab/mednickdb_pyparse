import xml.etree.ElementTree as ET
 
###   1 go throu XML build dicts for each leaf 
###   2 go through dicts if eventconcept contains sleep
###       - pull out evenconcept, start, duration --> Save into New Dictionary which will contain a list of eventconcept, start, duration


def StringTimetoEpoch(time):
    time = time.replace('.', ':')
    temp = time.split(":")
    hours = int(temp[0])
    if temp[-1].find("AM") != -1 and temp[0].find("12"):
        hours = 0
    elif temp[-1].find("PM") != -1:
        hours = hours + 12
    # get rid of AM and PM
    temp[-1] = temp[-1].split(' ')[0]
    EpochTime = hours * 60 + int(temp[1]) + int(temp[2]) / 60
    EpochTime = round(EpochTime, 1)

    return EpochTime

 
def XMLRepeter (node):
	temp = {}
	list = []
	for child in node:
		J = (XMLRepeter(child))
		if len(J) != 0:
			for key in J.keys():
				if key in temp.keys():
					temp[key].append(J[key])
				else:							#if J[key] != None:
					temp[key] = []
					temp[key].append(J[key])
		dict = {child.tag: child.text}
		if(child.text != '\n'):
			for key in dict.keys():
				if key in temp.keys():
					temp[key].append(dict[key])
				else:							#if dict[key] != None:
					temp[key] = []
					temp[key].append(dict[key])
	return temp


#characters that we will strip
STRIP = "' ', ',', '\'', '(', '[', '{', ')', '}', ']'"	

def XMLParse(file):
	tree = ET.parse(file)
	root = tree.getroot()
	dictXML = XMLRepeter(root)
	tempDict= {}	
	tempDict['epochstage'] = []
	tempDict['starttime'] = []
	tempDict['duration'] = []
	
	for key in dictXML.keys():
		needToStrip = str(dictXML[key]).split(',')
		for i in range(len(needToStrip)):
			needToStrip[i] = needToStrip[i].lstrip(STRIP).rstrip(STRIP)
		dictXML[key] = needToStrip
		
	# Need to change this maybe	right now only includes the important stuff
	# Need to fix the time
	#get dictionary with sleepevent, start time, and duration
	#need to expand so it will see every 30 sec and have it in epoch time
	for i in range(len(dictXML['EventType'])):
		if "Stages" in dictXML['EventType'][i]:
			tempDict['epochstage'].append(dictXML['EventConcept'][i])
			tempDict['duration'].append(float(dictXML['Duration'][i]))
			tempDict['starttime'].append(float(dictXML['Start'][i]))
	#print(tempDict['starttime'])
	returnDict = {}
	returnDict['epochstage'] = []
	returnDict['starttime'] = []
	returnDict['originalTime'] = StringTimetoEpoch(str(dictXML['ClockTime']).split(' ')[-1].lstrip(STRIP).rstrip(STRIP))
	#need to standardize
	for i in range(len(tempDict['epochstage'])):
		j = 0.0
		while j < (tempDict['duration'][i]):
			returnDict['epochstage'].append(tempDict['epochstage'][i].split('|')[0] )
			time = ( tempDict['starttime'][i] +  j )/ 60 + returnDict['originalTime']
			if time > 1440:
				time = time - 1440
			returnDict['starttime'].append(time)
			j = j + 30
			
	return returnDict
tree = XMLParse('C:/source/mednickdb/temp/Bad Data/CCSHS/CCSHS/scorefiles/ccshs-trec-1800001-nsrr.xml')
print(tree)
print(len(tree['epochstage']))

#print(tree['EventType'])	#<-- need to equal "Stages|Stages" for sleep data
#print(tree['EventConcept']) #<-- need to pull data if and only if it is sleep data same for Start and duration
#print(tree['Start'])
#print(tree['Duration'])
#print(tree['ClockTime'])

#tree['PSGAnnotation']['ScoredEvents'].popitem().split(
#stringVer = str(tree['PSGAnnotation']['ScoredEvents']).split('OrderedDict')
#print(len(stringVer))

#STRIP = "' ', ',', '\'', '(', '[', '{', ')', '}', ']'"
#for i in stringVer:
#	t = i.split('EventConcept')
#	t = t[-1].split('Start')
#	j = t[-1].split( 'Duration')
#	print(t[0].lstrip(STRIP).rstrip(STRIP))
	#print(j[0])
	#print(j[-1])
	