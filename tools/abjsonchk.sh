#!/usr/bin/env bash
set -euo pipefail
INFILE=${1:-"missing"}

if [[ ${INFILE} == "missing" ]]; then
  echo "Usage: $(basename ${0}) <input file>"
  exit 1
fi

cat ${INFILE} | jq '' >/dev/null
if [[ $? -eq 0 ]]; then
  echo "$(date +%D-%T) - json validity check - PASS"
  exit 0
else
  echo "$(date +%D-%T) - json validity check - FAIL"
  exit 1
fi
