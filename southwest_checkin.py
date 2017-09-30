#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

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
parser.add_option("-H", "--headless", action="store_true", dest="headless",
				  help="set to run headless and simulate a display")

(options, args) = parser.parse_args()

if options.headless:
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(800, 600))
	display.start()

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# create a wait driver
wait = WebDriverWait(driver,10)

# go directly to the checkin page
driver.get("https://www.southwest.com/flight/retrieveCheckinDoc.html")

# get text boxes for check in
confirmation_num = driver.find_element_by_id("confirmationNumber")
first_name = driver.find_element_by_id("passengerFirstName")
last_name = driver.find_element_by_id("passengerLastName")

# insert data
confirmation_num.send_keys(options.conf_num)
first_name.send_keys(options.first_name)
last_name.send_keys(options.last_name)

# busy wait until it is the desired time
des_time = datetime.strptime(options.time, '%b %d %Y %I:%M%p')
des_time_minus_6s = des_time - timedelta(seconds=6)
des_time_minus_30m = des_time - timedelta(minutes=30)
cur_time = datetime.now()
while des_time_minus_30m > cur_time:
	print("Waiting for checkin time " + str(des_time) + ". Time now is: " + str(cur_time) + ". Waiting 30min.")
	sleep(29*60)
	cur_time = datetime.now()
while des_time_minus_6s > cur_time:
	print("Waiting for checkin time " + str(des_time) + ". Time now is: " + str(cur_time) + ". Waiting 5s.")
	sleep(5)
	cur_time = datetime.now()
while des_time > cur_time:
	cur_time = datetime.now()

# check in!
print("checking in...")
driver.find_element_by_id("form-mixin--submit-button").click()

# while an error message exists, keep trying!
try:
	while driver.find_element_by_class_name("message-error"):
		print("error displayed")
		sleep(0.1)
		submit.click()
except NoSuchElementException:
        print("no error displayed, moving on!")

# confirm checkin
while True:
	try:
		checkInConfirm = driver.find_element_by_class_name('submit-button')
		while checkInConfirm.get_attribute("disabled") is not None:
			try:
				print("waiting to click confirm button")
				sleep(0.1)
				checkInConfirm = driver.find_element_by_class_name('submit-button')
			except WebDriverException:
				# this sometimes fails, give it a moment and try again
				sleep(0.1)
				checkInConfirm = driver.find_element_by_class_name('submit-button')
		checkInConfirm.click()
		break;
	except NoSuchElementException, StaleElementReferenceException:
		print("submit button not found, retrying")
		sleep(0.1)
print("checked in - getting boarding position")
boardingPositionDiv = driver.find_element_by_class_name("air-check-in-passenger-item--information-boarding-position")
boardingPositionSpan = boardingPositionDiv.find_element_by_class_name("swa-g-screen-reader-only")
position = boardingPositionSpan.get_attribute('innerHTML')
print(position)
