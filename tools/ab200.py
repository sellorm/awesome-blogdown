#!/usr/bin/env python3
"""
This utility parses the json file from awesome-blogdown.com, and then checks all
sites it finds are actually up.
No checks are made over the content of the site
"""

import requests, sys, os

# get the ab sites json
sites = requests.get('https://awesome-blogdown.com/sites.json').json()

# set the user agent for the checker - good manners cost nothing
headers = {'user-agent': 'awesome-blogdown.com site availability checker'}

# set an initial number of errors at zero
num_errors = 0

# cycle throught the sites and run the availability check
for site in sites:
  try:
    r = requests.get(site['url'], headers = headers)
    if r.ok:
      code_check_status = "OK"
    else:
      code_check_status = "FAIL"
      num_errors = num_errors + 1
    print(site['url']+" - "+str(r.status_code)+" - "+code_check_status)
  except:
    print(site['url']+" - "+str(r.status_code)+" - Unknown error")
    if r.ok == False:
      num_errors = num_errors + 1


# post results to slack
message = "awesome-blogdown.com site checker found "+str(num_errors)+" errors today"

# need some error handling around this really - in case it's not set
webhook_url = os.environ['SLACK_WEBHOOK_URL']

# what are we posting to slack?
slack_data = {'username': 'awesome-blogdown-checker', 'text': message}

response = requests.post(webhook_url, json=slack_data)

# check for errors
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )


# Exit the program using the number of errors as the exit code
sys.exit(num_errors)
      
    
