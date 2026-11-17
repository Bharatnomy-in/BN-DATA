# Coal production by state, 2015-16 to 2024-25

Raw coal mined in each state each year, in million tonnes.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 2, sheet "PT9", Table 3.9 "State Wise Raw Coal Production in last Ten Years"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Financial year (April to March) as printed |
| `production_mt` | Raw coal production, million tonnes |
| `state_as_printed` | State name as printed in the source |

## Notes

- The table's "Share (%)" and "Growth (%)" columns are left out: they are computed from the quantities.
- Blank cells: Meghalaya from 2018-19 (left blank in the source, no production reported).
- Checks: the states add up to All India except in six years where All India is 0.02-0.12 million tonnes higher (2015-16 to 2019-20, 2022-23), as printed.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
