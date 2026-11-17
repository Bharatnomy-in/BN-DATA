#!/bin/sh
# Download every monthly CEA "Energy Power Supply Position" PDF listed in raw/cea-psp_energy_file-list.tsv
# (month, type, file id; listed from https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1003&subSubHeadingId=10010&title=Power%20Supply%20Position%20-%20Energy&lang=en).
# Run from the repo root:  sh pipelines/cea/fetch_psp_energy.sh
R=_sources/cea-power-supply-position/raw
while IFS="$(printf '\t')" read -r month kind id; do
  f="$R/cea-psp_energy_$month.pdf"
  [ "$kind" = pdf ] || continue
  [ -s "$f" ] && continue
  curl -sL -m 120 -o "$f" "https://cea.nic.in/api/dashboardReports/download-pdf/en/$id"
  sleep 0.5
done < "$R/cea-psp_energy_file-list.tsv"
ls "$R"/cea-psp_energy_*.pdf | wc -l
