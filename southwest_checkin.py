#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from optparse import OptionParser
from datetime import datetime
from datetime import timedelta
from time import sleep

parser = OptionParser()
parser.add_option("-c", "--confirmation_num", action="store", dest="conf_num",
                  help="confirmation number for flight", type="string")
parser.add_option("-f", "--first_name", action="store", dest="first_name",
                  help="first name for flight", type="string")
parser.add_option("-l", "--last_name", action="store", dest="last_name",
                  help="last name for flight", type="string")
parser.add_option("-t", "--time", action="store", dest="time",
				  help="time to start checkin attempts", type="string")

(options, args) = parser.parse_args()

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# create a wait driver
wait = WebDriverWait(driver,10)

# go directly to the checkin page
driver.get("https://www.southwest.com/flight/retrieveCheckinDoc.html")

# get text boxes for check in
confirmation_num = driver.find_element_by_id("confirmationNumber")
first_name = driver.find_element_by_id("firstName")
last_name = driver.find_element_by_id("lastName")

# insert data
confirmation_num.send_keys(options.conf_num)
first_name.send_keys(options.first_name)
last_name.send_keys(options.last_name)

# busy wait until it is the desired time
des_time = datetime.strptime(options.time, '%b %d %Y %I:%M%p')
des_time_minus_6s = des_time - timedelta(seconds=6)
cur_time = datetime.now()
while des_time_minus_6s > cur_time:
	print("Waiting for checkin time " + str(des_time) + ". Time now is: " + str(cur_time))
	sleep(5)
	cur_time = datetime.now()
while des_time > cur_time:
	cur_time = datetime.now()

# check in!
driver.find_element_by_id("submitButton").click()

# while it is too early, keep retrying!
oops = driver.find_element_by_class_name("oopsError_message")
while oops.is_displayed():
	submit = driver.find_element_by_id("submitButton")
	while not submit.is_displayed():
		print("error displayed")
	submit.click()
	oops = driver.find_element_by_class_name("oopsError_message")

# Print Documents
printDocs = driver.find_element_by_id('printDocumentsButton')
while not printDocs.is_displayed():
	print()
printDocs.click()
