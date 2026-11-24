# Fly ash from coal power plants by district, Maharashtra, 2025-26

For each of Maharashtra's 19 coal power plants: the district it is in, the ash it produced in 2025-26 and how much ash was put to use (cement, bricks, roads, mine filling and so on).

## Source

- **Data:** Central Electricity Authority (CEA), *Fly Ash Generation at Coal / Lignite Based Thermal Power Stations and its Utilization in the Country*, Year Book 2026 (FY 2025-26), Table 5.9 (Maharashtra)
- **Built from:** [`ENG_fly-ash-power-plants_FY2025-26_STATES_CEA`](../ENG_fly-ash-power-plants_FY2025-26_STATES_CEA/) and the station-to-district lookup [`_reference/power-stations-maharashtra.csv`](../_reference/power-stations-maharashtra.csv) (Bharatnomy)
- **Downloaded:** 17 Nov 2026 (CEA file); districts assigned 24 Nov 2026
- **Script:** [`pipelines/power-stations-mh/build_station_districts_mh.py`](../pipelines/power-stations-mh/build_station_districts_mh.py); checks in `check_station_districts_mh.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | Maharashtra, 27 |
| `district`, `lgd_district_code` | District the plant is in; `State total` for CEA's printed Grand Total row |
| `cea_co2_station` | The same plant's name in the CEA CO2 Baseline Database (links to `ENG_power-station-generation-co2_*_MH_BNY_DIST`) |
| `plant` | Plant name as printed in the Year Book |
| `year` | 2025-26 |
| `utility` | Owning company |
| `installed_capacity_mw` | Installed capacity, MW |
| `ash_generation_lmt` | Ash generated, lakh tonnes (1 lakh tonnes = 100,000 t) |
| `ash_utilization_lmt` | Ash utilised, lakh tonnes |
| `ash_utilization_pct` | Ash utilised as % of ash generated; above 100 when ash stored in ponds from earlier years is also used |

## Notes

- Year Book names differ from the CO2 database; each plant is tied to its CO2-database station by hand (list in the script). `APL` (Adani Electricity Mumbai, 500 MW) is Dahanu TPS. For every plant the capacity printed here equals the tied station's capacity in the CO2 database.
- Values are copied unchanged; only the district and `cea_co2_station` columns are added.
- Checks (24 Nov 2026): 20 rows (19 plants + State total); plants add up to the printed Grand Total for ash generated (339.45) and used (312.22 lakh tonnes).
