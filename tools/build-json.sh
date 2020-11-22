#!/usr/bin/env bash
set -euo pipefail
INPUTDIR=${1:-"missing"}
OUTFILE=${2:-"missing"}
if [[ ${INPUTDIR} == "missing" ]] || [[ ${OUTFILE} == "missing" ]]; then
  echo "Usage: $(basename ${0}) <input file dir> <output file>"
  exit 1
fi
jq . -s ${INPUTDIR}/*.json > ${OUTFILE}
