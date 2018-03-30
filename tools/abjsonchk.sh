#!/usr/bin/env bash
cat ../docs/sites.json | jq '' >/dev/null
if [[ $? -eq 0 ]]; then
  echo "json validity check - PASS"
  exit 0
else
  echo "json validity check - FAIL"
  exit 1
fi
