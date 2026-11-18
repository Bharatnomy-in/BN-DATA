#!/bin/sh
# Download Global Solar Atlas (v2, Solargis / World Bank ESMAP, CC BY 4.0) country GIS data for India:
# long-term yearly and monthly averages of daily totals (GHI, DNI, DIF, GTI, PVOUT, OPTA, TEMP), GeoTIFF.
# No login. About 850 MB zip; the zip is deleted after unzipping (raw/ is git-ignored).
# File list: https://api.globalsolaratlas.info/download/India
# Run from the repo root:  sh pipelines/global-solar-atlas/fetch_gsa.sh
set -e
R=_sources/global-solar-atlas/raw
mkdir -p "$R"
n=India_GISdata_LTAym_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF
if [ -z "$(ls "$R"/*.tif 2>/dev/null)" ]; then
  curl -sL -m 7200 -o "$R/$n.zip" "https://api.globalsolaratlas.info/download/India/$n.zip"
  unzip -o -q "$R/$n.zip" -d "$R"
  rm "$R/$n.zip"
fi
find "$R" -name "*.tif" | sort
