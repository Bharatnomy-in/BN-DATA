# Coal royalty, DMF and NMET paid by state, 2022-23 to 2024-25

Royalty, District Mineral Foundation and National Mineral Exploration Trust payments on coal in each state, by Coal India (CIL) and other companies, in Rs crore.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 6, sheet "tb7.7", Table 7.7 "State Wise Payment of Royalty, DMF & NMET in India during last Three Years (CIL & Non-CIL)"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `company_type` | `CIL` (Coal India), `Non-CIL`, `Total` |
| `year` | Financial year (April to March) as printed |
| `royalty_inr_crore` | Royalty paid, Rs crore |
| `dmf_inr_crore` | DMF paid, Rs crore |
| `nmet_inr_crore` | NMET paid, Rs crore |
| `state_as_printed` | State name as printed in the source |

## Notes

- Blank cells are blank in the source. Odisha's 2024-25 Total for royalty and DMF is blank in the source, so the state Totals add up to less than All India in 2024-25 (the CIL and Non-CIL rows are there).
- Checks: CIL + Non-CIL = Total in every state and year; state Totals add up to All India except as noted.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
