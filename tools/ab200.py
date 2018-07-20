#!/usr/bin/env python3
import requests
import sys
import os

sites = requests.get('https://awesome-blogdown.com/sites.json').json()
headers = {'user-agent': 'awesome-blogdown.com site availability checker'}
num_errors = 0

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
message = "awesome-blogdown.com site checker found "+num_errors+" today"
webhook_url = os.environ['SLACK_WEBHOOK_URL']
slack_data = {'text': message}

response = requests.post(webhook_url, json=slack_data)

if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )


sys.exit(num_errors)
      
    
