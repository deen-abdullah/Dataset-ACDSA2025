# Merging contest problems with user information from cf_rated_user
# Example: Input files: cf_rated_users.json & 1288D.csv

import json
import csv
import os.path
from os import path

# For each run we have set input and output files name
input_file = "1344B.csv"
csv_file = "1344BMerged.csv"

# Final_Data will hold complete data
Final_Data = []

# Purpose of this function is to merge code-submission-info from 1288D.csv file with user-info from cf_rated_users.json
# We search information by 'handle'
# From cf_rated_user.json file we will extract "handle", "firstName", "lastName", "city", "country", "maxRank" and will merge them on 1288D.csv
def merging():
	with open('cf_rated_users.json') as f:
		data = json.load(f)

	count = 0

	with open(input_file, mode='r') as csvFile:
		csv_reader = csv.DictReader(csvFile)
		line_count = 0

		for row in csv_reader:
			count += 1
			local_data = {}

			if line_count == 0:
				line_count += 1

			if row['handle'] in data:
				local_data['sub_id'] = row['sub_id']
				local_data['handle'] = row['handle']
				local_data['language'] = row['language']
				local_data['time'] = row['time']
				local_data['memory'] = row['memory']
				local_data['source'] = row['source']

				local_data['firstName'] = data[row['handle']]['firstName']
				local_data['lastName'] = data[row['handle']]['lastName']
				local_data['city'] = data[row['handle']]['city']
				local_data['country'] = data[row['handle']]['country']
				local_data['maxRank'] = data[row['handle']]['maxRank']

				Final_Data.append(local_data)
				line_count += 1

			else:
				print ('Handle not match for ', row['handle'])

		print ('Previous no. of row: ', count-1)
		print('New number of row: ',line_count-1)


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


def main():
	merging();
	write_csv()

main()
