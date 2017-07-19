import numpy
import mne
import json
import sys
import time

def EdfParse(path = None):
   if path == None:
      #File name needs to be parsed to not include full Path
      EDF_file = mne.io.read_raw_edf(sys.argv[1])
      path = sys.argv[1]
   else: 
      EDF_file = mne.io.read_raw_edf(path)
   #splits the fileName into list of strings seperated by \
   #[-1] takes the last string in the list which is the file name
   NameOfFile = (path.split('/')[-1])

   timeConvert = time.strftime('%Y-%m-%d %H:%M:%S', 
       time.localtime(EDF_file.info["meas_date"]))

   edfDictionary = {}
   
   edfDictionary['bads'] = EDF_file.info["bads"]
   edfDictionary['ch_names'] = EDF_file.ch_names
   edfDictionary['highpass'] = EDF_file.info["highpass"]
   edfDictionary['lowpass'] = EDF_file.info["lowpass"]
   #Changed from epoch to date
   edfDictionary['meas_date'] = timeConvert
   edfDictionary['nchan'] = EDF_file.info["nchan"]
   edfDictionary['sfreq'] = EDF_file.info["sfreq"]
   edfDictionary['subject_info'] = EDF_file.info["subject_info"]

   edfDictionary['file_name'] = NameOfFile 

   #the jason dictionary of meta data of edf file
   edfDictionaryToJSON = json.dumps(edfDictionary)
   return print("Done")
 
def main (File_to_Parse = None):
   EdfParse(File_to_Parse)

#main()

