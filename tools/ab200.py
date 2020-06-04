#!/usr/bin/env python3
"""
This utility parses the json file from awesome-blogdown.com, and then checks all
sites it finds are actually up.
No checks are made over the content of the site
"""


import os
import sys
import requests


# set the user agent for the checker - good manners cost nothing
HEADERS = {'user-agent': 'awesome-blogdown.com site availability checker'}


# check for a URL passed on the command line
try:
    sys.argv[1]
    CLIRESPONSE = requests.get(sys.argv[1], headers=HEADERS)
    if CLIRESPONSE.ok:
        CHECK_STATUS_MSG = "OK"
    else:
        CHECK_STATUS_MSG = "FAIL"
    print(sys.argv[1]+" - "+str(CLIRESPONSE.status_code)+" - "+CHECK_STATUS_MSG)
    sys.exit()
except IndexError:
    print("No CLI input defined - continuing...")



# check for the BLOGDOWN_JSON_URL else error and quit
try:
    BLOGDOWN_JSON_URL = os.environ['BLOGDOWN_JSON_URL']
except KeyError:
    print("Error: BLOGDOWN_JSON_URL environment variable not defined")
    sys.exit(1)


# get the sites.json file from BLOGDOWN_JSON_URL
SITES = requests.get(BLOGDOWN_JSON_URL).json()


# set an initial number of errors at zero
NUM_ERRORS = 0


# set initial number of sites that pass the checks
NUM_PASSED = 0


# check for the SLACK_WEBHOOK_URL else error and quit
try:
    WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
except KeyError:
    print("Error: SLACK_WEBHOOK_URL environment variable not defined")
    sys.exit(1)


# URL information class - contains useful info about a given URL
class URLInfo:
    """
    Container for information about supplied URLs
    """
    def __init__(self, url):
        self.url = url
        self.status_msg = "Unchecked"
        self.status_code = 0
        self.is_error = False

    def check_url(self):
        """
        check the given URL and use the results to populate object properties
        """
        try:
            urlresponse = requests.get(self.url, headers=HEADERS)
            urlresponse.raise_for_status()
            self.status_code = urlresponse.status_code
            if urlresponse.ok:
                self.status_msg = "OK"
            else:
                self.status_msg = "Fail"
                self.is_error = True
        except requests.exceptions.SSLError:
            # retry but without verifying the certs
            urlresponse = requests.get(self.url, headers=HEADERS, verify=False)
            self.status_code = urlresponse.status_code
            self.status_msg = "SSL Error"
        except requests.exceptions.HTTPError:
            self.status_msg = "HTTP Error"
            self.is_error = True
        except requests.exceptions.ConnectionError:
            self.status_msg = "Connection Error"
            self.is_error = True
        except requests.exceptions.Timeout:
            self.status_msg = "Timeout"
            self.is_error = True
        except requests.exceptions.RequestException:
            self.status_msg = "Request Exception"
            self.is_error = True


# cycle throught the sites and run the availability check
for site in SITES:
    site_data = URLInfo(site['url'])
    site_data.check_url()
    print("{} - {} - {}".format(site_data.url, site_data.status_code,
                                site_data.status_msg))
    if site_data.is_error:
        NUM_ERRORS = NUM_ERRORS + 1
    else:
        NUM_PASSED = NUM_PASSED + 1


# create summary message for console and slack
MESSAGE = "awesome-blogdown.com site checker found {} errors today. {}/{} " \
          "passed.".format(str(NUM_ERRORS), str(NUM_PASSED), str(len(SITES)))
print(MESSAGE)


# build the slack payload
SLACK_DATA = {'username': 'awesome-blogdown-checker', 'text': MESSAGE}


# post to slack
RESPONSE = requests.post(WEBHOOK_URL, json=SLACK_DATA)


# check for errors
if RESPONSE.status_code != 200:
    raise ValueError(
        'Request to slack returned an error {}, the response is:\n{}'.format(
            RESPONSE.status_code, RESPONSE.text)
    )


# Exit the program using the number of errors as the exit code
sys.exit(NUM_ERRORS)
