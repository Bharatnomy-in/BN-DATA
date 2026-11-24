# Power plants of India with location and district, 2021 release

One row per power plant (1,589 plants of every fuel: coal, gas, oil, nuclear, hydro, solar, wind, biomass), with capacity, coordinates, owner and commissioning year as published by WRI, plus the district the plant's point falls in.

## Source

- **Data:** World Resources Institute (WRI), Global Power Plant Database v1.3.0 (released June 2021). Licence CC BY 4.0. WRI compiled it from CEA (capacity data year 2019 for 492 plants), Wiki-Solar, CDM project documents and company sources; the `source` column names each one.
- **Table taken from:** `global_power_plant_database.csv`, rows with `country` = `IND`
- **Link:** https://datasets.wri.org/dataset/globalpowerplantdatabase (file: https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip)
- **Downloaded:** 24 Nov 2026
- **Script:** [`_sources/wri-gppd/scripts/build_power_plants.py`](../_sources/wri-gppd/scripts/build_power_plants.py); checks in `check_power_plants.py`

Not an official Indian government release: CEA does not publish plant coordinates. Used with the user's approval (24 Nov 2026) because it is the only free, script-downloadable source of plant locations.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | State/UT the plant's point falls in, from the 2011 district boundary and [`_reference/geography.csv`](../_reference/geography.csv) (added by Bharatnomy) |
| `district`, `lgd_district_code`, `district_census_code` | 2011 district the point falls in, with its current LGD name and code (added by Bharatnomy) |
| `plant` | Plant name as published |
| `gppd_idnr` | WRI plant ID (unique key) |
| `capacity_mw` | Electrical generating capacity, MW |
| `latitude`, `longitude` | Plant location, decimal degrees (WGS84) |
| `primary_fuel` | Main fuel: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biomass |
| `other_fuel1`, `other_fuel2`, `other_fuel3` | Other fuels, if any |
| `commissioning_year` | Year of commissioning (capacity-weighted average for plants with several units, as WRI publishes it) |
| `owner` | Owner as published |
| `source`, `url` | Who reported the plant, and a link |
| `geolocation_source` | Who supplied the coordinates (WRI, Wiki-Solar, Industry About, NREL) |
| `wepp_id` | Plant ID in the Platts World Electric Power Plants database, where known |
| `year_of_capacity_data` | Year the capacity figure refers to (2019 for CEA plants; blank for others) |
| `generation_data_source` | Source of reported generation (see the generation table) |
| `district_match` | How the district was found (Bharatnomy): `inside` (point inside a district), `nearest_within_11km` (point just outside every boundary: coast, river or border; nearest district within 0.1°), `outside_all_districts` |
| `source_flag` | `not_available` where the place columns are blank because the point is outside every 2011 district |

## Notes

- Districts are 2011 boundaries (DataMeet Census 2011 map). Plants in districts created after 2011 carry the parent district, e.g. Dahanu (Palghar since 2014) is listed under Thane. Telangana and other new states are correct because `geography.csv` gives each 2011 district its present state.
- 7 points fall outside every boundary: 6 go to the nearest district (Uri, Kasaragod DG, Dahanu, Kudankulam, Tuticorin JV, Dhauli Ganga); Uri-II (Jammu & Kashmir) is beyond the 2011 map's border line and is left blank.
- The database is frozen at 2021: plants commissioned after about 2020 (much of India's newer solar and wind) are missing. Capacities for non-CEA plants can be older than 2019. Compare with `ENG_installed-capacity_*` (CEA) for current state totals.
- Blank cells in `other_fuel*`, `commissioning_year`, `owner`, `url`, `wepp_id`, `year_of_capacity_data` and `generation_data_source` are blank in the source, which does not say why.
- Generation figures are in [`ENG_power-plant-generation_2013-to-2019_STATES_WRI_DIST`](../ENG_power-plant-generation_2013-to-2019_STATES_WRI_DIST/).
- Checks (24 Nov 2026): 1,589 rows = India rows in the source; `gppd_idnr` unique; all `state_ut` in the list; capacity > 0; coordinates inside India's bounding box; 5 random rows match the source file.
