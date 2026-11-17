# Electricity sold by consumer category and state, 2023-24

Electricity sold by utilities to each category of consumer (homes, shops, industry, farms, etc.) in each state, in GWh.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 9.3, "Electrical Energy Sales to Ultimate Consumers Category-wise/State-wise, Utilities, 2023-24" (pages 139-140)
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
| `domestic_gwh` | Domestic (homes), GWh |
| `commercial_gwh` | Commercial, GWh |
| `industrial_lv_mv_gwh` | Industrial, low and medium voltage, GWh |
| `industrial_hv_gwh` | Industrial, high voltage, GWh |
| `public_lighting_gwh` | Public lighting, GWh |
| `public_water_works_gwh` | Public water works and sewage pumping, GWh |
| `traction_gwh` | Traction (railways, metro), GWh |
| `agriculture_gwh` | Agriculture (irrigation pumps), GWh |
| `miscellaneous_gwh` | Miscellaneous, GWh |
| `total_sold_gwh` | Total energy sold, GWh |

## Notes

- The table is printed over two pages (five categories each); the two halves are joined by row.
- CEA note: West Bengal and Jharkhand include DVC's sales to ultimate consumers in their areas.
- Checks: 41 rows; region sub-totals and All India recomputed in every column: no differences over 1 GWh; categories add up to the total.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.

## Changes on 17 Nov 2026

- Region sub-total rows removed (5 rows).
- Columns added (Bharatnomy calculations from the columns above, not published by the source):
  - `domestic_share_pct`: Domestic sales as % of total sold
  - `industrial_share_pct`: Industrial (LV, MV and HV) as % of total sold
  - `agriculture_share_pct`: Agriculture as % of total sold
- Script: [`pipelines/enrich/enrich_13.py`](../pipelines/enrich/enrich_13.py). Re-running this folder's build script removes these changes; run `enrich_13.py` again after it.
