# The purpose of this code is to collect gender using api from genderize.io

import json
import csv
import os.path
from os import path
import requests

input_file = "name.json"
output_file = "gender.json"


gender = {}

def get_gender_from_api(name):
	url = "https://api.genderize.io/?name=" + name
	for _ in range(10):
		try:
			r = requests.get(url)
			data = r.json()
			break
		except json.decoder.JSONDecodeError:
			data = {'error': True}
			break
		except requests.exceptions.ConnectionError as err:
			time.sleep(30)
			print("Connection Error:", str(err))

	if 'error' in data:
		print(data)
		return (None, None)
	if data['gender']:
		return [data['gender'], float(data['probability'])]
	return ['nil', 0.0]

def Merge(dict1, dict2):
	res = {**dict1, **dict2}
	return res

def findGender():
	count = 0
	status = path.isfile(str(output_file))
	if status is False:
		final_data = {}
	else:
		with open(output_file) as f:
			final_data = json.load(f)

	with open(input_file) as f:
		data = json.load(f)

	gender = {}

	for name in data:
		name = name.lower()


		if name not in final_data.keys():

			gender_info = get_gender_from_api(name)
			if gender_info[0] is not None:
				print(name)
				gender[name]={}
				gender[name]['gender']=gender_info[0]
				gender[name]['probability']=float(gender_info[1])

				final_data = Merge(final_data, gender)
				count += 1
			else:
				print('Request limit reached before extracting gender info for ', name)
				break



	with open(output_file, 'w') as fp:
		json.dump(final_data, fp)

	print ('Total data extracted today: ', count)




def main():
	findGender()

main()
