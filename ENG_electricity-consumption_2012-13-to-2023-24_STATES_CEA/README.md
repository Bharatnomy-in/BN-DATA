# Electricity consumption by state, 2012-13 to 2023-24

Electricity sold to final consumers by utilities in each state every year, in gigawatt-hours (GWh = million units). Captive (own) generation of industries is not included.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 1.7, "Growth of Total Electricity Consumption (GWh) by Ultimate Consumers, State-wise, Utilities only" (page 32)
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
| `consumption_gwh` | Electricity consumed by ultimate consumers, GWh |

## Notes

- The rows for Daman & Diu (1814 ... 2482) and Dadra & Nagar Haveli (4595 ... 6380), 2012-13 to 2021-22, have no label in the 2025 PDF; they are named from the same table in General Review 2023, which labels them. From 2022-23 the merged UT is reported (row printed as "Daman & Diu", values 9335 and 10199; stored as `Dadra & Nagar Haveli and Daman & Diu`).
- `Andhra Pradesh (undivided)`: 2012-13 and 2013-14, before Telangana was formed (blank `state_ut`). From 2014-15 Andhra Pradesh and Telangana are separate.
- Jammu & Kashmir: no value is printed for 2023-24; the row is labelled Jammu & Kashmir throughout (it includes Ladakh from 2019-20 onwards).
- Checks (17 Nov 2026): 500 rows; no duplicate keys; each region sub-total equals the sum of its states and All India the sum of regions for every year (one 2 GWh rounding difference, Northern Region 2023-24).
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
