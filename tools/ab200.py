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


# set initial number of sites checked
num_checked = 0


# check for the SLACK_WEBHOOK_URL else error and quit
try:
  webhook_url = os.environ['SLACK_WEBHOOK_URL']
except:
  print("Error: problem with SLACK_WEBHOOK_URL environment variable")
  sys.exit(1)


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
    num_checked = num_checked + 1
  except:
    # did we except because of an SSL issue?
    # try again but skip cert verification
    try:
      r = requests.get(site['url'], headers = headers, verify = False)
      if r.ok:
        code_check_status = "SSL Failure"
      else:
        code_check_status = "FAIL"
        num_errors = num_errors + 1
      print(site['url']+" - "+str(r.status_code)+" - "+code_check_status)
      num_checked = num_checked + 1
    except:
      print(site['url']+" - Unknown error")
      num_errors = num_errors + 1
  

# post results to slack
message = "awesome-blogdown.com site checker found {} errors today. {}/{} " \
          "perfects.".format(str(num_errors), str(num_checked), str(len(sites)))


# what are we posting to slack?
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
