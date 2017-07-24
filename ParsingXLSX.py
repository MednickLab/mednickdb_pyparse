import numpy
import json
import sys
import xlrd

def XLSXParse(path):
   XLSXpath = xlrd.open_workbook(path)
   screening_sheet = XLSXpath.sheet_by_index(0)
   
   NumOfCol = screening_sheet.ncols
   NumOfRow = screening_sheet.nrows
   TitleRow = []
   parsing = []
   for j in range(NumOfRow):   
      json_object = {}
      for i in range(NumOfCol):
         if(j == 0):
            TitleRow.append(screening_sheet.col_values(i)[j])
         else:
            #now I am cycling through all row and collumn
		    #store into json object key:value --> firstRow:curRow
            json_object[TitleRow[i]] = screening_sheet.col_values(i)[j]
      
      parsing.append(json_object)
   return parsing

def main():
   path = input('Enter Path to File ')
   parsed = XLSXParse(path)
   print (parsed[1])

main()