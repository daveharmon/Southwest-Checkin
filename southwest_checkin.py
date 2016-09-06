from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from optparse import OptionParser
from datetime import datetime

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

# go to the google home page
driver.get("http://www.southwest.com")

# the page is ajaxy so the title is originally this:
print driver.title

# click the checkin box
checkin = driver.find_element_by_id("booking-form--check-in-tab")
while not checkin.is_displayed():
	print 
checkin.click()

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
cur_time = datetime.strptime(datetime.now().strftime('%b %d %Y %I:%M%p'), '%b %d %Y %I:%M%p')
while des_time > cur_time:
	cur_time = datetime.strptime(datetime.now().strftime('%b %d %Y %I:%M%p'), '%b %d %Y %I:%M%p')
	print str(des_time), ' =/= ', str(cur_time)

# check in!
driver.find_element_by_id("jb-button-check-in").click()

# while it is too early, keep retrying!
while True:
	submit = driver.find_element_by_id("submitButton")
	oops = driver.find_element_by_class_name("oopsError_message")
	while not submit.is_displayed():
		print ""
	if not oops.is_displayed():
		print "No Error!  Should be checked in!!!"
		break
	submit.click()

# Print Documents
printDocs = driver.find_element_by_id('printDocumentsButton')
while not printDocs.is_displayed():
	print
printDocs.click()

