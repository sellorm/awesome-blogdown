#!/usr/bin/env bash
USERAGENT="awesome-blogdown.com site availability check"

if [[ -z ${1} ]]; then
  error=0
  for i in $(curl -s https://awesome-blogdown.com/sites.json | jq '.[] | .url')
  do
    curl -A ${USERAGENT} -s -I ${i//\"/} | grep ^HTTP | grep '200 OK' > /dev/null
    if [[ $? -eq 0 ]]; then
      echo "${i} - OK"
    else
      echo "${i} - FAIL"
      let error=${error}+11
    fi
  done
  if [[ ${error} -ne 0 ]]; then
    exit 1
  else
    exit 0
  fi
else
  curl -A ${USERAGENT} -s -I ${1//\"/}
fi

