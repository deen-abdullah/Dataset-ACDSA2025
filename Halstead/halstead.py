import sys, os
import math
import csv
import json
import os.path
from os import path

input_file = "final_data.csv"
csv_file = "final_data_.csv"


Final_Data = []

def calculateHalstead ():
	# uncomment the following line to execute the main.cpp file
	#x = os.system('g++ main.cpp -o main.exe')
	x = 0	# if main.cpp file is compiled
	if x == 0:
		os.system('./main.exe')
		print ('Halstead metrics calculated')

		with open('halstead.txt') as f:
			n1, n2, N1, N2 = [int(x) for x in next(f).split()]
		f.close()

		return n1, n2, N1, N2
	else:
		print(x)
		return


def halsteadMatrics ():

	n1, n2, N1, N2 = calculateHalstead()
	programVocabulary = n1 + n2
	programLength = N1 + N2
	
	if n1 == 0 and n2 != 0:
		calculatedEstimatedProgramLength = n2 * math.log (n2, 2)
	elif n1 != 0 and n2 == 0:
		calculatedEstimatedProgramLength = n1 * math.log (n1, 2)
	elif n1 == 0 and n2 == 0:
		calculatedEstimatedProgramLength = 0
	else:
		calculatedEstimatedProgramLength = (n1 * math.log (n1, 2)) + (n2 * math.log (n2, 2))
	
	if programVocabulary == 0:
		volume = 0
	else:
		volume = programLength * math.log (programVocabulary, 2)

	if n2 == 0:
		difficulty = 0
	else:
		difficulty = (n1 / 2) * (N2 / n2)
	
	effort = difficulty * volume

	return programVocabulary, programLength, calculatedEstimatedProgramLength, volume, difficulty, effort

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
			fc = open("code.cpp", "w")
			fc.write(row['source'])
			fc.write('\n')
			fc.close()

			programVocabulary, programLength, calculatedEstimatedProgramLength, volume, difficulty, effort = halsteadMatrics()

			local_data['sub_id'] = row['sub_id']
			local_data['handle'] = row['handle']
			local_data['language'] = row['language']
			local_data['time'] = row['time']
			local_data['memory'] = row['memory']
			local_data['source'] = row['source']
			local_data['firstName'] = row['firstName']
			local_data['lastName'] = row['lastName']
			local_data['city'] = row['city']
			local_data['country'] = row['country']
			local_data['continent'] = row['continent']
			local_data['maxRank'] = row['maxRank']

			local_data['program_vocabulary'] = programVocabulary
			local_data['program_length'] = programLength
			local_data['calculated_estimated_program_length'] = calculatedEstimatedProgramLength
			local_data['volume'] = volume
			local_data['difficulty'] = difficulty
			local_data['effort'] = effort

			local_data['gender'] = row['gender']

			Final_Data.append(local_data)
			line_count += 1

			
	csvFile.close()
	


main()
write_csv()
