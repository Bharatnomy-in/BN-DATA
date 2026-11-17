# PMUY (Ujjwala) LPG connections by state, 1 October 2026

Free LPG connections given to poor households under the Pradhan Mantri Ujjwala Yojana, cumulative.

## Source

- **Data:** Petroleum Planning & Analysis Cell (PPAC), Ministry of Petroleum & Natural Gas, *LPG Profile Report H1 FY 2026-27* (November 2026), compiled from IOCL, BPCL and HPCL data
- **Table taken from:** Table 12 "State-wise PMUY connections as on 01.10.2026 (P)" (page 34)
- **Link:** https://ppac.gov.in/download.php?file=rep_studies/1794560760_LPG_Profile_Report_H1_FY_2026-27_Web_Version.pdf
- **Downloaded:** 17 Nov 2026 (original in [`_sources/ppac-lpg-gas/raw/`](../_sources/ppac-lpg-gas/raw/))
- **Script:** [`pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py`](../pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py); checks in `check_ppac_lpg_gas.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `system` | Row label as printed (state, region, sub-total or total) |
| `date` | Date the figures refer to (as on), YYYY-MM-DD |
| `pmuy_connections_count` | PMUY connections, number |

## Notes

- Region rows (`Sub Total North`, `Sub Total North-East`, `Sub Total East`, `Sub Total West`, `Sub Total South`) are kept with blank `state_ut`; `All India` is the total.
- Figures are provisional (P) as marked in the report title.
- Same figures as the PMUY column of Table 11 (`ENG_lpg-scheme-beneficiaries_2026-10_STATES_PPAC`). An older snapshot (1 Aug 2026) from PPAC's web page is in `raw/` but not converted.
- Checks (17 Nov 2026): 42 rows; region sub-totals and All India recomputed: no differences above rounding (0.1).
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.

## Changes on 17 Nov 2026

- Region sub-total rows removed (5 rows).
- Columns added (Bharatnomy calculations from the columns above, not published by the source):
  - `ppac_region`: PPAC region the state is listed under (North, North-East, East, West, South)
  - `share_of_india_pct`: Share of All India PMUY connections, %
  - `rank`: Rank by PMUY connections, 1 = most
- Script: [`pipelines/enrich/enrich_13.py`](../pipelines/enrich/enrich_13.py). Re-running this folder's build script removes these changes; run `enrich_13.py` again after it.
