# Per capita electricity consumption by state, 2023-24

Gross electricity consumed in each state (utilities plus captive plants) divided by mid-year population: the official per capita consumption figure, in kWh per person.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 9.9, "Annual Per Capita Consumption of Electricity, State-wise (Utilities & Non-Utilities), 2023-24" (pages 154-155)
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
| `population_000` | Mid-year population (1 Oct 2023), thousand (col. 2) |
| `net_generation_and_drawal_gwh` | Net generation of utilities + net drawal from grid including imports, GWh (col. 3) |
| `aux_consumption_own_generation_gwh` | Auxiliary consumption for the state's own generation, GWh (col. 4) |
| `aux_consumption_for_regional_drawal_gwh` | Auxiliary consumption for drawal from the regional grid, GWh (col. 5) |
| `total_aux_consumption_gwh` | Total auxiliary consumption (4+5), GWh (col. 6) |
| `gross_generation_and_drawal_gwh` | Gross generation of utilities + gross drawal including imports (3+6), GWh (col. 7) |
| `captive_consumption_from_self_generation_gwh` | Gross consumption out of self-generation by captive industries, GWh (col. 8) |
| `gross_consumption_gwh` | Total gross consumption, utilities + non-utilities (7+8), GWh (col. 9) |
| `per_capita_consumption_kwh` | Per capita consumption of electricity (9/2), kWh |

## Notes

- Checks: 41 rows; region rows and All India recomputed in every summable column: no differences over 1 GWh.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.

## Changes on 17 Nov 2026

- Region rows removed (5 rows).
- Columns added (Bharatnomy calculations from the columns above, not published by the source):
  - `ratio_to_all_india`: Per capita consumption divided by the All India figure (1400 kWh)
  - `rank_among_states`: Rank by per capita consumption, 1 = highest (states and the joint J&K-Ladakh row)
  - `consumption_band`: Low (<1000), medium (1000-1999) or high (2000+ kWh per person)
- Script: [`pipelines/enrich/enrich_13.py`](../pipelines/enrich/enrich_13.py). Re-running this folder's build script removes these changes; run `enrich_13.py` again after it.
