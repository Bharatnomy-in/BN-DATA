# LPG distributors by state, 2001 to 2026

Number of LPG gas agencies (distributors) of the public sector oil companies in each state, every year since 2001.

## Source

- **Data:** Petroleum Planning & Analysis Cell (PPAC), *Statewise LPG distributors of the Oil Marketing Companies (Public Sector Undertakings)*, Excel on the "LPG Distributors" page (Source: Oil Marketing Companies)
- **Link:** https://ppac.gov.in/infrastructure/lpg-distributors
- **Downloaded:** 17 Nov 2026 (original in [`_sources/ppac-lpg-gas/raw/`](../_sources/ppac-lpg-gas/raw/))
- **Script:** [`pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py`](../pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py); checks in `check_ppac_lpg_gas.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `system` | Row label as printed (state, region, sub-total or total) |
| `as_on` | Year as printed in the header (`2001` ... `2025`; PPAC's report gives these counts as on 1 April) or `2026-08-01` for the latest, provisional column |
| `distributors_count` | Number of LPG distributors |
| `source_flag` | Status of the value: `provisional`, `not_available`, `not_applicable` |
| `source_marks` | Symbols printed next to a label or number, as `<column>:<symbol>` (explained in Notes) |

## Notes

- `source_flag`: `provisional` for 2026-08-01 (marked (P)); `not_applicable` for Ladakh before it became a UT (blank in the source).
- `source_marks` `system:#` on Telangana: "Telangana state was formed in FY 2014-15 ... For previous years Nil figures is taken for Telangana and Andhra Pradesh includes data for both".
- Region sub-total rows are kept with blank `state_ut`.
- Checks (17 Nov 2026): 1,118 rows; region sub-totals and All India recomputed for every year: no differences.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
