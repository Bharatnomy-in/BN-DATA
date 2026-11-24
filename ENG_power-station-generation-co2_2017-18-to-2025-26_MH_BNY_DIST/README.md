# Power stations by district, Maharashtra: net generation and CO2, 2017-18 to 2025-26

Every grid-connected thermal (coal, gas, oil), hydro and nuclear power station in Maharashtra listed by the Central Electricity Authority, with the district it stands in, and for each year its net generation, CO2 emitted and CO2 per MWh. 55 stations, 9 years. Sum by district for district totals.

## Source

- **Data:** Central Electricity Authority (CEA), *CO2 Baseline Database for the Indian Power Sector*, Version 22.0 (1 August 2026), station rows for Maharashtra
- **Built from:** [`ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA`](../ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA/) and the station-to-district lookup [`_reference/power-stations-maharashtra.csv`](../_reference/power-stations-maharashtra.csv) (Bharatnomy)
- **Link:** https://cea.nic.in/cdm-co2-baseline-view?mappingId=234&lang=en
- **Downloaded:** 17 Nov 2026 (CEA file); districts assigned 24 Nov 2026
- **Script:** [`pipelines/power-stations-mh/build_station_districts_mh.py`](../pipelines/power-stations-mh/build_station_districts_mh.py); checks in `check_station_districts_mh.py`

## How the district is found

CEA gives no location. Each station is matched by name to the WRI Global Power Plant Database (which took its Indian plant list from CEA), and takes the district its coordinates fall in. Nine stations are set by hand, with the reason in the lookup's `note`: three WRI puts in Thane that are in Palghar today (Dahanu, Tarapur, Surya), three not in WRI (NTPC Solapur, Shirpur, Dimbhe) and three spelled differently there.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | Maharashtra, 27 |
| `district`, `lgd_district_code` | District the station is in (current LGD name and code) |
| `station` | Station name as printed by CEA |
| `year` | Financial year |
| `capacity_mw_2026_03_31` | Capacity on 31 Mar 2026, MW (0 = retired or not reported by then) |
| `sector` | Owner type: CENTER, STATE, PVT |
| `owner` | Owning company |
| `type` | THERMAL, HYDRO or NUCLEAR |
| `fuel_1`, `fuel_2` | Main and secondary fuel (COAL, GAS, OIL); blank for hydro and nuclear |
| `net_generation_gwh` | Net generation in the year, GWh |
| `co2_emissions_t` | CO2 emitted in the year, tonnes |
| `co2_intensity_t_per_mwh` | Tonnes of CO2 per MWh generated |

## Notes

- Values are copied unchanged from the CEA table; only the district columns are added.
- 110 blank `net_generation_gwh` cells: CEA prints a dash, mostly for small hydro stations and years a station did not run (see the source table's `source_marks`).
- Capacity is the 31 March 2026 figure for every year, so stations that retired units earlier (e.g. JSW Ratnagiri, 1,200 MW before) show their current capacity. The source table's approximate plant load factor is left out here for that reason (it goes above 100% for JSW Ratnagiri).
- Koyna (district: Ratnagiri, where the Pophali powerhouses are; the dam is in Satara), Ghatghar (Thane; upper dam in Ahilyanagar) and Pench (shared with Madhya Pradesh) span more than one district.
- Not listed by CEA here: solar, wind and other non-hydro renewables, and captive (industrial) plants. For those, see `ENG_power-plants_2021_*_WRI_DIST`.
- Checks (24 Nov 2026): 495 rows = 55 stations x 9 years, no duplicates; generation, CO2 and capacity identical to the source table; no negative values; CO2 intensity within 0-2 t/MWh; every district and code is in `_reference/geography.csv`.
