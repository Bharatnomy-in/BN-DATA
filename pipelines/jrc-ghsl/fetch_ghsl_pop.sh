#!/bin/sh
# Download JRC GHSL population grids (GHS-POP R2023A, WGS84, 30 arc-seconds), epochs 1975-2030, and keep only the
# GeoTIFF. No login. About 5.8 GB of zips (482 MB each); the zips are deleted after unzipping.
# Run from the repo root:  sh pipelines/jrc-ghsl/fetch_ghsl_pop.sh
set -e
R=_sources/jrc-ghsl/raw
mkdir -p "$R"
B=https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A
for e in 1975 1980 1985 1990 1995 2000 2005 2010 2015 2020 2025 2030; do
  n=GHS_POP_E${e}_GLOBE_R2023A_4326_30ss
  [ -s "$R/${n}_V1_0.tif" ] && continue
  curl -sL -m 3600 -o "$R/$n.zip" "$B/$n/V1-0/${n}_V1_0.zip"
  unzip -o -q "$R/$n.zip" "*.tif" -d "$R"
  rm "$R/$n.zip"
  echo "done $e"
done
ls "$R"/GHS_POP_*.tif | wc -l
