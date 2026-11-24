#!/bin/sh
# Download WRI Global Power Plant Database v1.3 (CC BY 4.0) into raw/. Run from the repo root.
curl -L -o _sources/wri-gppd/raw/wri-gppd_global-power-plant-database_v1-3.zip \
  https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip
