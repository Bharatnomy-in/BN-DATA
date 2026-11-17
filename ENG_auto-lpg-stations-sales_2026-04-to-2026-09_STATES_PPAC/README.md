# Auto LPG stations and sales by state, 2026

Auto LPG dispensing stations (for vehicles) on 1 October 2026 and auto LPG sold April-September 2026.

## Source

- **Data:** Petroleum Planning & Analysis Cell (PPAC), Ministry of Petroleum & Natural Gas, *LPG Profile Report H1 FY 2026-27* (November 2026), compiled from IOCL, BPCL and HPCL data
- **Table taken from:** Table 5 "No of Auto LPG dispensing stations as on 01.10.2026 and Auto LPG Sales during Apr-Sep'26 (P)" (page 19)
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
| `period` | Months covered |
| `auto_lpg_stations_count` | Auto LPG dispensing stations (ALDS), 1 Oct 2026 |
| `auto_lpg_sales_t` | Auto LPG sales, tonnes (MT), April-September 2026 |

## Notes

- Region rows (`Sub Total North`, `Sub Total North-East`, `Sub Total East`, `Sub Total West`, `Sub Total South`) are kept with blank `state_ut`; `All India` is the total.
- Figures are provisional (P) as marked in the report title.
- Checks (17 Nov 2026): 42 rows; region sub-totals and All India recomputed: no differences above rounding (0.1).
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
