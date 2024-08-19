# This Program Fetch User Information and Submitted Code from Codeforce

# Run this program in Python3

# The url of the targeted problem should be set here
url = "https://codeforces.com/problemset/status/1324/problem/F/page/80?order=BY_PROGRAM_LENGTH_ASC"
# for problem number: 1324F, Next will start from page=110
csv_file = "1324F.csv"

Number_of_Page = 30	# Number of pages for each run

# Final_Data will hold complete data
Final_Data = []

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
# For Selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException, WebDriverException
#------------------

#-------------Get Codeforce User List-------------------------------------------------------------
# Generate all the user information and saved on cf_rated_user.json file
# If the file is already created, then dont need to run again, we will use the existing one
# To active this function uncomment the function from Main
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
#----------------------------------------------------------------------------------------------------

# ------------Just convert .json userfile into .data format------------------------------------------
# Steve used this approach to add the gender and the probaility, but we will add it after fetching coding information
# So, this function is doing the convertion from .json to .data file format
raw_file = 'raw.data'
def format_data ():
	with open(FILE) as file:
		user_list = json.load(file)

	raw = []

	for i, user in enumerate(user_list):
		raw.append(user)

	with open(raw_file, 'w') as file:
		json.dump(raw, file)
#-----------------------------------------------------------------------------------------------------

#------------------Selenium Data Collection-----------------------------------------------------------
# From Pop-up, this driver will collect code according to the submissionID
def codeCollectionPopup(driver, sub_id):

	elem = driver.find_element_by_link_text(sub_id) #submissionID
	driver.execute_script("arguments[0].scrollIntoView();", elem)
	elem.send_keys(Keys.RETURN)

	time.sleep(3)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	code = soup.find('div', {'class': 'popup'})

	src_html = []
	for tag in code.find_all('li'):
		src_html.append(tag.text)
	if src_html:
		source = "\n".join(src_html)
	else:
		source = ""

	# closing popup
	try:
		close = driver.find_element_by_class_name('close')
		driver.execute_script("arguments[0].scrollIntoView();", close)
		close.send_keys(Keys.RETURN)
		time.sleep(2)
	except ElementNotInteractableException as error:
		print(error)
		while True:
			try:
				driver.refresh()
				break
			except TimeoutException:
				print("Timeout: Trying to refresh again")
	return source
#------------------------------------------------------------------------------------------------------

#-------------------------To get the information from the table oneped in browser--------------------
# This function is called by collectCodeInfo function. This function returns the submissionID with corresponding user's handle
def table_read(driver):
	soup = BeautifulSoup(driver.page_source, "lxml")

	table = soup.find_all('table')[0]
	df = pd.read_html(str(table))
	dt = df[0].to_dict(orient='records')

	return dt
#-----------------------------------------------------------------------------------------------------

#-----------------------Open Browser according to the given problem link------------------------------
# fetch user information who have submitted the code,
# according to SubmissionId - the function will call codeCollection function to collect corresponding soource code
def collectCodeInfo(driver):

	dt = table_read(driver)

	for d in dt:
		local_data = {}
		if d['Verdict'] == "Accepted":
			print('Accessing information for ',d['#'])
			local_data['sub_id'] = d['#']
			local_data['handle'] = d['Who']
			local_data['language'] = d['Lang']
			local_data['time'] = d['Time']
			local_data['memory'] = d['Memory']
			source = codeCollectionPopup(driver,str(d['#']))
			local_data['source'] = source
			Final_Data.append(local_data)


def page_surfing():
	Page_Number = 1
	driver = webdriver.Firefox()
	driver.set_page_load_timeout(30)
	driver.implicitly_wait(5)

	driver.get(url)
	collectCodeInfo(driver)

	while True:
		try:
			print("Navigating to Next Page")
			Page_Number = Page_Number + 1
			driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[last()]/a[@class='arrow']"))))
			driver.find_element_by_xpath("//li[last()]/a[@class='arrow']").click()
			collectCodeInfo(driver)

			if Page_Number == Number_of_Page:
				break

		except (TimeoutException, WebDriverException) as e:
			print("Last page reached")
			break

	driver.close()


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
	#get_codeforce_user_list()   # uncomment the function, if we want to fetch user information. If the file 'cf_rated_user.json' exist then dont need to run this function
	#format_data()				 # uncomment the function, if we want to convert 'cf_rated_user.json' file into 'raw.data'

	page_surfing()
	write_csv()

main()
