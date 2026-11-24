# WRI Global Power Plant Database

Used for [`ENG_power-plants_2021_STATES_WRI_DIST/`](../../ENG_power-plants_2021_STATES_WRI_DIST/) and [`ENG_power-plant-generation_2013-to-2019_STATES_WRI_DIST/`](../../ENG_power-plant-generation_2013-to-2019_STATES_WRI_DIST/).

- **Data:** World Resources Institute, Global Power Plant Database v1.3.0 (June 2021), CC BY 4.0. About 35,000 plants in 167 countries; this repo takes the 1,589 India rows (all the columns WRI publishes for India).
- **Link:** https://datasets.wri.org/dataset/globalpowerplantdatabase ; file https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip (no login)
- **Downloaded:** 24 Nov 2026; `raw/` holds the zip (4 MB: CSV, WRI's README, release notes and two method papers). Re-download with `sh pipelines/wri-gppd/fetch_gppd.sh`.
- **Not official:** CEA publishes plant lists without coordinates; WRI is used with the user's approval as the only free source of plant locations.
