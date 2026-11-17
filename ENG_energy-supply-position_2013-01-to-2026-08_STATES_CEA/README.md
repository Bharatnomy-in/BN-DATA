# Electricity requirement and supply by state, monthly, January 2013 to August 2026

For each state, region and All India, every month: the electricity needed (energy requirement), the electricity supplied, and the shortfall, in million units (MU = GWh); also the same for April to that month.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *Energy Power Supply Position Report (Revised)*, monthly
- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1003&subSubHeadingId=10010&title=Power%20Supply%20Position%20-%20Energy&lang=en (one PDF per month)
- **Downloaded:** 17 Nov 2026 (original in 164 files listed (about 56 MB, not committed; `pipelines/cea/fetch_psp_energy.sh` downloads them, see [`_sources/cea-power-supply-position/`](../_sources/cea-power-supply-position/)))
- **Script:** [`pipelines/cea/build_psp_energy.py`](../pipelines/cea/build_psp_energy.py); checks in `check_psp_energy.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `system` | Row label as printed (English part): state, DVC, region, `Others (<region>)`, All India |
| `year` | Calendar year of the month |
| `month` | Month, YYYY-MM |
| `energy_requirement_mu` | Energy requirement in the month, MU net |
| `energy_supplied_mu` | Energy supplied ("availability" before 2017), MU net |
| `surplus_deficit_mu` | Up to Feb 2017: "Surplus / Deficit (-)" = supplied minus requirement, MU. Negative = shortage. Blank later |
| `surplus_deficit_pct` | Same, % of requirement |
| `energy_not_supplied_mu` | From 2017: "Energy not Supplied" = requirement minus supplied, MU. Positive = shortage. Blank before |
| `energy_not_supplied_pct` | Same, % of requirement |
| `apr_to_month_energy_requirement_mu` | Same as `energy_requirement_mu`, for April of the financial year to this month (blank in April reports, which print only the month) |
| `apr_to_month_energy_supplied_mu` | Same as `energy_supplied_mu`, for April of the financial year to this month (blank in April reports, which print only the month) |
| `apr_to_month_surplus_deficit_mu` | Same as `surplus_deficit_mu`, for April of the financial year to this month (blank in April reports, which print only the month) |
| `apr_to_month_surplus_deficit_pct` | Same as `surplus_deficit_pct`, for April of the financial year to this month (blank in April reports, which print only the month) |
| `apr_to_month_energy_not_supplied_mu` | Same as `energy_not_supplied_mu`, for April of the financial year to this month (blank in April reports, which print only the month) |
| `apr_to_month_energy_not_supplied_pct` | Same as `energy_not_supplied_pct`, for April of the financial year to this month (blank in April reports, which print only the month) |
| `source_marks` | Symbols printed next to a label or number, as `<column>:<symbol>` (explained in Notes) |

## Notes

- **61 months are missing.** CEA's "Power Supply Position - Energy" page lists generation reports instead of energy reports for these months: 2014-05 to 2016-08, 2017-03 to 2018-04, 2018-06 to 2018-12, 2019-03 to 2020-01, and 2020-03. The data has 103 months. For full-year totals use the `apr_to_month_` columns of March reports (2013-03, 2014-03, 2021-03 onwards) or the annual General Review.
- Sign change in 2017, as in the peak dataset: before, "Surplus / Deficit (-)" (negative = shortage); after, "Energy not Supplied" (positive = shortage). The two are in separate columns so no sign is changed.
- `source_marks`: `system:*` = "Excludes energy exported to Bangladesh" (Tripura); `system:(**)` = CEA: data for the month not received, previous month's data used (Andaman & Nicobar, several months in 2025-26).
- Lakshadweep and Andaman & Nicobar are stand-alone systems, not part of regional totals. From April 2022 the regional figures "include data of other miscellaneous entities drawing power directly from ISTS", and some months print these as `Others (<region>)` rows; in months without those rows the region total is larger than the sum of its states (CEA's own figures, kept as published).
- Checks (17 Nov 2026): 4,388 rows; no duplicate system-month; shortfall equals requirement minus supplied (within 1 MU) and supplied never exceeds requirement, for the month and April-to-month; percentages within -100 to 100. Region totals equal the sum of their members except in the months described above (185 region-months from 2022 and, by 4 MU, Southern Region in 2013-14).
- Companion of `ENG_peak-demand_2013-01-to-2026-08_STATES_CEA` (same reports' peak edition).
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
