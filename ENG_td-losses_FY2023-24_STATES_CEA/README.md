# Transmission and distribution (T&D) losses by state, 2023-24

Electricity available to each state, electricity consumed, and the difference lost in transmission and distribution, in GWh and as a percentage.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 6.4, "State-wise System Losses in the Year 2023-24" (page 106)
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
| `own_ipp_exbus_generation_gwh` | Own and IPP generation (and others) at the plant bus, GWh (col. 2) |
| `exbus_import_from_grid_gwh` | Net import from the grid (central schedule, bilateral, trading etc.), GWh (col. 3) |
| `exbus_import_from_cpp_gwh` | Import from captive power plants, GWh (col. 4) |
| `availability_exbus_gwh` | Total availability (2+3+4), GWh (col. 5) |
| `total_consumption_gwh` | Total consumption, GWh (col. 6) |
| `td_losses_gwh` | T&D losses (5-6), GWh (col. 7) |
| `td_losses_pct` | T&D losses as % of availability, 2023-24 (col. 8) |
| `td_losses_2022_23_pct` | T&D losses %, 2022-23, as printed in this table (col. 9) |

## Notes

- T&D losses are technical and commercial losses in the wires; they are not AT&C losses (which also count unpaid bills).
- Some state names are misspelt in the source ("Chandigrah", "Maharastra"); `system` keeps them, `state_ut` is standard.
- "Export to Other Countries 11295.19" printed below the table is not in the CSV.
- Checks: 41 rows; region rows equal the sum of their states and All India the sum of regions in all GWh columns; percentages within 0-100.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
