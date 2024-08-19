# Purpose : To read CSV file and generate features
# Running command: python feature.py -filename 3problems_56authors.csv

import sys, os, os.path
import math
import csv
import json
import os.path
from os import path
import lizard

input_file = "final_data_.csv"
csv_file = "final_data.csv"

Final_Data = []


def lineCount(fileName):

	lineCount = 0
	totalBlankLineCount = 0

	with open(fileName) as f:

		for line in f:
			lineCount += 1

			lineWithoutWhitespace = line.strip()
			if not lineWithoutWhitespace:
				totalBlankLineCount += 1

	return lineCount, totalBlankLineCount

def write_csv():
	csv_columns = []
	for d in Final_Data:
		for key in d:
			csv_columns.append(key)
		break
	try:
		status = path.isfile(str(csv_file))
		with open(csv_file, 'a+', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			if status is False:
				writer.writeheader()
			for data in Final_Data:
				writer.writerow(data)
	except IOError:
		print("I/O error")

def main ():
	with open(input_file, mode='r') as csvFile:
		csv_reader = csv.DictReader(csvFile)
		line_count = 0
		for row in csv_reader:
			local_data = {}

			print (row['sub_id'])
			code = row['source']

			fc = open("code.cpp", "w")
			fc.write(row['source'])
			fc.write('\n')
			fc.close()

			loc, blankLine = lineCount("code.cpp")

			li = lizard.analyze_file.analyze_source_code("foo.cpp",code)
			cc = 0
			slocP = 0
			for j in range (len(li.__dict__['function_list'])):
				cc = cc + (li.function_list[j].__dict__['cyclomatic_complexity'])
				slocP = slocP + (li.function_list[j].__dict__['nloc'])
			numberOfFunction = j + 1
			comments = loc - slocP
			lsloc = slocP - blankLine

			print ('Cyclomatic Complexity: ', cc)
			print ('Number of function: ', numberOfFunction)
			print ('Line Of Code: ', loc)
			print ('slocP: ', slocP)
			print ('lsloc: ', lsloc)
			print ('Comments: ', comments)
			print ('Blank Line: ', blankLine)

			local_data['sub_id'] = row['sub_id']
			local_data['handle'] = row['handle']
			local_data['language'] = row['language']
			local_data['time'] = row['time']
			local_data['memory'] = row['memory']
			local_data['source'] = row['source']
			local_data['firstName'] = row['firstName']
			local_data['lastName'] = row['lastName']
			local_data['country'] = row['country']
			local_data['continent'] = row['continent']
			local_data['program_vocabulary'] = row['program_vocabulary']
			local_data['program_length'] = row['program_length']
			local_data['calculated_estimated_program_length'] = row['calculated_estimated_program_length']
			local_data['volume'] = row['volume']
			local_data['difficulty'] = row['difficulty']
			local_data['effort'] = row['effort']

			local_data['loc'] = loc
			local_data['slocP'] = slocP
			local_data['lsloc'] = lsloc
			local_data['comments'] = comments
			local_data['blankLine'] = blankLine

			local_data['cyclomatic_complexity'] = cc
			local_data['numberOfFunction'] = numberOfFunction

			local_data['gender'] = row['gender']

			Final_Data.append(local_data)
			line_count += 1

	csvFile.close()

main()
write_csv()
