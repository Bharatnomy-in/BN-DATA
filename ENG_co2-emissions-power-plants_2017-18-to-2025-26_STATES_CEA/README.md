# Power stations and units: net generation and CO2 emissions, 2017-18 to 2025-26

Every grid-connected thermal, hydro and nuclear power station in India (and its units), with state, owner, fuel and capacity, and for each year its net electricity generation, CO2 emitted and CO2 per MWh. Renewable plants other than hydro are not listed.

## Source

- **Data:** Central Electricity Authority (CEA), *CO2 Baseline Database for the Indian Power Sector*, Version 22.0 (1 August 2026)
- **Table taken from:** sheet "Data"
- **Link:** https://cea.nic.in/cdm-co2-baseline-view?mappingId=234&lang=en (CDM-CO2 Baseline Database Reports; Excel file "1. Baseline Carbon Dioxide Emission Database Version 22.0")
- **Downloaded:** 17 Nov 2026 (original in [`_sources/cea-co2-baseline/raw/`](../_sources/cea-co2-baseline/raw/) (database and user guide))
- **Script:** [`pipelines/cea-co2-baseline/build_co2_baseline.py`](../pipelines/cea-co2-baseline/build_co2_baseline.py); checks in `check_co2_baseline.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `station` | Station name as printed |
| `unit_no` | Unit number; `0` = the whole station (station total row) |
| `year` | Financial year (April to March) as printed |
| `commissioned` | Date the unit was commissioned (blank on station rows) |
| `capacity_mw_2026_03_31` | Capacity on 31 Mar 2026, MW |
| `state_as_printed` | State name as printed in the source |
| `sector` | Owner type: CENTER, STATE, PVT |
| `owner` | Owning company ("SYSTEM" in the source) |
| `type` | THERMAL, HYDRO or NUCLEAR |
| `fuel_1` | Main fuel (COAL, LIGN = lignite, GAS, OIL, DISL = diesel); blank for hydro and nuclear |
| `fuel_2` | Secondary fuel |
| `net_generation_gwh` | Net generation in the year, GWh |
| `co2_emissions_t` | Absolute CO2 emissions in the year, tonnes |
| `co2_intensity_t_per_mwh` | Specific emissions, tonnes CO2 per MWh |
| `in_operating_margin` | `1` if the unit/station counts in the year's operating margin |
| `in_build_margin` | `1` if the unit counts in the build margin; a `CDM#<number>` value is the registered CDM project number printed instead |
| `serial_no` | Station serial number in the source (shared by a station's rows) |
| `source_row` | Row number in the source sheet (unique per unit; the source repeats some unit numbers) |
| `source_marks` | Symbols printed next to a label or number, as `<column>:<symbol>` (explained in Notes) |

## Notes

- One row per unit (or station total) per year; years in which a unit has no entry at all are left out.
- Numbers are the spreadsheet's values rounded to 12 significant digits (this only removes floating-point noise such as 8652.237000000001).
- `source_marks` `net_generation_gwh:-`: a dash is printed instead of a number (mostly hydro units).
- "TSECL" (Tripura State Electricity Corporation) is printed in the state column for Gumti HPS; `state_ut` = Tripura, `state_as_printed` keeps TSECL.
- The database repeats some unit numbers (e.g. Jorethang Loop unit 1, Shirpur unit 1, Konaseema and Peddapuram units); use `source_row` to tell them apart.
- Unit rows do not always add up to their station row (in some years only station figures are given), so use `unit_no` = 0 for station totals.
- Checks (17 Nov 2026): 16,731 rows, 589 stations; station CO2 summed by year equals the Results sheet total ("CO2 emissions in database") within 0.07%; station net generation within 0.24%.
- **Nagpur:** stations near Nagpur include KORADI, K_KHEDA II (Khaparkheda), MOUDA STPS, BUTIBORI TPP -II, MIHAN TPP; plant locations (district, coordinates) are not given.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.

## Changes on 17 Nov 2026

- Columns removed (helpers): `unit_no`, `commissioned`, `state_as_printed`, `source_marks`, `in_operating_margin`, `in_build_margin`.
- Unit rows removed: one row per station and year (station totals, `unit_no` 0); 11717 unit rows dropped.
- Columns added (Bharatnomy calculations from the columns above, not published by the source):
  - `plant_load_factor_pct`: Net generation as % of what the station's 31 Mar 2026 capacity could produce running all year (approximate PLF: uses current capacity and net, not gross, generation)
  - `is_coal`: `yes` if the main fuel is coal or lignite
  - `near_nagpur`: `yes` for stations in Nagpur district: Koradi, Khaparkheda (K_KHEDA II), Mouda, Butibori, MIHAN
- Script: [`pipelines/enrich/enrich_13.py`](../pipelines/enrich/enrich_13.py). Re-running this folder's build script removes these changes; run `enrich_13.py` again after it.
