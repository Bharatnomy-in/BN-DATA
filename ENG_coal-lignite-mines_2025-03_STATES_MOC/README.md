# Number of coal and lignite mines by state and type, 31 March 2025

Coal and lignite mines in each state: producing, non-producing and all operational mines, split into open cast, underground and mixed.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 11, sheet "tab12.2", Table 12.2 "State Wise Number of Producing Coal & Lignite Mines as on 31/03/2025"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `mineral` | `coal` or `lignite` |
| `date` | Date the figures refer to (as on), YYYY-MM-DD |
| `producing_open_cast_count` | Producing mines, open cast |
| `producing_underground_count` | Producing mines, underground |
| `producing_mixed_count` | Producing mines, mixed |
| `producing_total_count` | Producing mines, total |
| `non_producing_open_cast_count` | Non-producing mines, open cast |
| `non_producing_underground_count` | Non-producing mines, underground |
| `non_producing_mixed_count` | Non-producing mines, mixed |
| `non_producing_total_count` | Non-producing mines, total |
| `operational_open_cast_count` | All operational mines, open cast |
| `operational_underground_count` | All operational mines, underground |
| `operational_mixed_count` | All operational mines, mixed |
| `operational_total_count` | All operational mines, total |
| `state_as_printed` | State name as printed in the source |

## Notes

- Blank cells are blank in the source (lignite rows). Mines by owner (public / private) are in Table 12.8 of the same chapter, not taken yet.
- Checks: open cast + underground + mixed = total in every group.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
