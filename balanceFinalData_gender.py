# Balance gender which will be the final data for our experiment

import json
import csv
import os.path
from os import path

# We also ran this program for individual contest problem (cleaned) to get their balanced data

input_file = "final_data.csv"

csv_file1 = "balanceGender.csv"

# Final_Data will hold complete data
Final_Data1 = [] #balance gender

def balancingGender():

	count = 0
	male = 0
	female = 0
	not_matched = 0

	with open(input_file, mode='r') as csvFile:
		csv_reader = csv.DictReader(csvFile)

		for row in csv_reader:
			count += 1

			if row['gender'] == "male":
				male += 1
			elif row['gender'] == "female":
				female += 1
			else:
				not_matched += 1
				print(row['gender'])


		print ('Previous no. of row: ', count)
		print('Male: ', male)
		print ('Female: ', female)
		print ('Not matched:', not_matched)

	m = 0 # this will help to balance the data with number of female coder

	tf = 0
	tm = 0

	with open(input_file, mode='r') as csvFile:
		csv_reader = csv.DictReader(csvFile)
		line_count = 0
		for row in csv_reader:
			local_data = {}

			if row['gender'] == "female" or (row['gender'] == "male" and m < female):
				if row['gender'] == "male":
					m += 1

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
				local_data['gender'] = row['gender']

				Final_Data1.append(local_data)
				line_count += 1



def write_csv1():
	csv_columns = []
	for d in Final_Data1:
		for key in d:
			csv_columns.append(key)
		break
	try:
		status = path.isfile(str(csv_file1))
		with open(csv_file1, 'a+', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			if status is False:
				writer.writeheader()
			for data in Final_Data1:
				writer.writerow(data)
	except IOError:
		print("I/O error")


def test_balance_gender():
	with open(csv_file1, mode='r') as csvFile:
		csv_reader = csv.DictReader(csvFile)
		m = 0
		f = 0
		for row in csv_reader:
			if row['gender'] == "female":
				f += 1
			elif row['gender'] == "male":
				m += 1

		if (m == f):
			print("Gender balanced successfully and written in file")
			print ('Number of records for male and female individually: ', m)
		else:
			print ('Gender is not balanced. Please delete the balanceGender.csv file and check the code')



def main():
	balancingGender()
	write_csv1()
	test_balance_gender()

main()
