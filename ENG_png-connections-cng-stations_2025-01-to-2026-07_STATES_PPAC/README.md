# Piped gas (PNG) connections and CNG stations by state, January 2025 and July 2026

Homes, businesses and factories connected to piped natural gas, and CNG stations, by the state (or group of states) of each city gas licence area.

## Source

- **Data:** Petroleum Planning & Analysis Cell (PPAC), *Status of PNG connections and CNG stations across India*, Excel on the "City Gas Distribution Network" page (two sheets: as on 31.01.2025 and 31.07.2026)
- **Link:** https://ppac.gov.in/natural-gas/city-gas-distribution-network
- **Downloaded:** 17 Nov 2026 (original in [`_sources/ppac-lpg-gas/raw/`](../_sources/ppac-lpg-gas/raw/))
- **Script:** [`pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py`](../pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py); checks in `check_ppac_lpg_gas.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State, when the row is a single state; blank for rows that club several states (licence areas crossing state borders); `All India` for Grand Total |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `area_group` | State/UT or group of states as printed ("clubbed based on the GAs authorised by PNGRB") |
| `date` | Date the figures refer to (as on), YYYY-MM-DD |
| `cng_stations_count` | CNG stations |
| `png_domestic_count` | Domestic PNG connections (homes) |
| `png_commercial_count` | Commercial PNG connections |
| `png_industrial_count` | Industrial PNG connections |
| `source_flag` | Status of the value: `provisional`, `not_available`, `not_applicable` |
| `sheet` | Sheet of the source file |
| `source_row` | Row in the sheet (the Jan 2025 sheet lists "Haryana" twice) |

## Notes

- `source_flag` = `provisional`: both sheets are marked (P).
- PPAC notes: all geographical areas (GAs) with PNG connections/CNG stations are counted as operational.
- City gas companies and the boundaries of their licence areas (PNGRB) are not in this table.
- Checks: area groups add up to the Grand Total on both dates.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`. Maharashtra-only areas: row `Maharashtra`; areas shared with Gujarat or Madhya Pradesh are separate rows.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
