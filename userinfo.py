# This Program collect all the user information from codeforce

# run this program using python2.7

# -Python imports-
import sys
import json
import requests
#--------------------
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv
import os.path
from os import path
#------------------

#-------------Get Codeforce User List-------------------------------------------------------------
# Generate all the user information and saved on cf_rated_user.json file
CF_USER_LIST_API = 'https://codeforces.com/api/user.ratedList?'
FILE = 'cf_rated_users.json'

def get_codeforce_user_list():
	print("Fetching Codeforces users's information...")
	r = requests.get(CF_USER_LIST_API)
	data = r.json()

	if data['status'] != 'OK':
		print("The request failed:", data)
		sys.exit()

	with open(FILE, 'w') as f:
		json.dump(data['result'], f)
		print("User list created:", FILE)
#-----------------------------------------

#-----------------------------------------
# Purpose of this function is to format the cf_rated_user.json file
# So that we can search information by 'handle'
# From cf_rated_user.json file we will extract "handle", "firstName", "lastName", "city", "country", "maxRank"
def formattingJson():
	with open('cf_rated_users.json') as f:
		data = json.load(f)
	handle = {}

	for d in data:
		handle[d["handle"]]={}

		if ("firstName" in d):
			handle[d["handle"]]["firstName"]=d["firstName"]
		else:
			handle[d["handle"]]["firstName"]= ""

		if ("lastName" in d):
			handle[d["handle"]]["lastName"]=d["lastName"]
		else:
			handle[d["handle"]]["lastName"] = ""

		if ("city" in d):
			handle[d["handle"]]["city"]=d["city"]
		else:
			handle[d["handle"]]["city"]=""

		if ("country" in d):
			handle[d["handle"]]["country"]=d["country"]
		else:
			handle[d["handle"]]["country"]=""

		if ("maxRank" in d):
			handle[d["handle"]]["maxRank"]=d["maxRank"]
		else:
			handle[d["handle"]]["maxRank"]= ""

	with open('cf_rated_users.json', 'w') as fp:
		json.dump(handle, fp)
#----------------------------------------------------------------------------------------------------


def main():
	get_codeforce_user_list()
	formattingJson();

main()
