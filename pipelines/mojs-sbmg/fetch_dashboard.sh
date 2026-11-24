#!/bin/sh
# Save the SBM-G (Swachh Bharat Mission - Grameen) states dashboard page into raw/. Run from the repo root.
# The page embeds the district-wise ODF Plus village counts as a JavaScript array (markersDistrict).
# Usage: sh pipelines/mojs-sbmg/fetch_dashboard.sh YYYY-MM-DD   (the "as on" date printed on the page)
set -e
D=${1:?give the date printed on the page, YYYY-MM-DD}
curl -L -A "Mozilla/5.0" -o "_sources/mojs-sbmg/raw/mojs-sbmg_states-dashboard_${D}.html" \
  https://sbm.gov.in/sbmgdashboard/statesdashboard.aspx
