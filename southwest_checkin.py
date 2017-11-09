#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from optparse import OptionParser
from datetime import datetime
from datetime import timedelta
from time import sleep

import os

sendmail_location = "/usr/sbin/sendmail" # sendmail location; this probably won't change

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
parser.add_option("-e", action="store_true", dest="email",
                  help="set to send an email; use --email-from and --email-to as well")
parser.add_option("--email-from", action="store", dest="email_from",
                  help="email address to send from", type="string")
parser.add_option("--email-to", action="store", dest="email_to",
                  help="email address to send to", type="string")

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
driver.get("https://mobile.southwest.com/check-in")

# get text boxes for check in
while True:
	try:
		confirmation_num = driver.find_element_by_name("recordLocator")
		first_name = driver.find_element_by_name("firstName")
		last_name = driver.find_element_by_name("lastName")
		break;
	except NoSuchElementException:
		print("loading checkin...")
		sleep(0.1)

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
submit = driver.find_element_by_class_name("button--yellow");
submit.click()

# wait while the loading spinner is up
try:
	while driver.find_element_by_class_name("dimmer").is_displayed():
		print("loading...")
		sleep(0.1)
except NoSuchElementException:
        print("no spinner found, moving on - hope everything's okay...")

while True:
	# while an error message exists, keep trying!
	try:
		while driver.find_element_by_class_name("popup-showing"):
			print("error displayed, trying again")
			sleep(0.1)
			driver.find_element_by_class_name("confirm-button").click()
			sleep(0.5)
			submit.click()
	except NoSuchElementException:
	        print("no error displayed, moving on!")
		break;

# confirm checkin
print("confirming check in...")
submit = driver.find_element_by_class_name("button--yellow");
submit.click()

# wait while the loading spinner is up
try:
	while driver.find_element_by_class_name("dimmer").is_displayed():
		print("loading...")
		sleep(0.1)
	print("loading done")
except NoSuchElementException:
        print("no spinner found, moving on - hope everything's okay...")

print("checked in - getting boarding position")
boardingPositionDiv = driver.find_element_by_class_name("boarding-group-and-position")
(groupSpan, positionSpan) = boardingPositionDiv.find_elements_by_class_name("xxxlarge")
group = groupSpan.text
position = positionSpan.text
print("Checked in! Boarding position "+group+" "+position+".")

# Send mail, if enabled
if options.email:
	p = os.popen("%s -t" % sendmail_location, "w")
	p.write("From: %s\n" % options.email_from)
	p.write("To: %s\n" % options.email_to)
	p.write("Subject: Southwest Checkin for %s\n" % options.conf_num)
	p.write("\n") # blank line separating headers from body
	p.write("You have been checked in for your flight with confirmation number %s, with boarding position %s." % (options.conf_num, group+" "+position))
	status = p.close()
