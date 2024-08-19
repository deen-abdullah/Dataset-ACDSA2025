# The purpose of this code is to clean data from raw_data.csv
# FOr each contest problems (there are 9 for our experiment), we need to clean each files
# After cleaning all individual contest problems, we manually combine them to get full data in one file: 'cleaned_data.csv'

import json
import csv
import os.path
from os import path

input_file = "1344BMerged.csv"
output_file = "cleaned_1344BMerged.csv"

# Final_Data will hold complete data
Final_Data = []

def cleanData():
	program = ['Python 3', 'PyPy 3', 'PyPy 2', 'Java 8', 'Kotlin', 'GNU C11', 'JavaScript', 'D', 'Node.js', 'Java 11', 'Delphi', 'Python 2', 'Rust', 'Mono C#', 'Haskell', 'Go', 'Clang++17 Diagnostics', 'Scala']

	count = 0


	with open(input_file, mode='r') as inp:
		csv_reader = csv.DictReader(inp)
		for row in csv_reader:
			local_data = {}
			if row['firstName'] != '' and row['language'] not in program:
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
				local_data['maxRank'] = row['maxRank']

				Final_Data.append(local_data)

				count += 1

	print(count)


def write_csv():
	csv_columns = []
	for d in Final_Data:
		for key in d:
			csv_columns.append(key)
		break
	try:
		status = path.isfile(str(output_file))
		with open(output_file, 'a+', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			if status is False:
				writer.writeheader()
			for data in Final_Data:
				writer.writerow(data)
	except IOError:
		print("I/O error")

def main():
	cleanData()
	write_csv()

main()
