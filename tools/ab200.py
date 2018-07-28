#!/usr/bin/env python3
"""
This utility parses the json file from awesome-blogdown.com, and then checks all
sites it finds are actually up.
No checks are made over the content of the site
"""


import requests, sys, os


# set the user agent for the checker - good manners cost nothing
headers = {'user-agent': 'awesome-blogdown.com site availability checker'}


# check for a URL passed on the command line
try:
  sys.argv[1]
  r = requests.get(sys.argv[1], headers = headers)
  if r.ok:
    code_check_status = "OK"
  else:
    code_check_status = "FAIL"
  print(sys.argv[1]+" - "+str(r.status_code)+" - "+code_check_status)
  sys.exit()
except IndexError:
  print("No CLI input defined - continuing...")
    
  

# check for the BLOGDOWN_JSON_URL else error and quit
try:
  blogdown_json_url = os.environ['BLOGDOWN_JSON_URL']
except:
  print("Error: problem with BLOGDOWN_JSON_URL environment variable")
  sys.exit(1)


# get the sites.json file from blogdown_json_url
sites = requests.get(blogdown_json_url).json()


# set an initial number of errors at zero
num_errors = 0


# set initial number of sites that pass the checks
num_passed = 0


# check for the SLACK_WEBHOOK_URL else error and quit
try:
  webhook_url = os.environ['SLACK_WEBHOOK_URL']
except:
  print("Error: problem with SLACK_WEBHOOK_URL environment variable")
  sys.exit(1)


# URL information class - contains useful info about a given URL
class URLInfo:
  def __init__(self, url):
    self.url = url
    self.status_msg = "Unchecked"
    self.status_code = 0
    self.is_error = False

  def check_url(self):
    try:
      r = requests.get(self.url, headers = headers)
      if r.ok:
        self.status_msg = "OK"
      else:
        self.status_msg = "Fail"
        self.is_error = True
      self.status_code = r.status_code
    except:
      # see if we failed due to an SSL error
      try:
        r = requests.get(self.url, headers = headers, verify = False)
        if r.ok:
          self.status_msg = "SSL Failure"
        else:
          self.status_msg = "FAIL"
          self.is_error = True
        self.status_code = r.status_code
      except:
        self.status_msg = "Unknown Error"
        self.is_error = True
    

# cycle throught the sites and run the availability check
for site in sites:
  site_data = URLInfo(site['url'])
  site_data.check_url()
  print("{} - {} - {}".format(site_data.url, site_data.status_code,
                              site_data.status_msg))
  if site_data.is_error:
    num_errors = num_errors + 1
  else:
    num_passed = num_passed + 1
  

# create summary message for console and slack
message = "awesome-blogdown.com site checker found {} errors today. {}/{} " \
          "passed.".format(str(num_errors), str(num_passed), str(len(sites)))
print(message)


# build the slack payload
slack_data = {'username': 'awesome-blogdown-checker', 'text': message}


# post to slack
response = requests.post(webhook_url, json=slack_data)


# check for errors
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )


# Exit the program using the number of errors as the exit code
sys.exit(num_errors)
