# Coal production by state and type of mine (open cast, underground), 2021-22 to 2024-25

Raw coal from open cast (surface) and underground mines in each state, in million tonnes.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 2, sheet "PT25", Table 3.25 "State Wise Production of Raw Coal by type of Mines in last Three Years" (prints four years)
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Financial year (April to March) as printed |
| `open_cast_mt` | Open cast mines, million tonnes |
| `underground_mt` | Underground mines, million tonnes |
| `total_mt` | Total, million tonnes |
| `state_as_printed` | State name as printed in the source |

## Notes

- Blank cells are blank in the source (nil).
- Checks: open cast + underground = total in every row; states add up to All India.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
