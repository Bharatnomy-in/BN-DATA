# Per capita electricity consumption by consumer category and state, 2023-24

Electricity sold to final consumers divided by mid-year population, by category, in kWh per person.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 9.7, "Per Capita Ultimate Consumption of Electricity State-wise/Category-wise, Utilities, 2023-24" (pages 151-152)
- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1001&subSubHeadingId=10084&title=General%20Review&lang=en (listed there as "2024")
- **Downloaded:** 17 Nov 2026 (original in [`_sources/cea-general-review/raw/`](../_sources/cea-general-review/raw/))
- **Script:** [`pipelines/cea-general-review/build_general_review.py`](../pipelines/cea-general-review/build_general_review.py); checks in `check_general_review.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `system` | Row label as printed (state, region, sub-total or total) |
| `year` | Financial year (April to March) as printed |
| `population_million` | Mid-year population (1 Oct 2023, Registrar General projection), million |
| `domestic_kwh` | Domestic, kWh per person |
| `commercial_kwh` | Commercial, kWh per person |
| `industrial_lv_mv_kwh` | Industrial (low and medium voltage), kWh per person |
| `industrial_hv_kwh` | Industrial (high voltage), kWh per person |
| `public_lighting_kwh` | Public lighting, kWh per person |
| `traction_kwh` | Traction, kWh per person |
| `agriculture_kwh` | Agriculture, kWh per person |
| `public_water_works_kwh` | Public water works and sewage pumping, kWh per person |
| `miscellaneous_kwh` | Miscellaneous, kWh per person |
| `total_kwh` | Total ultimate consumption per person, kWh |

## Notes

- This is ultimate consumption by utilities' consumers only; the headline per capita consumption (which adds losses, auxiliary and captive use) is in `ENG_per-capita-consumption_FY2023-24_STATES_CEA`.
- The merged UT is printed "DNH & DD" on the first page and "Daman & Diu" on the second (same row; `system` keeps the first).
- Checks: 41 rows; ratio columns only, so totals are not recomputed.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
