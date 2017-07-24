# Southwest-Checkin
An easy python script to continuously retry checking into your Southwest flight using ChromeDriver and Selenium.  Effectively checking you in at the moment it becomes available!

### Example
	python southwest_checkin.py -c TESTER -f Testy -l McTest -t 'Jul 02 2017 07:00AM'

### Requirements
install the selenium python library with pip via `pip install -r requirements.txt`
Also requires chromedriver to be in the PATH environment variable, the MAC OSX chrome driver is in this repo, other versions are available [here](https://sites.google.com/a/chromium.org/chromedriver/downloads)

### Options
	* -c the confirmation number string
	* -f the first name for the confirmation
	* -l the last name for the confirmation
    * -t date and time of check in

`-t` value must be in the following format: `%b %d %Y %I:%M%p`

Refer to the [Python documentation](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior) for a complete explanation of the date format. Also keep in mind, you may need to convert the date/time to your local time zone.

### Notice
Try not to activate this script for very long if you can help it, constantly requesting webpages can cause issues for the webserver.
