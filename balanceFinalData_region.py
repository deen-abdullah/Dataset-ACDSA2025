import json
import csv
import os.path
from os import path

input_file = "1344B_.csv"

csv_file2 = "1344B.csv"

# Final_Data will hold complete data
Final_Data2 = [] #balance region


def write_csv2():
	csv_columns = []
	for d in Final_Data2:
		for key in d:
			csv_columns.append(key)
		break
	try:
		status = path.isfile(str(csv_file2))
		with open(csv_file2, 'a+', newline='', encoding="utf8") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			if status is False:
				writer.writeheader()
			for data in Final_Data2:
				writer.writerow(data)
	except IOError:
		print("I/O error")


def balancingRegion():
	continent = []
	with open(input_file, "r", encoding="utf-8") as csvFile:
		csv_reader = csv.DictReader(csvFile)
		for row in csv_reader:
			if row['continent'] not in continent:
				continent.append(row['continent'])

	asia = 0
	europe = 0
	america = 0
	reg = ""
	with open(input_file, mode='r', encoding="utf-8") as csvFile:
		csv_reader = csv.DictReader(csvFile)
		for row in csv_reader:
			if row['continent'] == "Asia":
				asia = asia + 1
			elif row['continent'] == "North America":
				america = america + 1
			elif row['continent'] == "South America":
				america = america + 1
			elif row['continent'] == "Europe":
				europe = europe + 1

	#print ('Asia: ' + str (asia))
	#print ('America: ' + str (america))
	#print ('Europe: ' + str (europe))

	num_of_data = min (asia, (america + europe))

	eastern = 0
	western = 0

	#print (num_of_data)
	with open(input_file, mode='r', encoding="utf-8") as csvFile:
		csv_reader = csv.DictReader(csvFile)
		for row in csv_reader:
			local_data = {}
			if (row['continent'] == "Asia" and eastern < num_of_data) or (row['continent'] == "North America" and western < num_of_data) or (row['continent'] == "South America" and western < num_of_data) or (row['continent'] == "Europe" and western < num_of_data):
				if row['continent'] == "Asia":
					eastern += 1
					reg = "Eastern"
				elif row['continent'] == "Europe":
					western += 1
					reg = "Western"
				elif row['continent'] == "North America" or row['continent'] == "South America":
					western += 1
					reg = "Western"

				local_data['sub_id'] = row['sub_id']
				local_data['handle'] = row['handle']
				local_data['language'] = row['language']
				local_data['time'] = row['time']
				local_data['memory'] = row['memory']
				local_data['source'] = row['source']
				local_data['firstName'] = row['firstName']
				local_data['lastName'] = row['lastName']
				local_data['continent'] = reg
				local_data['gender'] = row['gender']

				Final_Data2.append(local_data)


def test_balance_region():
	with open(csv_file2, mode='r', encoding="utf-8") as csvFile:
		csv_reader = csv.DictReader(csvFile)
		eastern = 0
		western = 0

		for row in csv_reader:
			if row['continent'] == "Eastern":
				eastern += 1
			elif row['continent'] == "Western":
				western += 1

		if eastern == western:
			print("Continent balanced successfully and written in file")
			print ('Number of records for Eastern and Westerm individually: ', eastern)
		else:
			print ('Continent is not balanced. Please delete the balanceRegion.csv file and check the code')


def main():
	balancingRegion()
	write_csv2()
	test_balance_region()

main()
