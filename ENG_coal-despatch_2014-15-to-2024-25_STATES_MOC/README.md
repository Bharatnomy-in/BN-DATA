# Coal despatched from mines by state, 2014-15 to 2024-25

Raw coal sent out from the mines of each state each year, in million tonnes.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 3, sheet "dt7", Table 4.7 "State Wise Raw Coal Despatch in India during last Ten Years"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Financial year (April to March) as printed |
| `despatch_mt` | Raw coal despatch, million tonnes |
| `state_as_printed` | State name as printed in the source |

## Notes

- Share and growth columns left out.
- The sheet's last block also carries 1993-94 to 2013-14 for Uttar Pradesh and West Bengal only, with `#REF!` (broken formulas) for All India, and a stray side panel for Arunachal Pradesh; these are outside the table's ten-year span and are not taken.
- Blank cells: Meghalaya from 2018-19.
- Checks: states add up to All India in every year.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
