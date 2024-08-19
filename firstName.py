# The purpose of this code is to collect all the first name from cleaned_data.csv

import json
import csv
import os.path
from os import path

input_file = "cleaned_data.csv"
name_file = "name.json"


gender = []

def findName():
	count = 0
	record = 0

	with open(input_file, mode='r') as inp:
		csv_reader = csv.DictReader(inp)
		for row in csv_reader:
			record += 1
			if row['firstName'] not in gender:
				gender.append(row['firstName'])
				count += 1

	with open(name_file, 'w') as f:
		json.dump(gender, f)

	print(count)
	print(record)

def main():
	findName()

main()
