# Coal resources by state (proved, indicated, inferred), 2005 to 2025

Coal estimated to lie underground in each state, in million tonnes, split by how certain the estimate is: proved (confirmed by drilling), indicated and inferred.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 1, sheet "2.2", Table 2.2 "State Wise Inventory of Geological Resources of Coal in India (as on 1st April)"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `coalfield_type` | Gondwana coalfields (most of India's coal) or Tertiary coalfields (North-East) |
| `date` | Inventory date (1 April of the year; 1 January for 2005 and 2006) |
| `proved_mt` | Proved resources, million tonnes |
| `indicated_mt` | Indicated resources, million tonnes |
| `inferred_mt` | Inferred resources, million tonnes |
| `total_mt` | Total, million tonnes |
| `state_as_printed` | State name as printed in the source |

## Notes

- Most states have four dates (2022 to 2025); Andhra Pradesh (Gondwana) and Assam (Tertiary) carry a longer series from 2005, as the sheet prints them.
- Rows `Total Gondwana` and `Total Tertiary` have blank `state_ut`; `All India` is the total of both.
- Checks: proved + indicated + inferred = total in every row; Gondwana and Tertiary state rows add up to their printed totals.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
